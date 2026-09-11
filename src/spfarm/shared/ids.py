"""UUID identifier utilities."""

import uuid


def generate_id() -> str:
    """Generate a random UUIDv4 string."""
    return str(uuid.uuid4())


def is_valid_uuid(val: str) -> bool:
    """Check if a string represents a valid UUID."""
    try:
        uuid_obj = uuid.UUID(val)
        return str(uuid_obj) == val.lower()
    except (ValueError, AttributeError, TypeError):
        return False
