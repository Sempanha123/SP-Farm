"""Unit tests for AccountQueryService."""

from __future__ import annotations

from unittest.mock import MagicMock

from spfarm.application.queries.accounts import (
    AccountFilterCriteria,
    AccountQueryService,
    mask_email,
    mask_phone,
)
from spfarm.domain.accounts.models import (
    Account,
    AccountEmail,
    AccountPhone,
    AccountSecurity,
    Group,
    Page,
)
from spfarm.domain.enums import AccountHealthState, AccountStatus, TwoFactorMethod


def test_mask_email_and_phone():
    assert mask_email("johndoe@example.com") == "j***e@example.com"
    assert mask_email("a@b.com") == "a***@b.com"
    assert mask_email(None) == "—"

    assert mask_phone("+15551234567") == "***-***-4567"
    assert mask_phone(None) == "—"


def test_list_accounts_filtering_and_search():
    acc1 = Account(
        id="acc_1",
        profile_id="1001",
        display_name="Marketing Hero",
        status=AccountStatus.ACTIVE,
        health_state=AccountHealthState.HEALTHY,
        category_id="marketing",
    )
    acc1.add_email(AccountEmail(account_id="acc_1", address="hero@marketing.com"))

    acc2 = Account(
        id="acc_2",
        profile_id="1002",
        display_name="Support Desk",
        status=AccountStatus.RESTRICTED,
        health_state=AccountHealthState.WARNING,
        category_id="support",
    )

    acc3 = Account(
        id="acc_3",
        profile_id="1003",
        display_name="Old Account",
        status=AccountStatus.ARCHIVED,
        health_state=AccountHealthState.UNKNOWN,
    )

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [acc1, acc2, acc3]
    mock_uow.environments.list_all.return_value = []
    mock_uow.devices.list_all.return_value = []
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    service = AccountQueryService(uow_factory=lambda: mock_uow_ctx)

    # 1. Default (excludes archived)
    res_default = service.list_accounts()
    assert len(res_default) == 2
    assert res_default[0].id == "acc_1"
    assert res_default[0].masked_contact == "h***o@marketing.com"

    # 2. Include archived
    res_all = service.list_accounts(AccountFilterCriteria(include_archived=True))
    assert len(res_all) == 3

    # 3. Status filter
    res_restricted = service.list_accounts(AccountFilterCriteria(status="restricted"))
    assert len(res_restricted) == 1
    assert res_restricted[0].id == "acc_2"

    # 4. Search filter by name or email
    res_search = service.list_accounts(AccountFilterCriteria(search="Hero"))
    assert len(res_search) == 1
    assert res_search[0].display_name == "Marketing Hero"


def test_get_account_detail_hydration():
    acc = Account(
        id="acc_full",
        profile_id="9999",
        display_name="Full Account",
        security=AccountSecurity(
            account_id="acc_full",
            two_factor_method=TwoFactorMethod.TOTP,
            two_factor_enabled=True,
            password_secret_ref="vault://accounts/acc_full/pass",
            totp_secret_ref="vault://accounts/acc_full/totp",
        ),
    )
    acc.add_email(AccountEmail(account_id="acc_full", address="lead@farm.com"))
    acc.add_phone(AccountPhone(account_id="acc_full", number="+15559876543"))
    acc.pages.append(Page(account_id="acc_full", platform_page_id="pg_1", name="Farm News"))
    acc.groups.append(Group(account_id="acc_full", platform_group_id="grp_1", name="Farm Club"))

    mock_uow = MagicMock()
    mock_uow.accounts.get_by_id.return_value = acc
    mock_uow.environments.list_all.return_value = []
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    service = AccountQueryService(uow_factory=lambda: mock_uow_ctx)
    detail = service.get_account_detail("acc_full")

    assert detail is not None
    assert detail.display_name == "Full Account"
    assert len(detail.emails) == 1
    assert detail.emails[0]["masked"] == "l***d@farm.com"
    assert len(detail.phones) == 1
    assert detail.phones[0]["masked"] == "***-***-6543"
    assert detail.security["two_factor_method"] == "TOTP"
    assert len(detail.pages) == 1
    assert detail.pages[0]["name"] == "Farm News"
    assert len(detail.groups) == 1
    assert detail.groups[0]["name"] == "Farm Club"
