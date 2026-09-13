"""Unit tests for Page and Group commands and handlers."""

from __future__ import annotations

from unittest.mock import MagicMock

from spfarm.application.commands.page_group_commands import (
    AddGroupCommand,
    AddGroupHandler,
    AddPageCommand,
    AddPageHandler,
    DeleteGroupCommand,
    DeleteGroupHandler,
    DeletePageCommand,
    DeletePageHandler,
    UpdateGroupCommand,
    UpdateGroupHandler,
    UpdatePageCommand,
    UpdatePageHandler,
)
from spfarm.application.events.base import EventBus
from spfarm.application.services.audit import AuditService
from spfarm.domain.accounts.models import Account, Group, Page


def test_add_page_command():
    acc = Account(id="acc_1", profile_id="1001", display_name="Account 1")
    mock_uow = MagicMock()
    mock_uow.accounts.get_by_id.return_value = acc
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    bus = EventBus()
    audit = MagicMock(spec=AuditService)

    handler = AddPageHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=bus,
        audit_service=audit,
    )

    cmd = AddPageCommand(
        account_id="acc_1",
        platform_page_id="pg_999",
        name="Official News",
        category="Media",
        followers=2500,
        publishing_enabled=True,
    )

    res = handler.handle(cmd)
    assert res.is_success
    page_id = res.value
    assert isinstance(page_id, str)
    assert len(acc.pages) == 1
    assert acc.pages[0].name == "Official News"
    assert acc.pages[0].platform_page_id == "pg_999"
    assert acc.pages[0].followers == 2500
    assert mock_uow.commit.called


def test_update_and_delete_page_command():
    page = Page(
        id="pg_1",
        account_id="acc_1",
        platform_page_id="pg_999",
        name="Old Page Name",
        followers=100,
        publishing_enabled=True,
    )
    acc = Account(id="acc_1", profile_id="1001", display_name="Account 1")
    acc.pages.append(page)

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [acc]
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow

    bus = EventBus()
    audit = MagicMock(spec=AuditService)

    update_handler = UpdatePageHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=bus,
        audit_service=audit,
    )
    delete_handler = DeletePageHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=bus,
        audit_service=audit,
    )

    # Update
    res_up = update_handler.handle(
        UpdatePageCommand(
            page_id="pg_1",
            name="Brand New Name",
            followers=5000,
            publishing_enabled=False,
        )
    )
    assert res_up.is_success
    assert page.name == "Brand New Name"
    assert page.followers == 5000
    assert page.publishing_enabled is False

    # Delete
    res_del = delete_handler.handle(DeletePageCommand(page_id="pg_1"))
    assert res_del.is_success
    assert len(acc.pages) == 0


def test_add_group_command():
    acc = Account(id="acc_1", profile_id="1001", display_name="Account 1")
    mock_uow = MagicMock()
    mock_uow.accounts.get_by_id.return_value = acc
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow

    bus = EventBus()
    audit = MagicMock(spec=AuditService)

    handler = AddGroupHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=bus,
        audit_service=audit,
    )

    cmd = AddGroupCommand(
        account_id="acc_1",
        platform_group_id="grp_555",
        name="Farm Community",
        role="ADMIN",
        members=1200,
        posting_permission="ALLOWED",
    )

    res = handler.handle(cmd)
    assert res.is_success
    group_id = res.value
    assert isinstance(group_id, str)
    assert len(acc.groups) == 1
    assert acc.groups[0].name == "Farm Community"
    assert acc.groups[0].role == "ADMIN"
    assert acc.groups[0].members == 1200


def test_update_and_delete_group_command():
    group = Group(
        id="grp_1",
        account_id="acc_1",
        platform_group_id="grp_555",
        name="Old Group Name",
        role="MEMBER",
        members=50,
    )
    acc = Account(id="acc_1", profile_id="1001", display_name="Account 1")
    acc.groups.append(group)

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [acc]
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow

    bus = EventBus()
    audit = MagicMock(spec=AuditService)

    update_handler = UpdateGroupHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=bus,
        audit_service=audit,
    )
    delete_handler = DeleteGroupHandler(
        uow_factory=lambda: mock_uow_ctx,
        event_bus=bus,
        audit_service=audit,
    )

    # Update
    res_up = update_handler.handle(
        UpdateGroupCommand(
            group_id="grp_1",
            name="Upgraded Community",
            role="MODERATOR",
            members=1000,
        )
    )
    assert res_up.is_success
    assert group.name == "Upgraded Community"
    assert group.role == "MODERATOR"
    assert group.members == 1000

    # Delete
    res_del = delete_handler.handle(DeleteGroupCommand(group_id="grp_1"))
    assert res_del.is_success
    assert len(acc.groups) == 0
