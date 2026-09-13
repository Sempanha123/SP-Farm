"""Cute cards for Pages and Groups grid view."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from spfarm.application.queries.pages_groups import GroupSummaryDTO, PageSummaryDTO
from spfarm.presentation.components.cards import CuteCard
from spfarm.presentation.components.status_pill import CuteStatusPill
from spfarm.shared.theme import PALETTE


class CutePageCard(CuteCard):
    """Visual card for a Facebook Page."""

    clicked = Signal(str)  # page_id
    publishing_toggled = Signal(str, bool)  # (page_id, enabled)

    def __init__(self, page: PageSummaryDTO, parent: Optional[QWidget] = None) -> None:
        badge = CuteStatusPill(
            f"{page.followers:,} followers", "ready" if page.followers > 0 else "offline"
        )
        super().__init__(title=f"📄 {page.name}", badge=badge, parent=parent)
        self.badge = badge
        self.page = page

        self.setStyleSheet(f"""
            CuteCard {{
                background-color: {PALETTE.surface};
                border: 1px solid {PALETTE.border};
                border-radius: 12px;
            }}
            CuteCard:hover {{
                border-color: {PALETTE.primary};
            }}
        """)

        body = QWidget()
        layout = QVBoxLayout(body)
        layout.setContentsMargins(12, 8, 12, 12)
        layout.setSpacing(6)

        # Managing account
        lbl_acc = QLabel(f"👤 Manager: <b>{page.account_name}</b>")
        lbl_acc.setStyleSheet(f"color: {PALETTE.text}; font-size: 11px;")
        layout.addWidget(lbl_acc)

        # ID & Category
        meta_box = QHBoxLayout()
        lbl_id = QLabel(f"ID: {page.platform_page_id}")
        lbl_id.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 10px;")
        lbl_cat = QLabel(f"🏷️ {page.category}")
        lbl_cat.setStyleSheet(f"color: {PALETTE.cute_pink}; font-size: 10px; font-weight: 600;")
        meta_box.addWidget(lbl_id)
        meta_box.addStretch()
        meta_box.addWidget(lbl_cat)
        layout.addLayout(meta_box)

        # Publishing Switch
        pub_box = QHBoxLayout()
        self.chk_pub = QCheckBox("Publishing Enabled")
        self.chk_pub.setChecked(page.publishing_enabled)
        self.chk_pub.toggled.connect(lambda checked: self.publishing_toggled.emit(page.id, checked))
        pub_box.addWidget(self.chk_pub)
        layout.addLayout(pub_box)

        self.add_widget(body)

    def mousePressEvent(self, event) -> None:
        if event is not None:
            super().mousePressEvent(event)
        self.clicked.emit(self.page.id)


class CuteGroupCard(CuteCard):
    """Visual card for a Facebook Group."""

    clicked = Signal(str)  # group_id

    def __init__(self, group: GroupSummaryDTO, parent: Optional[QWidget] = None) -> None:
        role_type = (
            "ready"
            if group.role == "ADMIN"
            else ("warning" if group.role == "MODERATOR" else "cooldown")
        )
        badge = CuteStatusPill(group.role, role_type)
        super().__init__(title=f"👥 {group.name}", badge=badge, parent=parent)
        self.badge = badge
        self.group = group

        body = QWidget()
        layout = QVBoxLayout(body)
        layout.setContentsMargins(12, 8, 12, 12)
        layout.setSpacing(6)

        # Managing account
        lbl_acc = QLabel(f"👤 Member: <b>{group.account_name}</b>")
        lbl_acc.setStyleSheet(f"color: {PALETTE.text}; font-size: 11px;")
        layout.addWidget(lbl_acc)

        # Members & Permission
        meta_box = QHBoxLayout()
        lbl_members = QLabel(f"👥 {group.members:,} members")
        lbl_members.setStyleSheet(f"color: {PALETTE.text_secondary}; font-size: 10px;")
        lbl_perm = QLabel(f"Permission: {group.posting_permission}")
        lbl_perm.setStyleSheet(f"color: {PALETTE.primary}; font-size: 10px; font-weight: 600;")
        meta_box.addWidget(lbl_members)
        meta_box.addStretch()
        meta_box.addWidget(lbl_perm)
        layout.addLayout(meta_box)

        self.add_widget(body)

    def mousePressEvent(self, event) -> None:
        if event is not None:
            super().mousePressEvent(event)
        self.clicked.emit(self.group.id)
