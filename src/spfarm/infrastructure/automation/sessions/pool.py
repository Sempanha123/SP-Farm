"""Thread-safe per-device Appium session pool."""

from __future__ import annotations

import contextlib
import threading
import uuid
from dataclasses import dataclass
from typing import Any, Optional, Protocol

import requests

from spfarm.infrastructure.automation.appium.service import (
    AppiumServer,
    AppiumServiceManager,
    PortAllocator,
)


class AppiumTransport(Protocol):
    def request(
        self,
        method: str,
        url: str,
        payload: Optional[dict[str, Any]] = None,
        timeout: float = 30.0,
    ) -> tuple[int, dict[str, Any]]: ...


class RequestsAppiumTransport:
    def request(
        self,
        method: str,
        url: str,
        payload: Optional[dict[str, Any]] = None,
        timeout: float = 30.0,
    ) -> tuple[int, dict[str, Any]]:
        response = requests.request(method, url, json=payload, timeout=timeout)
        try:
            body = response.json()
        except ValueError:
            body = {"value": response.text}
        return response.status_code, body


@dataclass
class AppiumSession:
    device_id: str
    adb_target: str
    session_id: str
    server: AppiumServer
    system_port: int
    capabilities: dict[str, Any]
    lease_count: int = 1


class AppiumSessionLease:
    def __init__(self, pool: AppiumSessionPool, device_id: str, token: str) -> None:
        self._pool = pool
        self.device_id = device_id
        self.token = token
        self._released = False

    @property
    def session(self) -> AppiumSession:
        return self._pool.get_session(self.device_id)

    def release(self) -> None:
        if not self._released:
            self._pool.release(self)
            self._released = True

    def __enter__(self) -> AppiumSessionLease:
        return self

    def __exit__(self, *_args: object) -> None:
        self.release()


