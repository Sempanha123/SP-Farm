"""Unit tests for LDPlayer CLI runner and instance models."""

from __future__ import annotations

from pathlib import Path

from spfarm.infrastructure.devices.ldplayer.cli import LDConsoleRunner
from spfarm.infrastructure.devices.ldplayer.models import LDInstanceInfo


def test_ld_instance_info_parser() -> None:
    """LDInstanceInfo accurately parses standard ldconsole list2 format."""
    raw_sample = """
    0,LDPlayer,0,0,0,0,0
    1,Worker-01,123456,654321,1,2345,6789
    2,Worker-02,0,0,0,0,0
    """
    instances = LDInstanceInfo.parse_list2_output(raw_sample)
    assert len(instances) == 3

    inst0 = instances[0]
    assert inst0.index == 0
    assert inst0.title == "LDPlayer"
    assert inst0.android_started is False
    assert inst0.adb_port == 5555
    assert inst0.adb_target == "127.0.0.1:5555"

    inst1 = instances[1]
    assert inst1.index == 1
    assert inst1.title == "Worker-01"
    assert inst1.android_started is True
    assert inst1.top_hwnd == 123456
    assert inst1.adb_port == 5557
    assert inst1.adb_target == "127.0.0.1:5557"


def test_ld_console_runner_missing_executable() -> None:
    """When LDPlayer is not installed, runner gracefully reports unavailable."""
    runner = LDConsoleRunner(custom_install_dir=Path(r"C:\NonExistent\Path\LDPlayer"))
    assert runner.is_available is False
    assert runner.list2() == []
    code, _, err = runner.launch(0)
    assert code == -1
    assert "not found" in err


def test_ld_console_runner_with_mock_executor(tmp_path: Path) -> None:
    """Runner commands invoke the process executor with exact CLI arguments."""
    # Create a fake executable file in tmp_path
    mock_exe = tmp_path / "ldconsole.exe"
    mock_exe.write_text("fake binary")

    executed_calls: list[list[str]] = []

    def mock_executor(args: list[str], cwd: Path | None, timeout: float) -> tuple[int, str, str]:
        executed_calls.append(args)
        cmd_name = args[1] if len(args) > 1 else ""

        if cmd_name == "list2":
            return 0, "0,LDPlayer,0,0,0,0,0\n1,Worker-01,100,200,1,300,400\n", ""
        if cmd_name == "isrunning":
            return 0, "running\n", ""
        return 0, "OK\n", ""

    runner = LDConsoleRunner(custom_install_dir=tmp_path, process_executor=mock_executor)
    assert runner.is_available is True

    # 1. list2
    instances = runner.list2()
    assert len(instances) == 2
    assert any(call[1] == "list2" for call in executed_calls)

    # 2. launch
    code, out, _ = runner.launch(1)
    assert code == 0
    assert any("launch" in call and "--index" in call and "1" in call for call in executed_calls)

    # 3. quit
    code, out, _ = runner.quit(1)
    assert code == 0
    assert any("quit" in call and "--index" in call and "1" in call for call in executed_calls)

    # 4. reboot
    code, out, _ = runner.reboot(1)
    assert code == 0
    assert any("reboot" in call for call in executed_calls)

    # 5. installapp
    mock_apk = tmp_path / "test.apk"
    mock_apk.write_text("payload")
    code, out, _ = runner.install_app(1, mock_apk)
    assert code == 0
    assert any("installapp" in call for call in executed_calls)

    # 6. runapp / killapp / uninstallapp
    runner.run_app(1, "com.facebook.katana")
    assert any("runapp" in call for call in executed_calls)

    runner.kill_app(1, "com.facebook.katana")
    assert any("killapp" in call for call in executed_calls)

    runner.uninstall_app(1, "com.facebook.katana")
    assert any("uninstallapp" in call for call in executed_calls)

    # 7. sort_windows
    runner.sort_windows()
    assert any("sortWnd" in call for call in executed_calls)
