"""Secret scanning script for SP-Farm V2.

Scans the repository to ensure no plaintext tokens, private keys, or credentials
are accidentally committed or tracked in version control.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Directories and patterns to ignore
IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "archive",
    "_archive",
    "build",
    "dist",
    "__pycache__",
    "node_modules",
}

IGNORED_FILES = {
    ".env.example",
    "scan_secrets.py",
}

# Regex patterns for detecting common secret leaks
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "Private Key Header",
        re.compile(r"-----BEGIN (?:[A-Z0-9_-]+ )?PRIVATE KEY-----"),
    ),
    (
        "GitHub Personal Access Token",
        re.compile(r"(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36}"),
    ),
    (
        "AWS Access Key ID",
        re.compile(r"\b(AKIA|ABIA|ACCA|ASIA)[A-Z0-9]{16}\b"),
    ),
    (
        "Facebook / Meta Access Token",
        re.compile(r"\bEAACEdEose0cBA[0-9A-Za-z]+\b|\bEAA[A-Za-z0-9]{20,}\b"),
    ),
    (
        "Generic Secret / API Key Assignment",
        re.compile(
            r"""(?i)(?:api_key|access_token|secret_key|password)\s*[:=]\s*["']([A-Za-z0-9_\-\.]{20,})["']"""
        ),
    ),
]

SAFE_SAMPLE_ALLOWLIST = {
    "placeholder",
    "example",
    "test_token",
    "your_secret_here",
    "dummy_secret",
}


def is_allowlisted(value: str) -> bool:
    val_lower = value.lower()
    return any(sample in val_lower for sample in SAFE_SAMPLE_ALLOWLIST)


def scan_file(file_path: Path) -> list[tuple[int, str, str]]:
    """Scan a single file for exposed secrets.

    Returns a list of (line_number, pattern_name, line_snippet).
    """
    findings: list[tuple[int, str, str]] = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for line_num, line in enumerate(content.splitlines(), start=1):
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue

        for rule_name, pattern in SECRET_PATTERNS:
            match = pattern.search(line_clean)
            if match:
                matched_str = match.group(0)
                if not is_allowlisted(matched_str):
                    findings.append((line_num, rule_name, line_clean[:80]))

    return findings


def scan_directory(root_dir: Path) -> list[tuple[Path, int, str, str]]:
    """Recursively scan a directory, skipping ignored trees."""
    all_findings: list[tuple[Path, int, str, str]] = []

    for path in root_dir.rglob("*"):
        if path.is_dir():
            continue
        # Check if any parent part is ignored
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.name in IGNORED_FILES:
            continue
        # Skip binary files by extension
        if path.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".ico",
            ".pdf",
            ".zip",
            ".apk",
            ".pyc",
        }:
            continue

        file_findings = scan_file(path)
        for line_num, rule_name, snippet in file_findings:
            all_findings.append((path, line_num, rule_name, snippet))

    return all_findings


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    print(f"[SP-Farm Secret Scanner] Scanning repository: {repo_root}")
    findings = scan_directory(repo_root)

    if not findings:
        print("[SP-Farm Secret Scanner] PASS: No secrets detected.")
        return 0

    print(f"\n[SP-Farm Secret Scanner] FAIL: Found {len(findings)} potential secret(s):")
    for file_path, line_num, rule_name, snippet in findings:
        rel_path = file_path.relative_to(repo_root)
        print(f"  - {rel_path}:{line_num} [{rule_name}] -> {snippet}")

    print("\nPlease remove or vault these credentials before committing.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
