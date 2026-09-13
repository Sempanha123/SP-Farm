"""Tests for Cute Light Design System reusable components."""

from PySide6.QtWidgets import QApplication, QLabel

from spfarm.presentation.components.buttons import CuteButton
from spfarm.presentation.components.cards import CuteCard
from spfarm.presentation.components.command_palette import CommandPaletteDialog
from spfarm.presentation.components.inspector import CuteInspector
from spfarm.presentation.components.status_pill import CuteStatusPill
from spfarm.presentation.components.stepper import CuteStepper
from spfarm.presentation.components.toast import CuteToast


def test_cute_button_roles(qapp: QApplication) -> None:
    btn_primary = CuteButton("Save", role="primary")
    assert btn_primary.property("role") == "primary"

    btn_cute = CuteButton("Cute Action", role="cute")
    assert btn_cute.property("role") == "cute"

    btn_secondary = CuteButton("Cancel", role="secondary")
    assert btn_secondary.property("role") == "secondary"

    btn_ghost = CuteButton("More", role="ghost")
    assert btn_ghost.property("role") == "ghost"

    btn_danger = CuteButton("Delete", role="danger")
    assert btn_danger.property("role") == "danger"


def test_cute_status_pill(qapp: QApplication) -> None:
    pill = CuteStatusPill("Ready", status_type="ready")
    assert pill.status_type == "ready"
    assert pill.text_label.text() == "Ready"

    pill.set_status("Running (1)", "running")
    assert pill.status_type == "running"
    assert pill.text_label.text() == "Running (1)"

    pill.set_status("ADB Error", "error")
    assert pill.status_type == "error"


def test_cute_card(qapp: QApplication) -> None:
    badge = CuteStatusPill("Active", "active")
    card = CuteCard(title="Accounts Overview", badge=badge)
    assert card.title_label.text() == "Accounts Overview"

    body_label = QLabel("Card Content")
    card.add_widget(body_label)
    assert card.body_layout.count() == 1


def test_cute_inspector(qapp: QApplication) -> None:
    inspector = CuteInspector()
    inspector.set_header("Account Details", "ACC-001 · Active")
    assert inspector.lbl_title.text() == "Account Details"
    assert inspector.lbl_subtitle.text() == "ACC-001 · Active"

    # Set content
    inspector.set_content(QLabel("Inspector Form"))
    assert inspector.content_layout.count() == 1

    closed_signal_received: list[bool] = []
    inspector.closed.connect(lambda: closed_signal_received.append(True))
    inspector._on_close()
    assert inspector.isHidden()
    assert closed_signal_received == [True]


def test_cute_toast(qapp: QApplication) -> None:
    toast = CuteToast("Operation succeeded!", toast_type="success", duration_ms=500)
    toast.show_toast()
    assert not toast.isHidden()
    toast._dismiss()


def test_cute_stepper(qapp: QApplication) -> None:
    steps = ["Content", "Targets", "Schedule", "Review"]
    stepper = CuteStepper(steps=steps, current_step=0)
    assert stepper.current_step == 0

    step_changes: list[int] = []
    stepper.step_changed.connect(lambda s: step_changes.append(s))

    stepper.set_step(2)
    assert stepper.current_step == 2
    assert step_changes == [2]


def test_command_palette_dialog(qapp: QApplication) -> None:
    palette = CommandPaletteDialog()
    assert palette.list_widget.count() > 0

    # Search filter
    palette.txt_search.setText("accounts")
    assert palette.list_widget.count() >= 1
    assert "Accounts" in palette.list_widget.item(0).text()

    palette.close()
