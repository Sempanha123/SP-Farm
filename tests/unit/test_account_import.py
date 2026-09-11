"""Unit tests for AccountImportService with CSV and JSON parsing, duplicate detection, and import execution."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from spfarm.application.commands.account_commands import CreateAccountHandler
from spfarm.application.services.account_dedup import AccountDuplicateDetector
from spfarm.application.services.account_import import AccountImportService
from spfarm.domain.accounts.models import Account, AccountEmail
from spfarm.shared.result import Success


def test_import_csv_preview_and_dedup():
    existing_acc = Account(id="acc_1", profile_id="1001", display_name="Existing John")
    existing_acc.add_email(AccountEmail(account_id="acc_1", address="john@test.com"))

    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = [existing_acc]
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    mock_create_handler = MagicMock(spec=CreateAccountHandler)
    mock_create_handler.handle.return_value = Success("new_acc_id")

    service = AccountImportService(
        uow_factory=lambda: mock_uow_ctx,
        dedup_detector=AccountDuplicateDetector(),
        create_handler=mock_create_handler,
    )

    csv_data = """name,profile_id,email,phone,notes
Alpha Team,2001,alpha@test.com,+15551112222,Team lead
Duplicate John,1001,other@test.com,,Duplicate ID
Invalid Row,,,,No ID or Email
Internal Dup,2001,internal@test.com,,Same ID as Alpha
"""
    preview = service.preview_csv_content(csv_data)
    assert preview.total_rows == 4
    assert preview.valid_count == 1  # Alpha Team
    assert preview.duplicate_count == 2  # Duplicate John (database), Internal Dup (batch)
    assert preview.error_count == 1  # Invalid Row

    # Execute import with skip_duplicates=True
    result = service.execute_import(preview.rows, skip_duplicates=True)
    assert result.imported_count == 1
    assert result.skipped_count == 3
    assert mock_create_handler.handle.call_count == 1


def test_import_json_preview():
    mock_uow = MagicMock()
    mock_uow.accounts.list_all.return_value = []
    mock_uow_ctx = MagicMock()
    mock_uow_ctx.__enter__.return_value = mock_uow
    mock_uow_ctx.__exit__.return_value = None

    service = AccountImportService(
        uow_factory=lambda: mock_uow_ctx,
        dedup_detector=AccountDuplicateDetector(),
        create_handler=MagicMock(),
    )

    json_data = json.dumps([
        {"id": "5001", "name": "JSON User 1", "email": "u1@json.com"},
        {"uid": "5002", "display_name": "JSON User 2", "phone": "1234567890"},
    ])

    preview = service.preview_json_content(json_data)
    assert preview.total_rows == 2
    assert preview.valid_count == 2
    assert preview.duplicate_count == 0
    assert preview.error_count == 0
    assert preview.rows[0].profile_id == "5001"
    assert preview.rows[1].profile_id == "5002"
