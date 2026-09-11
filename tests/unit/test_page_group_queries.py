"""Unit tests for PagesAndGroupsQueryService."""

from __future__ import annotations

from unittest.mock import MagicMock

from spfarm.application.queries.pages_groups import (
    PagesAndGroupsQueryService,
)
from spfarm.domain.accounts.models import Account, Group, Page


def test_list_pages_and_filtering():
    acc1 = Account(id="acc_1", profile_id="1001", display_name="Account Alpha")
    p1 = Page(
        id="pg_1",
        account_id="acc_1",
        platform_page_id="p_101",
        name="Tech Daily",
        category="Technology",
        followers=8000,
    )
    p2 = Page(
        id="pg_2",
        account_id="acc_1",
        platform_page_id="p_102",
        name="Cooking Fun",
        category="Food",
        followers=2000,
    )
    acc1.pages.extend([p1, p2])

    acc2 = Account(id="acc_2", profile_id="1002", display_name="Account Beta")
    p3 = Page(
        id="pg_3",
        account_id="acc_2",
        platform_page_id="p_103",
        name="Gaming Zone",
        category="Gaming",
        followers=15000,
    )
    acc2.pages.append(p3)

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [acc1, acc2]
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    service = PagesAndGroupsQueryService(uow_factory=lambda: mock_uow_ctx)

    # 1. List all
    all_pages = service.list_pages()
    assert len(all_pages) == 3

    # 2. Filter by account
    acc1_pages = service.list_pages(account_id="acc_1")
    assert len(acc1_pages) == 2
    assert acc1_pages[0].account_name == "Account Alpha"

    # 3. Filter by category
    tech_pages = service.list_pages(category="Technology")
    assert len(tech_pages) == 1
    assert tech_pages[0].name == "Tech Daily"

    # 4. Search keyword
    gaming_pages = service.list_pages(search="gaming")
    assert len(gaming_pages) == 1
    assert gaming_pages[0].name == "Gaming Zone"


def test_list_groups_and_filtering():
    acc = Account(id="acc_1", profile_id="1001", display_name="Account Alpha")
    g1 = Group(
        id="grp_1",
        account_id="acc_1",
        platform_group_id="g_501",
        name="Developers Hub",
        role="ADMIN",
        members=500,
    )
    g2 = Group(
        id="grp_2",
        account_id="acc_1",
        platform_group_id="g_502",
        name="Coffee Lovers",
        role="MEMBER",
        members=120,
    )
    acc.groups.extend([g1, g2])

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [acc]
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    service = PagesAndGroupsQueryService(uow_factory=lambda: mock_uow_ctx)

    all_groups = service.list_groups()
    assert len(all_groups) == 2

    admin_groups = service.list_groups(role="ADMIN")
    assert len(admin_groups) == 1
    assert admin_groups[0].name == "Developers Hub"

    search_groups = service.list_groups(search="coffee")
    assert len(search_groups) == 1
    assert search_groups[0].name == "Coffee Lovers"
