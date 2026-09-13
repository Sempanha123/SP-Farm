"""Tests for concurrent multi-provider device registry execution."""

from __future__ import annotations

import concurrent.futures
import json
import threading
from pathlib import Path

from spfarm.application.events.base import EventBus
from spfarm.application.services.device_registry import DeviceRegistry
from spfarm.domain.enums import DeviceProvider, DeviceState
from spfarm.infrastructure.devices.adb import AdbRunner
from spfarm.infrastructure.devices.fake_provider import FakeDeviceProvider
from spfarm.infrastructure.devices.ldplayer.cli import LDConsoleRunner
from spfarm.infrastructure.devices.ldplayer.provider import LDPlayerProvider
from spfarm.infrastructure.devices.mumu.cli import MuMuManagerRunner
from spfarm.infrastructure.devices.mumu.provider import MuMuProvider


def _build_test_registry(tmp_path: Path) -> tuple[DeviceRegistry, LDPlayerProvider, MuMuProvider]:
    ld_dir = tmp_path / "ldplayer"
    ld_dir.mkdir(parents=True)
    (ld_dir / "ldconsole.exe").write_text("fake")

    def mock_ld_exec(args: list[str], cwd: Path | None, timeout: float):
        if "list2" in args:
            return 0, "0,LDPlayer-0,0,0,0,0,0\n1,LDPlayer-1,100,200,1,300,400\n", ""
        return 0, "OK", ""

    adb_exe = tmp_path / "adb.exe"
    adb_exe.write_text("fake")

    def mock_adb_exec(args: list[str], timeout: float):
        return 0, b"\x89PNG\r\n\x1a\nmock-screen", b""

    adb_runner = AdbRunner(executable_path=adb_exe, executor=mock_adb_exec)
    ld_runner = LDConsoleRunner(custom_install_dir=ld_dir, process_executor=mock_ld_exec)
    ld_prov = LDPlayerProvider(runner=ld_runner, adb_runner=adb_runner)

    mumu_dir = tmp_path / "mumu"
    mumu_dir.mkdir(parents=True)
    (mumu_dir / "MuMuManager.exe").write_text("fake")

    mumu_payload = [
        {"index": 0, "name": "MuMuPlayer-0", "title": "MuMu-Worker-0", "is_running": False, "adb_port": 16384},
        {"index": 1, "name": "MuMuPlayer-1", "title": "MuMu-Worker-1", "is_running": True, "adb_port": 16416},
    ]

    def mock_mumu_exec(args: list[str], cwd: Path | None, timeout: float):
        if "api" in args and "player_state" in args and "all" in args:
            return 0, json.dumps(mumu_payload), ""
        return 0, "OK", ""

    mumu_runner = MuMuManagerRunner(custom_install_dir=mumu_dir, process_executor=mock_mumu_exec)
    mumu_prov = MuMuProvider(runner=mumu_runner, adb_runner=adb_runner)

    fake_prov = FakeDeviceProvider()

    event_bus = EventBus()
    registry = DeviceRegistry(event_bus=event_bus)

    registry.register_provider(fake_prov)
    registry.register_provider(ld_prov)
    registry.register_provider(mumu_prov)

    return registry, ld_prov, mumu_prov


def test_concurrent_multi_provider_discovery(tmp_path: Path) -> None:
    """Registry aggregates devices from Fake, LDPlayer, and MuMu without collisions."""
    registry, _, _ = _build_test_registry(tmp_path)
    devices = registry.discover_all()

    # 2 fake + 2 LDPlayer + 2 MuMu = 6 devices total
    assert len(devices) == 6

    providers_present = {d.provider for d in devices}
    assert providers_present == {
        DeviceProvider.FAKE,
        DeviceProvider.LDPLAYER,
        DeviceProvider.MUMU,
    }

    # Verify ID segregation and unique ADB ports
    adb_targets = [d.adb_target for d in devices if d.adb_target]
    assert len(adb_targets) == len(set(adb_targets))

    ld_devs = [d for d in devices if d.provider == DeviceProvider.LDPLAYER]
    assert len(ld_devs) == 2
    assert ld_devs[0].adb_target == "127.0.0.1:5555"
    assert ld_devs[1].adb_target == "127.0.0.1:5557"

    mumu_devs = [d for d in devices if d.provider == DeviceProvider.MUMU]
    assert len(mumu_devs) == 2
    assert mumu_devs[0].adb_target == "127.0.0.1:16384"
    assert mumu_devs[1].adb_target == "127.0.0.1:16416"


def test_provider_calls_overlap(tmp_path: Path) -> None:
    registry, ld_provider, mumu_provider = _build_test_registry(tmp_path)
    registry.discover_all()
    barrier = threading.Barrier(2, timeout=1)
    original_ld_start = ld_provider.start
    original_mumu_start = mumu_provider.start

    def synchronized_ld_start(device_id: str):
        barrier.wait()
        return original_ld_start(device_id)

    def synchronized_mumu_start(device_id: str):
        barrier.wait()
        return original_mumu_start(device_id)

    ld_provider.start = synchronized_ld_start  # type: ignore[method-assign]
    mumu_provider.start = synchronized_mumu_start  # type: ignore[method-assign]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(
            executor.map(registry.start_device, ["ldplayer_0", "mumu_0"])
        )

    assert all(result.success for result in results)


def test_concurrent_device_actions(tmp_path: Path) -> None:
    """Operations across multiple providers execute concurrently without deadlocks."""
    registry, _, _ = _build_test_registry(tmp_path)
    devices = registry.discover_all()

    # Screenshot test path
    shot_dir = tmp_path / "screenshots"
    shot_dir.mkdir(parents=True, exist_ok=True)

    def run_device_action(device_id: str) -> bool:
        dev = registry.get_device(device_id)
        if not dev:
            return False

        # If offline, start it
        if dev.state == DeviceState.OFFLINE:
            res_start = registry.start_device(device_id)
            if not res_start.success:
                return False

        # Take screenshot
        shot_path = shot_dir / f"{device_id}.png"
        res_shot = registry.take_screenshot(device_id, shot_path)
        return res_shot.success

    # Execute actions across all devices simultaneously via thread pool
    dev_ids = [d.id for d in devices]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(run_device_action, dev_ids))

    assert all(results)
    for dev_id in dev_ids:
        assert (shot_dir / f"{dev_id}.png").exists()
