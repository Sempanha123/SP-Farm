"""Tests for repository secret scanner."""

from pathlib import Path

from scripts.scan_secrets import is_allowlisted, scan_directory, scan_file


def test_allowlist_matches() -> None:
    assert is_allowlisted("placeholder_key") is True
    assert is_allowlisted("your_secret_here") is True
    assert is_allowlisted("ABCDEFGHIJK123456789") is False


def test_scan_detects_real_looking_secret(tmp_path: Path) -> None:
    bad_file = tmp_path / "leaked.py"
    # Write a simulated fake private key header dynamically to avoid flagging the test file itself
    dummy_key_header = f"-----BEGIN {'RSA'} PRIVATE KEY-----\n"
    bad_file.write_text(f"{dummy_key_header}MIIEowIBAAKCAQEA0...", encoding="utf-8")

    findings = scan_file(bad_file)
    assert len(findings) > 0
    assert findings[0][1] == "Private Key Header"


def test_scan_passes_on_clean_file(tmp_path: Path) -> None:
    clean_file = tmp_path / "clean.py"
    clean_file.write_text("def add(a: int, b: int) -> int:\n    return a + b\n", encoding="utf-8")

    findings = scan_file(clean_file)
    assert len(findings) == 0


def test_repo_scan_has_no_secrets() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    findings = scan_directory(repo_root)
    assert len(findings) == 0, f"Found unexpected secrets in repository: {findings}"
