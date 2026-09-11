"""Initial schema migration for SP-Farm V2 normalized tables.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-09-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Accounts
    op.create_table(
        "accounts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("platform", sa.String(length=32), nullable=False),
        sa.Column("profile_id", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=128), nullable=True),
        sa.Column("middle_name", sa.String(length=128), nullable=True),
        sa.Column("last_name", sa.String(length=128), nullable=True),
        sa.Column("username", sa.String(length=128), nullable=True),
        sa.Column("profile_url", sa.String(length=512), nullable=True),
        sa.Column("avatar_asset_id", sa.String(length=36), nullable=True),
        sa.Column("birthday", sa.String(length=32), nullable=True),
        sa.Column("gender_optional", sa.String(length=32), nullable=True),
        sa.Column("country", sa.String(length=64), nullable=True),
        sa.Column("city", sa.String(length=64), nullable=True),
        sa.Column("language", sa.String(length=16), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("health_state", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=True),
        sa.Column("category_id", sa.String(length=36), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.String(length=64), nullable=False),
        sa.Column("imported_at", sa.String(length=64), nullable=True),
        sa.Column("last_synced_at", sa.String(length=64), nullable=True),
        sa.Column("last_activity_at", sa.String(length=64), nullable=True),
        sa.Column("archived_at", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_accounts_profile_id", "accounts", ["profile_id"], unique=True)
    op.create_index("ix_accounts_username", "accounts", ["username"], unique=False)
    op.create_index("ix_accounts_status", "accounts", ["status"], unique=False)

    # 2. Account Emails
    op.create_table(
        "account_emails",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("label", sa.String(length=64), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("added_at", sa.String(length=64), nullable=False),
        sa.Column("last_checked_at", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_account_emails_account_id", "account_emails", ["account_id"], unique=False)

    # 3. Account Phones
    op.create_table(
        "account_phones",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("number", sa.String(length=64), nullable=False),
        sa.Column("country", sa.String(length=16), nullable=False),
        sa.Column("label", sa.String(length=64), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("added_at", sa.String(length=64), nullable=False),
        sa.Column("last_checked_at", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_account_phones_account_id", "account_phones", ["account_id"], unique=False)

    # 4. Account Security
    op.create_table(
        "account_security",
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("two_factor_enabled", sa.Boolean(), nullable=False),
        sa.Column("two_factor_method", sa.String(length=32), nullable=False),
        sa.Column("recovery_email_status", sa.String(length=64), nullable=False),
        sa.Column("recovery_phone_status", sa.String(length=64), nullable=False),
        sa.Column("manual_review_required", sa.Boolean(), nullable=False),
        sa.Column("restriction_state", sa.String(length=64), nullable=True),
        sa.Column("last_security_review_at", sa.String(length=64), nullable=True),
        sa.Column("password_secret_ref", sa.String(length=255), nullable=True),
        sa.Column("totp_secret_ref", sa.String(length=255), nullable=True),
        sa.Column("recovery_codes_secret_ref", sa.String(length=255), nullable=True),
        sa.Column("cookie_vault_ref", sa.String(length=255), nullable=True),
        sa.Column("session_vault_ref", sa.String(length=255), nullable=True),
        sa.Column("access_token_secret_ref", sa.String(length=255), nullable=True),
        sa.Column("session_updated_at", sa.String(length=64), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("account_id"),
    )

    # 5. Pages
    op.create_table(
        "pages",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("platform_page_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=128), nullable=False),
        sa.Column("profile_url", sa.String(length=512), nullable=True),
        sa.Column("followers", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("publishing_enabled", sa.Boolean(), nullable=False),
        sa.Column("last_synced_at", sa.String(length=64), nullable=True),
        sa.Column("last_published_at", sa.String(length=64), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_pages_account_id", "pages", ["account_id"], unique=False)
    op.create_index("ix_pages_platform_page_id", "pages", ["platform_page_id"], unique=False)

    # 6. Groups
    op.create_table(
        "groups",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("platform_group_id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=64), nullable=False),
        sa.Column("members", sa.Integer(), nullable=False),
        sa.Column("posting_permission", sa.String(length=64), nullable=False),
        sa.Column("last_synced_at", sa.String(length=64), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_groups_account_id", "groups", ["account_id"], unique=False)
    op.create_index("ix_groups_platform_group_id", "groups", ["platform_group_id"], unique=False)

    # 7. Account Environments
    op.create_table(
        "account_environments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("label", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("preferred_device_provider", sa.String(length=32), nullable=True),
        sa.Column("preferred_android_version", sa.String(length=32), nullable=True),
        sa.Column("app_channel", sa.String(length=128), nullable=False),
        sa.Column("app_package", sa.String(length=128), nullable=False),
        sa.Column("app_version", sa.String(length=64), nullable=True),
        sa.Column("locale", sa.String(length=32), nullable=False),
        sa.Column("language", sa.String(length=16), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.Column("screen_width", sa.Integer(), nullable=False),
        sa.Column("screen_height", sa.Integer(), nullable=False),
        sa.Column("density_dpi", sa.Integer(), nullable=False),
        sa.Column("orientation", sa.String(length=32), nullable=False),
        sa.Column("network_profile_id", sa.String(length=36), nullable=True),
        sa.Column("location_profile_id", sa.String(length=36), nullable=True),
        sa.Column("permission_profile_id", sa.String(length=36), nullable=True),
        sa.Column("notification_profile_id", sa.String(length=36), nullable=True),
        sa.Column("storage_profile_id", sa.String(length=36), nullable=True),
        sa.Column("session_vault_ref", sa.String(length=255), nullable=True),
        sa.Column("app_state_backup_ref", sa.String(length=255), nullable=True),
        sa.Column("last_runtime_device_id", sa.String(length=36), nullable=True),
        sa.Column("last_restored_at", sa.String(length=64), nullable=True),
        sa.Column("last_backup_at", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.String(length=64), nullable=False),
        sa.Column("updated_at", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_account_environments_account_id", "account_environments", ["account_id"], unique=False)

    # 8. Runtime Devices
    op.create_table(
        "runtime_devices",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("provider_instance_id", sa.String(length=128), nullable=False),
        sa.Column("friendly_name", sa.String(length=128), nullable=False),
        sa.Column("adb_target", sa.String(length=128), nullable=False),
        sa.Column("android_version", sa.String(length=32), nullable=False),
        sa.Column("manufacturer_display", sa.String(length=64), nullable=False),
        sa.Column("model_display", sa.String(length=64), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("health", sa.String(length=32), nullable=False),
        sa.Column("capabilities_json", sa.Text(), nullable=True),
        sa.Column("current_job_id", sa.String(length=36), nullable=True),
        sa.Column("current_environment_id", sa.String(length=36), nullable=True),
        sa.Column("last_seen_at", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("adb_target"),
    )
    op.create_index("ix_runtime_devices_state", "runtime_devices", ["state"], unique=False)

    # 9. Runtime History
    op.create_table(
        "runtime_history",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("account_id", sa.String(length=36), nullable=False),
        sa.Column("environment_id", sa.String(length=36), nullable=False),
        sa.Column("device_id", sa.String(length=36), nullable=False),
        sa.Column("job_id", sa.String(length=36), nullable=True),
        sa.Column("started_at", sa.String(length=64), nullable=False),
        sa.Column("ended_at", sa.String(length=64), nullable=True),
        sa.Column("result_state", sa.String(length=32), nullable=False),
        sa.Column("app_version", sa.String(length=64), nullable=True),
        sa.Column("network_profile_id", sa.String(length=36), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_runtime_history_account_id", "runtime_history", ["account_id"], unique=False)

    # 10. Jobs
    op.create_table(
        "jobs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("job_type", sa.String(length=64), nullable=False),
        sa.Column("target_account_id", sa.String(length=36), nullable=True),
        sa.Column("target_device_id", sa.String(length=36), nullable=True),
        sa.Column("target_environment_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.String(length=32), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("progress_pct", sa.Integer(), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=True),
        sa.Column("result_data_json", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.String(length=64), nullable=False),
        sa.Column("started_at", sa.String(length=64), nullable=True),
        sa.Column("completed_at", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_jobs_target_account_id", "jobs", ["target_account_id"], unique=False)
    op.create_index("ix_jobs_status", "jobs", ["status"], unique=False)


def downgrade() -> None:
    op.drop_table("jobs")
    op.drop_table("runtime_history")
    op.drop_table("runtime_devices")
    op.drop_table("account_environments")
    op.drop_table("groups")
    op.drop_table("pages")
    op.drop_table("account_security")
    op.drop_table("account_phones")
    op.drop_table("account_emails")
    op.drop_table("accounts")
