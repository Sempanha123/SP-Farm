# ♡ SP-Farm V2

A modern, robust Windows desktop operations platform for authorized multi-device Android and Facebook account management, Page/Group publishing, campaign orchestration, and automation.

---

## Highlights

- **Cute Productivity Design**: Fresh, cute, and light-first interface using a soothing Sky Blue (`#5B8DEF`), Pastel Pink (`#F38BB7`), and Lavender (`#A894F6`) palette.
- **Decoupled Architecture**: Clean separation between **Runtime Devices** (LDPlayer, MuMu, Physical Android) and **Account Environment Profiles**.
- **No-Restart Companion App Bridge**: Safe environment application without device reboots.
- **Enterprise-Grade Security**: Zero plaintext passwords, cookies, or 2FA keys. Everything is vaulted via OS Keyring/DPAPI or encrypted reference stores.
- **Layered Architecture**: Strict dependency separation: Presentation (PySide6) → Application → Domain → Infrastructure (SQLAlchemy 2, SQLite WAL, ADB, Appium).
- **Persistent Job Engine**: Restart-safe background worker pool with resource-aware concurrency.

---

## Safe Product Boundaries

SP-Farm V2 is built exclusively for authorized account owners and community managers:

### Permitted Capabilities
- Managing accounts, Pages, Groups, and devices owned or authorized by the operator.
- Official Meta Graph API integration.
- Controlled UI automation for authorized management and QA workflows on owned devices.
- Managing approved official Facebook and Facebook Lite APK updates.
- Transparent network profiles (proxy/VPN) and QA/device-lab test location profiles.
- Guided 2FA setup and account health diagnostics.

### Strictly Excluded / Prohibited
- No mass account creation or disposable SMS automation.
- No CAPTCHA or checkpoint bypass mechanisms.
- No anti-detection hardware fingerprint spoofing (IMEI, MEID, GSF, advertising ID rotation).
- No mass-engagement farming (mass likes, unsolicited DMs, spam comments, friend-request harvesting).

---

## Getting Started

### Prerequisites
- Windows 10/11 (64-bit)
- Python 3.13+ (or 3.14 compatible)
- Git

### Installation
```pwsh
git clone https://github.com/Sempanha123/SP-Farm.git
cd SP-Farm
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Running the Application
```pwsh
python -m spfarm
```

### Running Tests and Linters
```pwsh
pytest -v tests/
ruff check src tests
python scripts/scan_secrets.py
```

---

## License & Policies
Please review [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before submitting code.
