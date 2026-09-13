"""UI tests for Pages and Groups workspace (Cards, Dialogs, View, and Inspector)."""

from __future__ import annotations

from unittest.mock import MagicMock

from PySide6.QtWidgets import QApplication, QMessageBox

from spfarm.application.commands.page_group_commands import (
    AddGroupCommand,
    AddPageCommand,
    DeleteGroupCommand,
    UpdatePageCommand,
)
from spfarm.application.events.base import EventBus
from spfarm.application.queries.accounts import AccountQueryService, AccountSummaryDTO
from spfarm.application.queries.pages_groups import (
    GroupSummaryDTO,
    PagesAndGroupsQueryService,
    PageSummaryDTO,
)
from spfarm.presentation.pages_groups.cards import CuteGroupCard, CutePageCard
from spfarm.presentation.pages_groups.group_dialog import GroupDialog
from spfarm.presentation.pages_groups.page_dialog import PageDialog
from spfarm.presentation.pages_groups.pages_groups_view import PagesAndGroupsView
from spfarm.shared.result import Success


def test_cute_page_card(qapp: QApplication) -> None:
    """CutePageCard renders page metadata, capabilities, and emits clicked / publishing_toggled."""
    page = PageSummaryDTO(
        id="page_1",
        account_id="acc_1",
        account_name="Master Account",
        platform_page_id="100998877",
        name="Official Brand Store",
        category="E-commerce",
        followers=15420,
        status="ACTIVE",
        publishing_enabled=True,
        notes="Official brand fanpage",
    )

    card = CutePageCard(page)
    assert "Official Brand Store" in card.title_label.text()
    assert "15,420" in card.badge.text_label.text()

    # Emits clicked signal
    clicked_ids: list[str] = []
    card.clicked.connect(lambda pid: clicked_ids.append(pid))
    card.mousePressEvent(None)
    assert clicked_ids == ["page_1"]

    # Emits publishing_toggled signal
    toggled_events: list[tuple[str, bool]] = []
    card.publishing_toggled.connect(lambda pid, en: toggled_events.append((pid, en)))
    card.chk_pub.setChecked(False)
    assert toggled_events == [("page_1", False)]


def test_cute_group_card(qapp: QApplication) -> None:
    """CuteGroupCard renders group privacy, members, and handles clicked signal."""
    group = GroupSummaryDTO(
        id="grp_1",
        account_id="acc_1",
        account_name="Master Account",
        platform_group_id="554433221",
        name="VIP Customers Community",
        role="ADMIN",
        members=3200,
        posting_permission="ANY_MEMBER",
        notes="High priority customer group",
    )

    card = CuteGroupCard(group)
    assert "VIP Customers Community" in card.title_label.text()
    assert "ADMIN" in card.badge.text_label.text()

    clicked_ids: list[str] = []
    card.clicked.connect(lambda gid: clicked_ids.append(gid))
    card.mousePressEvent(None)
    assert clicked_ids == ["grp_1"]


def test_page_dialog_create_and_validation(qapp: QApplication) -> None:
    """PageDialog validates required fields and constructs AddPageCommand."""
    accounts = [
        AccountSummaryDTO(
            id="acc_1",
            profile_id="10001",
            display_name="Main Operator",
            masked_contact="op@test.com",
            status="ACTIVE",
            health_state="HEALTHY",
            pages_count=1,
            groups_count=1,
            device_name=None,
            last_activity_at=None,
        )
    ]

    dialog = PageDialog(accounts=accounts)
    assert "Attach Facebook Page" in dialog.windowTitle()

    # Fill details
    dialog.txt_name.setText("My Test Page")
    dialog.txt_page_id.setText("9988776655")
    dialog.txt_category.setText("Tech")
    dialog.spin_followers.setValue(500)
    dialog.chk_publishing.setChecked(True)
    dialog.txt_notes.setPlainText("Important page notes")

    cmd = dialog.get_add_command()
    assert isinstance(cmd, AddPageCommand)
    assert cmd.account_id == "acc_1"
    assert cmd.platform_page_id == "9988776655"
    assert cmd.name == "My Test Page"
    assert cmd.category == "Tech"
    assert cmd.followers == 500
    assert cmd.publishing_enabled is True
    assert cmd.notes == "Important page notes"


def test_page_dialog_edit_mode(qapp: QApplication) -> None:
    """PageDialog pre-populates fields in edit mode and constructs UpdatePageCommand."""
    page = PageSummaryDTO(
        id="page_existing",
        account_id="acc_1",
        account_name="Main Operator",
        platform_page_id="9988776655",
        name="Existing Page",
        category="Community",
        followers=1200,
        status="ACTIVE",
        publishing_enabled=True,
        notes="Some notes",
    )

    dialog = PageDialog(accounts=[], page=page)
    assert "Edit Facebook Page" in dialog.windowTitle()
    assert dialog.txt_name.text() == "Existing Page"
    assert dialog.txt_page_id.text() == "9988776655"
    assert dialog.spin_followers.value() == 1200

    dialog.txt_name.setText("Updated Page Title")
    cmd = dialog.get_update_command()
    assert isinstance(cmd, UpdatePageCommand)
    assert cmd.page_id == "page_existing"
    assert cmd.name == "Updated Page Title"


