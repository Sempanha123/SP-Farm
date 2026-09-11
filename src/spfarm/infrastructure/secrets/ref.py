"""Secret reference (URI) formatting and parsing helpers."""

from __future__ import annotations

import re

VAULT_SCHEME = "vault://"
REF_REGEX = re.compile(r"^vault://([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-]+)/([a-zA-Z0-9_\-]+)$")


def make_secret_ref(category: str, entity_id: str, key_name: str) -> str:
    """Construct a canonical secret reference URI.

    Example:
        make_secret_ref("accounts", "acc_123", "password")
        -> "vault://accounts/acc_123/password"
    """
    cat = category.strip("/").lower()
    eid = entity_id.strip("/")
    k = key_name.strip("/").lower()
    return f"{VAULT_SCHEME}{cat}/{eid}/{k}"


def parse_secret_ref(ref: str) -> tuple[str, str, str]:
    """Parse a canonical secret reference URI into (category, entity_id, key_name).

    Raises:
        ValueError: If the ref does not conform to vault://<category>/<entity_id>/<key_name>
    """
    match = REF_REGEX.match(ref.strip())
    if not match:
        raise ValueError(
            f"Invalid secret reference: '{ref}'. Expected format: vault://<category>/<entity_id>/<key_name>"
        )
    return match.group(1), match.group(2), match.group(3)


def is_secret_ref(val: str) -> bool:
    """Check whether a given string is a valid secret reference URI."""
    if not isinstance(val, str):
        return False
    return bool(REF_REGEX.match(val.strip()))
