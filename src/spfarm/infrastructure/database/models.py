"""Normalized SQLAlchemy 2 declarative models."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


class AccountModel(Base):
    """Normalized accounts table."""

    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    platform: Mapped[str] = mapped_column(String(32), default="FACEBOOK", nullable=False)
    profile_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(128))
    middle_name: Mapped[Optional[str]] = mapped_column(String(128))
    last_name: Mapped[Optional[str]] = mapped_column(String(128))
    username: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    profile_url: Mapped[Optional[str]] = mapped_column(String(512))
    avatar_asset_id: Mapped[Optional[str]] = mapped_column(String(36))
    birthday: Mapped[Optional[str]] = mapped_column(String(32))
    gender_optional: Mapped[Optional[str]] = mapped_column(String(32))
    country: Mapped[Optional[str]] = mapped_column(String(64))
    city: Mapped[Optional[str]] = mapped_column(String(64))
    language: Mapped[str] = mapped_column(String(16), default="en")
    locale: Mapped[str] = mapped_column(String(16), default="en_US")
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", index=True)
    health_state: Mapped[str] = mapped_column(String(32), default="HEALTHY")
    priority: Mapped[int] = mapped_column(Integer, default=0)
    workspace_id: Mapped[Optional[str]] = mapped_column(String(36))
    category_id: Mapped[Optional[str]] = mapped_column(String(36))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    imported_at: Mapped[Optional[str]] = mapped_column(String(64))
    last_synced_at: Mapped[Optional[str]] = mapped_column(String(64))
    last_activity_at: Mapped[Optional[str]] = mapped_column(String(64))
    archived_at: Mapped[Optional[str]] = mapped_column(String(64))

    # Child relationships
    emails: Mapped[list[AccountEmailModel]] = relationship(
        "AccountEmailModel", back_populates="account", cascade="all, delete-orphan"
    )
    phones: Mapped[list[AccountPhoneModel]] = relationship(
        "AccountPhoneModel", back_populates="account", cascade="all, delete-orphan"
    )
    security: Mapped[Optional[AccountSecurityModel]] = relationship(
        "AccountSecurityModel",
        back_populates="account",
        uselist=False,
        cascade="all, delete-orphan",
    )
    pages: Mapped[list[PageModel]] = relationship(
        "PageModel", back_populates="account", cascade="all, delete-orphan"
    )
    groups: Mapped[list[GroupModel]] = relationship(
        "GroupModel", back_populates="account", cascade="all, delete-orphan"
    )
    environments: Mapped[list[AccountEnvironmentProfileModel]] = relationship(
        "AccountEnvironmentProfileModel", back_populates="account", cascade="all, delete-orphan"
    )


class AccountEmailModel(Base):
    """Normalized account emails table."""

    __tablename__ = "account_emails"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    label: Mapped[str] = mapped_column(String(64), default="personal")
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    added_at: Mapped[str] = mapped_column(String(64), nullable=False)
    last_checked_at: Mapped[Optional[str]] = mapped_column(String(64))

    account: Mapped[AccountModel] = relationship("AccountModel", back_populates="emails")


class AccountPhoneModel(Base):
    """Normalized account phone numbers table."""

    __tablename__ = "account_phones"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )
    number: Mapped[str] = mapped_column(String(64), nullable=False)
    country: Mapped[str] = mapped_column(String(16), default="US")
    label: Mapped[str] = mapped_column(String(64), default="mobile")
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    added_at: Mapped[str] = mapped_column(String(64), nullable=False)
    last_checked_at: Mapped[Optional[str]] = mapped_column(String(64))

    account: Mapped[AccountModel] = relationship("AccountModel", back_populates="phones")


class AccountSecurityModel(Base):
    """Normalized account security table storing vault references only (no raw credentials)."""

    __tablename__ = "account_security"

    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True
    )
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    two_factor_method: Mapped[str] = mapped_column(String(32), default="NONE")
    recovery_email_status: Mapped[str] = mapped_column(String(64), default="unknown")
    recovery_phone_status: Mapped[str] = mapped_column(String(64), default="unknown")
    manual_review_required: Mapped[bool] = mapped_column(Boolean, default=False)
    restriction_state: Mapped[Optional[str]] = mapped_column(String(64))
    last_security_review_at: Mapped[Optional[str]] = mapped_column(String(64))

    # Secret references (opaque tokens pointing to OS keyring/DPAPI)
    password_secret_ref: Mapped[Optional[str]] = mapped_column(String(255))
    totp_secret_ref: Mapped[Optional[str]] = mapped_column(String(255))
    recovery_codes_secret_ref: Mapped[Optional[str]] = mapped_column(String(255))
    cookie_vault_ref: Mapped[Optional[str]] = mapped_column(String(255))
    session_vault_ref: Mapped[Optional[str]] = mapped_column(String(255))
    access_token_secret_ref: Mapped[Optional[str]] = mapped_column(String(255))
    session_updated_at: Mapped[Optional[str]] = mapped_column(String(64))

    account: Mapped[AccountModel] = relationship("AccountModel", back_populates="security")


class PageModel(Base):
    """Normalized Facebook pages table."""

    __tablename__ = "pages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )
    platform_page_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(128), default="General")
    profile_url: Mapped[Optional[str]] = mapped_column(String(512))
    followers: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    publishing_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    last_synced_at: Mapped[Optional[str]] = mapped_column(String(64))
    last_published_at: Mapped[Optional[str]] = mapped_column(String(64))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    account: Mapped[AccountModel] = relationship("AccountModel", back_populates="pages")


class GroupModel(Base):
    """Normalized Facebook groups table."""

    __tablename__ = "groups"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )
    platform_group_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(64), default="MEMBER")
    members: Mapped[int] = mapped_column(Integer, default=0)
    posting_permission: Mapped[str] = mapped_column(String(64), default="ALLOWED")
    last_synced_at: Mapped[Optional[str]] = mapped_column(String(64))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    account: Mapped[AccountModel] = relationship("AccountModel", back_populates="groups")


class AccountEnvironmentProfileModel(Base):
    """Normalized account environment profiles table."""

    __tablename__ = "account_environments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )
    label: Mapped[str] = mapped_column(String(128), default="Default Environment")
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE")
    revision: Mapped[int] = mapped_column(Integer, default=1)
    preferred_device_provider: Mapped[Optional[str]] = mapped_column(String(32))
    preferred_android_version: Mapped[Optional[str]] = mapped_column(String(32))
    app_channel: Mapped[str] = mapped_column(String(128), default="com.facebook.katana")
    app_package: Mapped[str] = mapped_column(String(128), default="com.facebook.katana")
    app_version: Mapped[Optional[str]] = mapped_column(String(64))
    locale: Mapped[str] = mapped_column(String(32), default="en_US")
    language: Mapped[str] = mapped_column(String(16), default="en")
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    screen_width: Mapped[int] = mapped_column(Integer, default=720)
    screen_height: Mapped[int] = mapped_column(Integer, default=1280)
    density_dpi: Mapped[int] = mapped_column(Integer, default=320)
    orientation: Mapped[str] = mapped_column(String(32), default="portrait")
    network_profile_id: Mapped[Optional[str]] = mapped_column(String(36))
    location_profile_id: Mapped[Optional[str]] = mapped_column(String(36))
    permission_profile_id: Mapped[Optional[str]] = mapped_column(String(36))
    notification_profile_id: Mapped[Optional[str]] = mapped_column(String(36))
    storage_profile_id: Mapped[Optional[str]] = mapped_column(String(36))
    session_vault_ref: Mapped[Optional[str]] = mapped_column(String(255))
    app_state_backup_ref: Mapped[Optional[str]] = mapped_column(String(255))
    last_runtime_device_id: Mapped[Optional[str]] = mapped_column(String(36))
    last_restored_at: Mapped[Optional[str]] = mapped_column(String(64))
    last_backup_at: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(64), nullable=False)

    account: Mapped[AccountModel] = relationship("AccountModel", back_populates="environments")


class RuntimeDeviceModel(Base):
    """Normalized runtime devices table."""

    __tablename__ = "runtime_devices"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    provider: Mapped[str] = mapped_column(String(32), nullable=False)
    provider_instance_id: Mapped[str] = mapped_column(String(128), nullable=False)
    friendly_name: Mapped[str] = mapped_column(String(128), nullable=False)
    adb_target: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    android_version: Mapped[str] = mapped_column(String(32), default="12")
    manufacturer_display: Mapped[str] = mapped_column(String(64), default="Android")
    model_display: Mapped[str] = mapped_column(String(64), default="Generic Device")
    state: Mapped[str] = mapped_column(String(32), default="READY", index=True)
    health: Mapped[str] = mapped_column(String(32), default="HEALTHY")
    capabilities_json: Mapped[Optional[str]] = mapped_column(Text)
    current_job_id: Mapped[Optional[str]] = mapped_column(String(36))
    current_environment_id: Mapped[Optional[str]] = mapped_column(String(36))
    last_seen_at: Mapped[str] = mapped_column(String(64), nullable=False)


class RuntimeHistoryModel(Base):
    """Normalized runtime execution history log."""

    __tablename__ = "runtime_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )
    environment_id: Mapped[str] = mapped_column(String(36), nullable=False)
    device_id: Mapped[str] = mapped_column(String(36), nullable=False)
    job_id: Mapped[Optional[str]] = mapped_column(String(36))
    started_at: Mapped[str] = mapped_column(String(64), nullable=False)
    ended_at: Mapped[Optional[str]] = mapped_column(String(64))
    result_state: Mapped[str] = mapped_column(String(32), default="SUCCESS")
    app_version: Mapped[Optional[str]] = mapped_column(String(64))
    network_profile_id: Mapped[Optional[str]] = mapped_column(String(36))
    notes: Mapped[Optional[str]] = mapped_column(Text)


class JobModel(Base):
    """Normalized background jobs table."""

    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    job_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target_account_id: Mapped[Optional[str]] = mapped_column(String(36), index=True)
    target_device_id: Mapped[Optional[str]] = mapped_column(String(36))
    target_environment_id: Mapped[Optional[str]] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(String(32), default="PENDING", index=True)
    priority: Mapped[str] = mapped_column(String(32), default="NORMAL")
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    progress_pct: Mapped[int] = mapped_column(Integer, default=0)
    payload_json: Mapped[Optional[str]] = mapped_column(Text)
    result_data_json: Mapped[Optional[str]] = mapped_column(Text)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    started_at: Mapped[Optional[str]] = mapped_column(String(64))
    completed_at: Mapped[Optional[str]] = mapped_column(String(64))
