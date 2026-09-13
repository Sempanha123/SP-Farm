"""Unit tests for MuMuManager CLI runner and parsing logic."""

import json
from pathlib import Path

from spfarm.infrastructure.devices.mumu.cli import MuMuManagerRunner
from spfarm.infrastructure.devices.mumu.models import MuMuInstanceInfo


class TestMuMuInstanceInfo:
    """Tests for MuMuInstanceInfo parsing."""

    def test_adb_port_calculation(self) -> None:
        """Port should be 16384 + index * 32."""
        info0 = MuMuInstanceInfo(index=0, title="MuMuPlayer-0", is_running=False, adb_port=16384)
        assert info0.adb_port == 16384
        assert info0.adb_target == "127.0.0.1:16384"
        assert info0.name == "MuMuPlayer-0"

        info1 = MuMuInstanceInfo(index=1, title="MuMuPlayer-1", is_running=False, adb_port=16416)
        assert info1.adb_port == 16416
        assert info1.adb_target == "127.0.0.1:16416"

        info2 = MuMuInstanceInfo(index=2, title="MuMuPlayer-2", is_running=False, adb_port=16448)
        assert info2.adb_port == 16448
        assert info2.adb_target == "127.0.0.1:16448"

    def test_from_json_dict_running(self) -> None:
        data = {
            "index": 0,
            "name": "MuMuPlayer-0",
            "title": "Main Emulator",
            "is_running": True,
            "adb_port": 16384,
            "android_version": "12",
        }
        info = MuMuInstanceInfo.from_dict(data)
        assert info.index == 0
        assert info.name == "MuMuPlayer-0"
        assert info.title == "Main Emulator"
        assert info.is_running is True
        assert info.adb_port == 16384

    def test_from_json_dict_offline(self) -> None:
        data = {
            "index": 1,
            "name": "MuMuPlayer-1",
            "is_running": False,
        }
        info = MuMuInstanceInfo.from_dict(data)
        assert info.index == 1
        assert info.name == "MuMuPlayer-1"
        assert info.is_running is False
        assert info.adb_port == 16416

    def test_from_csv_line(self) -> None:
        line = "0,MuMuPlayer-0,1,16384,12"
        info = MuMuInstanceInfo.from_csv_line(line)
        assert info is not None
        assert info.index == 0
        assert info.name == "MuMuPlayer-0"
        assert info.is_running is True
        assert info.adb_port == 16384

    def test_from_csv_line_invalid(self) -> None:
        assert MuMuInstanceInfo.from_csv_line("") is None
        assert MuMuInstanceInfo.from_csv_line("invalid") is None


class TestMuMuManagerRunner:
    """Tests for MuMuManager CLI runner."""

    def test_is_available_false_when_missing(self, tmp_path: Path) -> None:
        runner = MuMuManagerRunner(custom_install_dir=tmp_path)
        assert runner.is_available is False

    def test_is_available_true_with_mock_exe(self, tmp_path: Path) -> None:
        mock_exe = tmp_path / "MuMuManager.exe"
        mock_exe.touch()
        runner = MuMuManagerRunner(custom_install_dir=tmp_path)
        assert runner.is_available is True
        assert runner.executable_path == mock_exe

    def test_execute_with_mock_executor(self, tmp_path: Path) -> None:
        mock_exe = tmp_path / "MuMuManager.exe"
        mock_exe.touch()

        executed_commands = []

        def mock_exec(args: list[str], cwd: Path | None, timeout: float):
            executed_commands.append((args, cwd, timeout))
            return 0, "OK", ""

        runner = MuMuManagerRunner(custom_install_dir=tmp_path, process_executor=mock_exec)
        code, stdout, stderr = runner.run_raw("api", "-v", "0", "player_state")
        assert code == 0
        assert stdout == "OK"
        assert len(executed_commands) == 1
        assert executed_commands[0][0] == [str(mock_exe), "api", "-v", "0", "player_state"]

    def test_list_instances_json(self, tmp_path: Path) -> None:
        mock_exe = tmp_path / "MuMuManager.exe"
        mock_exe.touch()

        payload = [
            {"index": 0, "name": "MuMuPlayer-0", "is_running": True, "adb_port": 16384},
            {"index": 1, "name": "MuMuPlayer-1", "is_running": False, "adb_port": 16416},
        ]

        def mock_exec(args: list[str], cwd: Path | None, timeout: float):
            return 0, json.dumps(payload), ""

        runner = MuMuManagerRunner(custom_install_dir=tmp_path, process_executor=mock_exec)
        instances = runner.list_instances()
        assert len(instances) == 2
        assert instances[0].index == 0
        assert instances[0].is_running is True
        assert instances[1].index == 1
        assert instances[1].is_running is False

    def test_list_instances_csv_fallback(self, tmp_path: Path) -> None:
        mock_exe = tmp_path / "MuMuManager.exe"
        mock_exe.touch()

        csv_output = "0,MuMuPlayer-0,1,16384\n1,MuMuPlayer-1,0,16416\n"

        def mock_exec(args: list[str], cwd: Path | None, timeout: float):
            return 0, csv_output, ""

        runner = MuMuManagerRunner(custom_install_dir=tmp_path, process_executor=mock_exec)
        instances = runner.list_instances()
        assert len(instances) == 2
        assert instances[0].index == 0
        assert instances[0].is_running is True
        assert instances[1].index == 1
        assert instances[1].is_running is False

    def test_instance_actions(self, tmp_path: Path) -> None:
        mock_exe = tmp_path / "MuMuManager.exe"
        mock_exe.touch()

        called_cmds = []

        def mock_exec(args: list[str], cwd: Path | None, timeout: float):
            called_cmds.append(args[1:])
            return 0, "success", ""

        runner = MuMuManagerRunner(custom_install_dir=tmp_path, process_executor=mock_exec)
        code, out, _ = runner.launch(0)
        assert code == 0

        code, out, _ = runner.close(0)
        assert code == 0

        code, out, _ = runner.restart(0)
        assert code == 0

        code, out, _ = runner.install_app(0, Path("C:/test.apk"))
        assert code == 0

        code, out, _ = runner.run_app(0, "com.facebook.katana")
        assert code == 0

        code, out, _ = runner.stop_app(0, "com.facebook.katana")
        assert code == 0

        code, out, _ = runner.uninstall_app(0, "com.facebook.katana")
        assert code == 0

        assert called_cmds == [
            ["api", "-v", "0", "launch_player"],
            ["api", "-v", "0", "close_player"],
            ["api", "-v", "0", "restart_player"],
            ["api", "-v", "0", "app", "-i", "C:\\test.apk" if "\\" in str(Path("C:/test.apk")) else "C:/test.apk"],
            ["api", "-v", "0", "app", "-l", "com.facebook.katana"],
            ["api", "-v", "0", "app", "-k", "com.facebook.katana"],
            ["api", "-v", "0", "app", "-u", "com.facebook.katana"],
        ]
