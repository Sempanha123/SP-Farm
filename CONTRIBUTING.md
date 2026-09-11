# Contributing to SP-Farm V2

Thank you for contributing to SP-Farm V2! Please adhere to the guidelines below to maintain clean architecture and code quality.

---

## 1. Branching Strategy

- `main`: Production-ready, stable releases.
- `develop`: Primary integration branch for completed phases.
- `phase/XX-<name>`: Work branch dedicated to a specific development phase (e.g. `phase/01-clean-repository-and-security-reset`).
- `feature/<name>` / `fix/<name>`: Focused features or bug fixes branching off `develop`.

---

## 2. Architectural Principles

1. **Strict Layering**:
   - `presentation/`: PySide6 views, models, and widgets. Absolutely no database, subprocess, or network operations.
   - `application/`: Commands, queries, workflows, and orchestrators.
   - `domain/`: Business entities and logic. Independent of UI frameworks or infrastructure libraries.
   - `infrastructure/`: Implementations for databases (SQLAlchemy), device drivers (ADB, Appium), APIs, and secrets.
   - `workers/`: Background supervisors and async job processing.
2. **Asynchronous Execution**: Every long-running operation must execute off the Qt main UI thread using workers and signals.
3. **Typing & Linting**: All code must include type hints and pass Ruff checks.
4. **Path Handling**: Always use `pathlib.Path`, never hardcoded Windows slash strings. All paths must be configurable.

---

## 3. Local Development Workflow

### Setup
```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pre-commit install
```

### Pre-commit Verification
Before opening a pull request or merging a phase:
```pwsh
# 1. Check linting and formatting
ruff check src tests

# 2. Run test suite
pytest -v tests/

# 3. Verify no secrets are exposed
python scripts/scan_secrets.py

# 4. Check git status for unintended files
git status
```