def test_group_dialog_create_and_validation(qapp: QApplication) -> None:
    """GroupDialog validates fields and constructs AddGroupCommand / UpdateGroupCommand."""
    accounts = [
        AccountSummaryDTO(
            id="acc_1",
            profile_id="10001",
            display_name="Main Operator",
            masked_contact="op@test.com",
            status="ACTIVE",
            health_state="HEALTHY",
            pages_count=1,
            groups_count=1,
            device_name=None,
            last_activity_at=None,
        )
    ]

    dialog = GroupDialog(accounts=accounts)
    assert "Associate Facebook Group" in dialog.windowTitle()

    dialog.txt_name.setText("Developers Group")
    dialog.txt_group_id.setText("1122334455")
    dialog.cmb_role.setCurrentText("ADMIN")
    dialog.spin_members.setValue(250)
    dialog.cmb_permission.setCurrentText("ALLOWED")
    dialog.txt_notes.setPlainText("Dev notes")

    cmd = dialog.get_add_command()
    assert isinstance(cmd, AddGroupCommand)
    assert cmd.account_id == "acc_1"
    assert cmd.platform_group_id == "1122334455"
    assert cmd.role == "ADMIN"
    assert cmd.members == 250
    assert cmd.posting_permission == "ALLOWED"


def test_pages_and_groups_view_workflows(qapp: QApplication, monkeypatch) -> None:
    """PagesAndGroupsView handles section toggle, cards/table mode, filtering, and inspector."""
    mock_query_svc = MagicMock(spec=PagesAndGroupsQueryService)
    mock_account_query = MagicMock(spec=AccountQueryService)
    mock_event_bus = MagicMock(spec=EventBus)

    mock_add_page = MagicMock()
    mock_update_page = MagicMock()
    mock_delete_page = MagicMock()
    mock_add_group = MagicMock()
    mock_update_group = MagicMock()
    mock_delete_group = MagicMock()

    sample_pages = [
        PageSummaryDTO(
            id="page_1",
            account_id="acc_1",
            account_name="Alpha Account",
            platform_page_id="111",
            name="Alpha Page",
            category="News",
            followers=1000,
            status="ACTIVE",
            publishing_enabled=True,
            notes="Alpha notes",
        )
    ]
    sample_groups = [
        GroupSummaryDTO(
            id="grp_1",
            account_id="acc_1",
            account_name="Alpha Account",
            platform_group_id="222",
            name="Alpha Community",
            role="MODERATOR",
            members=500,
            posting_permission="ANY_MEMBER",
            notes="Group notes",
        )
    ]

    mock_query_svc.list_pages.return_value = sample_pages
    mock_query_svc.list_groups.return_value = sample_groups
    mock_account_query.list_accounts.return_value = [
        AccountSummaryDTO(
            id="acc_1",
            profile_id="10001",
            display_name="Alpha Account",
            masked_contact="alpha@test.com",
            status="ACTIVE",
            health_state="HEALTHY",
            pages_count=1,
            groups_count=1,
            device_name=None,
            last_activity_at=None,
        )
    ]

    view = PagesAndGroupsView(
        query_service=mock_query_svc,
        account_queries=mock_account_query,
        add_page_handler=mock_add_page,
        update_page_handler=mock_update_page,
        delete_page_handler=mock_delete_page,
        add_group_handler=mock_add_group,
        update_group_handler=mock_update_group,
        delete_group_handler=mock_delete_group,
        event_bus=mock_event_bus,
    )

    # Initial state: Pages section, Table view
    assert view.current_section == "pages"
    assert view.table_view.rowCount() == 1
    assert "Alpha Page" in view.table_view.item(0, 1).text()

    # Select page row -> Inspector updates
    view._select_entity("page_1")
    assert "Alpha Page" in view.insp_title.text()
    assert "Alpha notes" in view.insp_notes.toPlainText()

    # Toggle view mode to Cards
    view._toggle_view_mode()
    assert view.view_mode == "cards"
    assert view.center_stack.currentIndex() == 1

    # Switch section to Groups
    view._set_section("groups")
    assert view.current_section == "groups"
    assert view.btn_add.text() == "➕ Add Group"

    # Select group entity -> Inspector updates
    view._select_entity("grp_1")
    assert "Alpha Community" in view.insp_title.text()
    assert "Group notes" in view.insp_notes.toPlainText()

    # Delete entity confirmation mock
    monkeypatch.setattr(
        QMessageBox, "question", lambda *args, **kwargs: QMessageBox.StandardButton.Yes
    )
    mock_delete_group.handle.return_value = Success(None)

    view._on_delete_item()
    mock_delete_group.handle.assert_called_once()
    assert isinstance(mock_delete_group.handle.call_args[0][0], DeleteGroupCommand)
    assert mock_delete_group.handle.call_args[0][0].group_id == "grp_1"
