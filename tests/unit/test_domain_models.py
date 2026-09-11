"""Comprehensive unit tests for pure domain models and state transitions."""

import pytest

from spfarm.domain.accounts.models import (
    Account,
    AccountEmail,
    AccountPhone,
    AccountSecurity,
    Group,
    Page,
)
from spfarm.domain.devices.models import RuntimeDevice
from spfarm.domain.enums import (
    AccountHealthState,
    AccountStatus,
    DeviceProvider,
    DeviceState,
    JobPriority,
    JobStatus,
    TwoFactorMethod,
)
from spfarm.domain.environments.models import AccountEnvironmentProfile
from spfarm.domain.jobs.models import Job
from spfarm.shared.errors import ConflictError, ValidationError


def test_account_creation_and_collections() -> None:
    account = Account(
        profile_id="fb-100234",
        display_name="Operations Alpha",
        status=AccountStatus.ACTIVE,
        health_state=AccountHealthState.HEALTHY,
    )

    # 1. Multiple emails with primary management
    email1 = AccountEmail(account_id=account.id, address="first@example.com", is_primary=True)
    email2 = AccountEmail(account_id=account.id, address="second@example.com", is_primary=True)
    account.add_email(email1)
    account.add_email(email2)

    assert len(account.emails) == 2
    assert account.primary_email.address == "second@example.com"
    assert email1.is_primary is False
    assert email2.is_primary is True

    # 2. Multiple phones with primary management
    phone1 = AccountPhone(account_id=account.id, number="+1234567890", is_primary=True)
    phone2 = AccountPhone(account_id=account.id, number="+1987654321", is_primary=False)
    account.add_phone(phone1)
    account.add_phone(phone2)

    assert len(account.phones) == 2
    assert account.primary_phone.number == "+1234567890"

    # 3. Security secret references
    account.security = AccountSecurity(
        account_id=account.id,
        two_factor_enabled=True,
        two_factor_method=TwoFactorMethod.TOTP,
        password_secret_ref="vault://accounts/acc-01/password",
        totp_secret_ref="vault://accounts/acc-01/totp",
        cookie_vault_ref="vault://accounts/acc-01/cookies",
    )
    assert account.security.two_factor_enabled is True
    assert account.security.password_secret_ref.startswith("vault://")

    # 4. Pages and Groups
    account.pages.append(Page(account_id=account.id, platform_page_id="p-001", name="Page A"))
    account.pages.append(Page(account_id=account.id, platform_page_id="p-002", name="Page B"))
    account.groups.append(Group(account_id=account.id, platform_group_id="g-001", name="Group 1"))

    assert len(account.pages) == 2
    assert len(account.groups) == 1


def test_account_status_transitions() -> None:
    account = Account(profile_id="123", display_name="Test")
    assert account.status == AccountStatus.ACTIVE

    account.set_status(AccountStatus.RESTRICTED)
    assert account.status == AccountStatus.RESTRICTED

    account.set_status(AccountStatus.ARCHIVED)
    assert account.status == AccountStatus.ARCHIVED
    assert account.archived_at is not None

    # Cannot transition archived to restricted without reactivating
    with pytest.raises(ValidationError):
        account.set_status(AccountStatus.RESTRICTED)


def test_environment_profile_and_device_compatibility() -> None:
    env = AccountEnvironmentProfile(
        account_id="acc-uuid",
        label="Facebook Lite Standard",
        preferred_device_provider=DeviceProvider.LDPLAYER,
        preferred_android_version="9.0",
    )

    dev_ldplayer = RuntimeDevice(
        provider=DeviceProvider.LDPLAYER,
        provider_instance_id="ld-01",
        friendly_name="LDPlayer Instance 1",
        adb_target="emulator-5554",
        android_version="9.0",
    )

    dev_mumu = RuntimeDevice(
        provider=DeviceProvider.MUMU,
        provider_instance_id="mumu-01",
        friendly_name="MuMu Instance 1",
        adb_target="127.0.0.1:16384",
        android_version="12.0",
    )

    # Compatible with LDPlayer 9.0
    assert env.is_compatible_with(dev_ldplayer) is True
    # Incompatible with MuMu (preferred provider was LDPLAYER)
    assert env.is_compatible_with(dev_mumu) is False


def test_environment_moves_between_devices() -> None:
    env = AccountEnvironmentProfile(account_id="acc-123")

    dev1 = RuntimeDevice(
        provider=DeviceProvider.LDPLAYER,
        provider_instance_id="ld-01",
        friendly_name="Device 1",
        adb_target="127.0.0.1:5555",
    )
    dev2 = RuntimeDevice(
        provider=DeviceProvider.PHYSICAL_ANDROID,
        provider_instance_id="phys-01",
        friendly_name="Pixel 6",
        adb_target="9889a123",
    )

    assert dev1.is_available is True
    assert dev2.is_available is True

    # 1. Lease Device 1
    lease1 = dev1.reserve(environment_id=env.id, job_id="job-01")
    assert dev1.is_available is False
    assert dev1.state == DeviceState.RESERVED
    assert dev1.current_environment_id == env.id

    # Double reservation fails
    with pytest.raises(ConflictError):
        dev1.reserve(environment_id="other-env")

    # 2. Release Device 1
    dev1.release()
    assert dev1.is_available is True
    assert lease1.is_active is False

    # 3. Environment moves to Device 2
    lease2 = dev2.reserve(environment_id=env.id, job_id="job-02")
    assert dev2.state == DeviceState.RESERVED
    assert dev2.current_environment_id == env.id
    dev2.release()
    assert dev2.is_available is True
    assert lease2.is_active is False


def test_environment_revision_history() -> None:
    env = AccountEnvironmentProfile(account_id="acc-rev")
    assert env.revision == 1

    rev_record = env.bump_revision("Switched locale to fr_FR")
    assert env.revision == 2
    assert rev_record.revision == 2
    assert rev_record.note == "Switched locale to fr_FR"


def test_job_state_lifecycle() -> None:
    job = Job(
        job_type="SYNC_PROFILE",
        target_account_id="acc-01",
        priority=JobPriority.HIGH,
        max_attempts=2,
    )
    assert job.status == JobStatus.PENDING

    # Start attempt 1
    attempt1 = job.start(device_id="dev-01")
    assert job.status == JobStatus.RUNNING
    assert job.attempts == 1
    assert attempt1.attempt_number == 1

    # Attempt 1 fails -> status RETRYING
    job.fail("Network timeout")
    assert job.status == JobStatus.RETRYING
    assert job.can_retry is True

    # Start attempt 2
    job.start()
    assert job.status == JobStatus.RUNNING
    assert job.attempts == 2

    # Attempt 2 succeeds
    job.complete(result_data={"synced_pages": 3})
    assert job.status == JobStatus.COMPLETED
    assert job.progress_pct == 100
    assert job.result_data["synced_pages"] == 3

    # Completed job cannot be cancelled
    with pytest.raises(ValidationError):
        job.cancel()
