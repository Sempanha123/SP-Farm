"""Automated AST-based architectural dependency boundary tests."""

import ast
from pathlib import Path


def get_imports_from_file(file_path: Path) -> list[str]:
    """Parse a python file using AST and return all top-level imported module names."""
    imports: list[str] = []
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))
    except Exception as exc:
        raise RuntimeError(f"Failed to parse {file_path}: {exc}") from exc

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)

    return imports


def test_domain_layer_has_no_forbidden_imports() -> None:
    """Domain layer must not import UI, ORM/SQL, network HTTP, or device libraries."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    domain_dir = repo_root / "src" / "spfarm" / "domain"

    forbidden_prefixes = (
        "PySide6",
        "PyQt5",
        "PyQt6",
        "sqlalchemy",
        "requests",
        "urllib",
        "appium",
        "subprocess",
    )

    violations: list[str] = []
    for py_file in domain_dir.rglob("*.py"):
        imported_modules = get_imports_from_file(py_file)
        for mod in imported_modules:
            for forbidden in forbidden_prefixes:
                if mod == forbidden or mod.startswith(f"{forbidden}."):
                    violations.append(f"{py_file.name} imports forbidden '{mod}'")

    assert not violations, "Domain layer architectural violations found:\n" + "\n".join(violations)


def test_application_layer_has_no_ui_imports() -> None:
    """Application layer must not depend on PySide6 UI or presentation modules."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    app_dir = repo_root / "src" / "spfarm" / "application"

    forbidden_prefixes = (
        "PySide6",
        "PyQt5",
        "PyQt6",
        "spfarm.presentation",
    )

    violations: list[str] = []
    for py_file in app_dir.rglob("*.py"):
        imported_modules = get_imports_from_file(py_file)
        for mod in imported_modules:
            for forbidden in forbidden_prefixes:
                if mod == forbidden or mod.startswith(f"{forbidden}."):
                    violations.append(f"{py_file.name} imports forbidden '{mod}'")

    assert not violations, "Application layer architectural violations found:\n" + "\n".join(violations)


def test_presentation_layer_has_no_direct_sql_or_subprocess() -> None:
    """Presentation layer must not directly import SQLAlchemy, subprocess, or database repositories."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    pres_dir = repo_root / "src" / "spfarm" / "presentation"

    forbidden_prefixes = (
        "sqlalchemy",
        "subprocess",
        "spfarm.infrastructure.database",
    )

    violations: list[str] = []
    for py_file in pres_dir.rglob("*.py"):
        imported_modules = get_imports_from_file(py_file)
        for mod in imported_modules:
            for forbidden in forbidden_prefixes:
                if mod == forbidden or mod.startswith(f"{forbidden}."):
                    violations.append(f"{py_file.name} imports forbidden '{mod}'")

    assert not violations, "Presentation layer architectural violations found:\n" + "\n".join(violations)
