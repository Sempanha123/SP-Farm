"""Account domain models and aggregate entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from spfarm.domain.enums import AccountHealthState, AccountStatus, TwoFactorMethod
from spfarm.shared.errors import ValidationError
from spfarm.shared.ids import generate_id
from spfarm.shared.time import format_iso, utcnow


@dataclass(kw_only=True)
class AccountEmail:
    """An email address associated with an account."""

    id: str = field(default_factory=generate_id)
    account_id: str
    address: str
    label: str = "personal"
    is_primary: bool = False
    is_verified: bool = False
    added_at: str = field(default_factory=format_iso)
    last_checked_at: Optional[str] = None


@dataclass(kw_only=True)
class AccountPhone:
    """A phone number associated with an account."""

    id: str = field(default_factory=generate_id)
    account_id: str
    number: str
    country: str = "US"
    label: str = "mobile"
    is_primary: bool = False
    is_verified: bool = False
    added_at: str = field(default_factory=format_iso)
    last_checked_at: Optional[str] = None


@dataclass(kw_only=True)
class AccountSecurity:
    """Security, 2FA, and vaulted secret references for an account.

    Zero raw credentials: only secret vault references are stored.
    """

    account_id: str
    two_factor_enabled: bool = False
    two_factor_method: TwoFactorMethod = TwoFactorMethod.NONE
    recovery_email_status: str = "unknown"
    recovery_phone_status: str = "unknown"
    manual_review_required: bool = False
    restriction_state: Optional[str] = None
    last_security_review_at: Optional[str] = None

    # Secret references (never raw values)
    password_secret_ref: Optional[str] = None
    totp_secret_ref: Optional[str] = None
    recovery_codes_secret_ref: Optional[str] = None
    cookie_vault_ref: Optional[str] = None
    session_vault_ref: Optional[str] = None
    access_token_secret_ref: Optional[str] = None
    session_updated_at: Optional[str] = None


@dataclass(kw_only=True)
class Page:
    """A Facebook Page managed by an account."""

    id: str = field(default_factory=generate_id)
    account_id: str
    platform_page_id: str
    name: str
    category: str = "General"
    profile_url: Optional[str] = None
    followers: int = 0
    status: str = "ACTIVE"
    publishing_enabled: bool = True
    last_synced_at: Optional[str] = None
    last_published_at: Optional[str] = None
    notes: Optional[str] = None


@dataclass(kw_only=True)
class Group:
    """A Facebook Group managed by or joined by an account."""

    id: str = field(default_factory=generate_id)
    account_id: str
    platform_group_id: str
    name: str
    role: str = "MEMBER"  # ADMIN, MODERATOR, MEMBER
    members: int = 0
    posting_permission: str = "ALLOWED"  # ALLOWED, PENDING_APPROVAL, MUTED
    last_synced_at: Optional[str] = None
    notes: Optional[str] = None


@dataclass(kw_only=True)
class Account:
    """Account root entity."""

    id: str = field(default_factory=generate_id)
    platform: str = "FACEBOOK"
    profile_id: str
    display_name: str
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    profile_url: Optional[str] = None
    avatar_asset_id: Optional[str] = None
    birthday: Optional[str] = None
    gender_optional: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    language: str = "en"
    locale: str = "en_US"
    timezone: str = "UTC"
    status: AccountStatus = AccountStatus.ACTIVE
    health_state: AccountHealthState = AccountHealthState.HEALTHY
    priority: int = 0
    workspace_id: Optional[str] = None
    category_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = field(default_factory=format_iso)
    imported_at: Optional[str] = None
    last_synced_at: Optional[str] = None
    last_activity_at: Optional[str] = None
    archived_at: Optional[str] = None

    # Child collections
    emails: list[AccountEmail] = field(default_factory=list)
    phones: list[AccountPhone] = field(default_factory=list)
    security: Optional[AccountSecurity] = None
    pages: list[Page] = field(default_factory=list)
    groups: list[Group] = field(default_factory=list)

    def add_email(self, email: AccountEmail) -> None:
        """Add an email, ensuring primary uniqueness."""
        if email.is_primary:
            for em in self.emails:
                em.is_primary = False
        elif not self.emails:
            email.is_primary = True
        self.emails.append(email)

    def add_phone(self, phone: AccountPhone) -> None:
        """Add a phone, ensuring primary uniqueness."""
        if phone.is_primary:
            for ph in self.phones:
                ph.is_primary = False
        elif not self.phones:
            phone.is_primary = True
        self.phones.append(phone)

    @property
    def primary_email(self) -> Optional[AccountEmail]:
        for em in self.emails:
            if em.is_primary:
                return em
        return self.emails[0] if self.emails else None

    @property
    def primary_phone(self) -> Optional[AccountPhone]:
        for ph in self.phones:
            if ph.is_primary:
                return ph
        return self.phones[0] if self.phones else None

    def set_status(self, new_status: AccountStatus) -> None:
        """Validate and apply a status transition."""
        if self.status == AccountStatus.ARCHIVED and new_status != AccountStatus.ACTIVE:
            raise ValidationError(f"Cannot transition archived account to {new_status}")

        if new_status == AccountStatus.ARCHIVED:
            self.archived_at = format_iso(utcnow())

        self.status = new_status
