# Security Policy & Safe Automation Standards

SP-Farm V2 is developed under strict security and legal compliance guidelines.

---

## 1. Safety Boundaries & Anti-Abuse Rules

SP-Farm V2 strictly enforces the following engineering boundaries:

- **Authorized Access Only**: All accounts, Pages, Groups, devices, and campaigns managed by this tool must belong to the operator or be managed with explicit authorization.
- **No Checkpoint or Verification Bypass**: The software will not attempt automated CAPTCHA solving, SMS farm registration, or identity verification bypass.
- **No Hardware Fingerprint Spoofing**: Anti-detection hardware rotation (e.g. generating fake IMEI, MEID, GSF ID, MAC addresses, or Advertising IDs to evade platform security) is strictly forbidden and rejected at the architectural level.
- **No Spam or Mass Engagement Automation**: Features that automate unsolicited direct messages, spam comments, friend requests, or engagement loops are explicitly excluded.

---

## 2. Secret Storage & Credential Vaulting

- **Zero Plaintext Secrets**: Passwords, cookies, session tokens, TOTP secrets, recovery codes, and proxy credentials MUST NOT be stored in plaintext databases or committed to repository files.
- **Secure Secret References**: Domain entities and database records store opaque secret references (e.g., `password_secret_ref`, `cookie_vault_ref`).
- **Encrypted Vaults**: Secrets are stored in OS-level secure credential stores (Windows Credential Manager / DPAPI / Keyring) or encrypted local vaults with restricted file permissions (`chmod 600`).
- **Audit & Masking**: User credentials in UI inspectors are masked by default (`••••••••`). Explicit unmasking or copying actions are temporary and logged to audit trails without ever writing sensitive payloads to disk logs.

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability or potential credential exposure:

1. **Do not create a public issue.**
2. Report the vulnerability privately to the maintainers.
3. Provide reproduction steps, affected code components, and impact analysis.
4. Allow reasonable time for remediation before disclosure.

---

## 4. Secret Hygiene in Commits

Prior to committing any code, run:
```pwsh
python scripts/scan_secrets.py
```
Pre-commit hooks and automated CI checks enforce zero-secret tolerance on all branches and pull requests.
