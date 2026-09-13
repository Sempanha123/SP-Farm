"""Tests for mobile WebDriver primitives."""

from typing import Any, Optional

from spfarm.infrastructure.automation.appium.driver import MobileAutomationDriver


class FakePool:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, Optional[dict[str, Any]]]] = []

    def execute(
        self,
        _lease: object,
        method: str,
        path: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        self.calls.append((method, path, payload))
        if path == "/element":
            return {"value": {"element-6066-11e4-a52e-4f735466cecf": "element-1"}}
        if path == "/source":
            return {"value": "<hierarchy />"}
        if path == "/screenshot":
            return {"value": "iVBORw0KGgo="}
        return {"value": None}


class FakeLease:
    def __init__(self) -> None:
        self.released = False

    def release(self) -> None:
        self.released = True


def test_mobile_driver_primitives() -> None:
    pool = FakePool()
    lease = FakeLease()
    driver = MobileAutomationDriver(pool, lease)  # type: ignore[arg-type]

    element_id = driver.find_element("accessibility id", "Submit")
    driver.click(element_id)
    driver.type_text(element_id, "hello")
    driver.tap(10, 20)
    driver.swipe(10, 20, 10, 200)
    driver.press_back()

    assert element_id == "element-1"
    assert ("POST", "/element/element-1/click", {}) in pool.calls
    assert driver.page_source() == "<hierarchy />"
    assert driver.screenshot().startswith(b"\x89PNG")
    driver.close()
    assert lease.released
