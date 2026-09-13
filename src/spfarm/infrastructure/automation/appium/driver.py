"""Small WebDriver primitive set backed by a device session lease."""

from __future__ import annotations

from typing import Any

from spfarm.infrastructure.automation.sessions.pool import (
    AppiumSessionLease,
    AppiumSessionPool,
)


class MobileAutomationDriver:
    def __init__(self, pool: AppiumSessionPool, lease: AppiumSessionLease) -> None:
        self.pool = pool
        self.lease = lease

    def find_element(self, strategy: str, value: str) -> str:
        body = self.pool.execute(
            self.lease,
            "POST",
            "/element",
            {"using": strategy, "value": value},
        )
        element = body.get("value", {})
        element_id = element.get("element-6066-11e4-a52e-4f735466cecf") or element.get(
            "ELEMENT"
        )
        if not element_id:
            raise RuntimeError("Appium did not return an element ID")
        return str(element_id)

    def click(self, element_id: str) -> None:
        self.pool.execute(self.lease, "POST", f"/element/{element_id}/click", {})

    def type_text(self, element_id: str, text: str) -> None:
        self.pool.execute(
            self.lease,
            "POST",
            f"/element/{element_id}/value",
            {"text": text, "value": list(text)},
        )

    def tap(self, x: int, y: int) -> None:
        self._perform_actions(
            [
                {"type": "pointerMove", "duration": 0, "x": x, "y": y},
                {"type": "pointerDown", "button": 0},
                {"type": "pointerUp", "button": 0},
            ]
        )

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration_ms: int = 500,
    ) -> None:
        self._perform_actions(
            [
                {"type": "pointerMove", "duration": 0, "x": start_x, "y": start_y},
                {"type": "pointerDown", "button": 0},
                {
                    "type": "pointerMove",
                    "duration": duration_ms,
                    "x": end_x,
                    "y": end_y,
                },
                {"type": "pointerUp", "button": 0},
            ]
        )

    def press_back(self) -> None:
        self.pool.execute(self.lease, "POST", "/back", {})

    def screenshot(self) -> bytes:
        import base64

        body = self.pool.execute(self.lease, "GET", "/screenshot")
        return base64.b64decode(body.get("value", ""), validate=True)

    def page_source(self) -> str:
        body = self.pool.execute(self.lease, "GET", "/source")
        return str(body.get("value", ""))

    def close(self) -> None:
        self.lease.release()

    def _perform_actions(self, actions: list[dict[str, Any]]) -> None:
        self.pool.execute(
            self.lease,
            "POST",
            "/actions",
            {
                "actions": [
                    {
                        "type": "pointer",
                        "id": "finger1",
                        "parameters": {"pointerType": "touch"},
                        "actions": actions,
                    }
                ]
            },
        )