class AppiumSessionPool:
    def __init__(
        self,
        service_manager: AppiumServiceManager,
        transport: Optional[AppiumTransport] = None,
        system_ports: Optional[PortAllocator] = None,
        command_timeout: float = 30.0,
    ) -> None:
        self.service_manager = service_manager
        self.transport = transport or RequestsAppiumTransport()
        self._system_ports = system_ports or PortAllocator(start=8200)
        self._command_timeout = command_timeout
        self._sessions: dict[str, AppiumSession] = {}
        self._leases: dict[str, str] = {}
        self._device_locks: dict[str, threading.RLock] = {}
        self._lock = threading.RLock()

    def acquire(
        self,
        device_id: str,
        adb_target: str,
        capabilities: Optional[dict[str, Any]] = None,
    ) -> AppiumSessionLease:
        device_lock = self._get_device_lock(device_id)
        with device_lock:
            with self._lock:
                session = self._sessions.get(device_id)
            if session:
                self._recover_if_needed(session)
                session.lease_count += 1
            else:
                session = self._create_session(device_id, adb_target, capabilities or {})
                with self._lock:
                    self._sessions[device_id] = session
            token = uuid.uuid4().hex
            with self._lock:
                self._leases[token] = device_id
            return AppiumSessionLease(self, device_id, token)

    def release(self, lease: AppiumSessionLease) -> None:
        device_lock = self._get_device_lock(lease.device_id)
        with device_lock:
            with self._lock:
                device_id = self._leases.pop(lease.token, None)
                session = self._sessions.get(lease.device_id)
            if device_id is None or session is None:
                return
            session.lease_count -= 1
            if session.lease_count <= 0:
                self._delete_session(session)
                with self._lock:
                    self._sessions.pop(session.device_id, None)
                self._system_ports.release(session.system_port)
                self.service_manager.stop(session.server)

    def get_session(self, device_id: str) -> AppiumSession:
        with self._lock:
            session = self._sessions.get(device_id)
        if not session:
            raise RuntimeError(f"No Appium session for device {device_id}")
        return session

    def execute(
        self,
        lease: AppiumSessionLease,
        method: str,
        path: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        device_lock = self._get_device_lock(lease.device_id)
        with device_lock:
            self._validate_lease(lease)
            session = self.get_session(lease.device_id)
            session = self._recover_if_needed(session)
            status, body = self.transport.request(
                method,
                f"{session.server.url}/session/{session.session_id}{path}",
                payload,
                self._command_timeout,
            )
            if status >= 400:
                raise RuntimeError(self._error_message(body, status))
            return body

    def close_all(self) -> None:
        with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
            self._leases.clear()
        for session in sessions:
            self._delete_session(session)
            self._system_ports.release(session.system_port)
            self.service_manager.stop(session.server)

    def diagnostics(self, device_id: Optional[str] = None) -> dict[str, object]:
        with self._lock:
            sessions = list(self._sessions.values())
        if device_id is not None:
            sessions = [session for session in sessions if session.device_id == device_id]
        return {
            "active_sessions": len(sessions),
            "sessions": [
                {
                    "device_id": session.device_id,
                    "server_port": session.server.port,
                    "system_port": session.system_port,
                    "server_running": session.server.is_running,
                    "server_generation": session.server.generation,
                    "lease_count": session.lease_count,
                }
                for session in sessions
            ],
        }

    def _create_session(
        self,
        device_id: str,
        adb_target: str,
        extra_capabilities: dict[str, Any],
        server: Optional[AppiumServer] = None,
        system_port: Optional[int] = None,
    ) -> AppiumSession:
        selected_server = server or self.service_manager.start()
        selected_system_port = (
            system_port if system_port is not None else self._system_ports.acquire()
        )
        appium_options = {
            "automationName": "UiAutomator2",
            "udid": adb_target,
            "systemPort": selected_system_port,
            "newCommandTimeout": 120,
            **extra_capabilities,
        }
        capabilities = {
            "platformName": "Android",
            "appium:options": appium_options,
        }
        try:
            status, body = self.transport.request(
                "POST",
                f"{selected_server.url}/session",
                {"capabilities": {"alwaysMatch": capabilities}},
                self._command_timeout,
            )
            if status >= 400:
                raise RuntimeError(self._error_message(body, status))
            session_id = body.get("sessionId") or body.get("value", {}).get("sessionId")
            if not session_id:
                raise RuntimeError("Appium did not return a session ID")
            return AppiumSession(
                device_id=device_id,
                adb_target=adb_target,
                session_id=str(session_id),
                server=selected_server,
                system_port=selected_system_port,
                capabilities=capabilities,
            )
        except Exception:
            self.service_manager.stop(selected_server)
            if system_port is None:
                self._system_ports.release(selected_system_port)
            raise

    def _recover_if_needed(self, session: AppiumSession) -> AppiumSession:
        server = self.service_manager.ensure_running(session.server)
        if server is session.server:
            return session
        appium_options = dict(session.capabilities["appium:options"])
        appium_options.pop("udid", None)
        appium_options.pop("systemPort", None)
        replacement = self._create_session(
            session.device_id,
            session.adb_target,
            appium_options,
            server=server,
            system_port=session.system_port,
        )
        replacement.lease_count = session.lease_count
        with self._lock:
            self._sessions[session.device_id] = replacement
        return replacement

    def _delete_session(self, session: AppiumSession) -> None:
        with contextlib.suppress(requests.RequestException):
            self.transport.request(
                "DELETE",
                f"{session.server.url}/session/{session.session_id}",
                timeout=min(self._command_timeout, 5.0),
            )

    def _get_device_lock(self, device_id: str) -> threading.RLock:
        with self._lock:
            return self._device_locks.setdefault(device_id, threading.RLock())

    def _validate_lease(self, lease: AppiumSessionLease) -> None:
        with self._lock:
            if self._leases.get(lease.token) != lease.device_id:
                raise RuntimeError("Appium session lease is not active")

    @staticmethod
    def _error_message(body: dict[str, Any], status: int) -> str:
        value = body.get("value")
        if isinstance(value, dict) and value.get("message"):
            return str(value["message"])
        return f"Appium request failed with HTTP {status}"
