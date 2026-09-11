"""Account batch import service from CSV and JSON files with preview and duplicate detection."""

from __future__ import annotations

import csv
import io
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from spfarm.application.commands.account_commands import CreateAccountCommand, CreateAccountHandler
from spfarm.application.services.account_dedup import AccountDuplicateDetector
from spfarm.domain.accounts.models import Account
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork

logger = logging.getLogger(__name__)


@dataclass
class ImportRowDTO:
    """Parsed single account candidate row from import source."""

    row_index: int
    display_name: str
    profile_id: str
    email: str = ""
    phone: str = ""
    category_id: str = ""
    notes: str = ""
    status: str = "ACTIVE"
    is_valid: bool = True
    validation_error: Optional[str] = None
    is_duplicate: bool = False
    duplicate_reason: Optional[str] = None


@dataclass
class ImportPreviewDTO:
    """Aggregated preview of an import batch before committing."""

    total_rows: int = 0
    valid_count: int = 0
    duplicate_count: int = 0
    error_count: int = 0
    rows: list[ImportRowDTO] = field(default_factory=list)


@dataclass
class ImportResultDTO:
    """Outcome of committing an import batch."""

    imported_count: int = 0
    skipped_count: int = 0
    error_count: int = 0
    errors: list[str] = field(default_factory=list)


class AccountImportService:
    """Parses, previews, and imports accounts from CSV or JSON files."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
        dedup_detector: AccountDuplicateDetector,
        create_handler: CreateAccountHandler,
    ) -> None:
        self._uow_factory = uow_factory
        self._dedup = dedup_detector
        self._create_handler = create_handler

    def preview_csv_content(self, content: str) -> ImportPreviewDTO:
        """Parse raw CSV string and return preview with duplicate detection."""
        stream = io.StringIO(content.strip())
        reader = csv.DictReader(stream)
        raw_rows: list[dict[str, str]] = list(reader)
        return self._build_preview(raw_rows)

    def preview_csv_file(self, file_path: str | Path) -> ImportPreviewDTO:
        """Read CSV file from disk and return preview."""
        path = Path(file_path)
        if not path.exists():
            return ImportPreviewDTO(error_count=1, rows=[
                ImportRowDTO(
                    row_index=0,
                    display_name="",
                    profile_id="",
                    is_valid=False,
                    validation_error=f"File not found: {path}",
                )
            ])
        text = path.read_text(encoding="utf-8-sig")
        return self.preview_csv_content(text)

    def preview_json_content(self, content: str) -> ImportPreviewDTO:
        """Parse raw JSON string and return preview with duplicate detection."""
        try:
            data = json.loads(content)
        except Exception as exc:
            return ImportPreviewDTO(error_count=1, rows=[
                ImportRowDTO(
                    row_index=0,
                    display_name="",
                    profile_id="",
                    is_valid=False,
                    validation_error=f"Invalid JSON syntax: {exc}",
                )
            ])

        if isinstance(data, dict):
            # Check if wrapped in "accounts" or "data"
            data = data.get("accounts", data.get("data", [data]))
        if not isinstance(data, list):
            data = [data]

        raw_rows: list[dict[str, str]] = []
        for item in data:
            if isinstance(item, dict):
                raw_rows.append({str(k): str(v) for k, v in item.items()})

        return self._build_preview(raw_rows)

    def preview_json_file(self, file_path: str | Path) -> ImportPreviewDTO:
        """Read JSON file from disk and return preview."""
        path = Path(file_path)
        if not path.exists():
            return ImportPreviewDTO(error_count=1, rows=[
                ImportRowDTO(
                    row_index=0,
                    display_name="",
                    profile_id="",
                    is_valid=False,
                    validation_error=f"File not found: {path}",
                )
            ])
        text = path.read_text(encoding="utf-8-sig")
        return self.preview_json_content(text)

    def _build_preview(self, raw_rows: list[dict[str, str]]) -> ImportPreviewDTO:
        """Normalize columns, validate, and check duplicates."""
        existing_accounts: list[Account] = []
        with self._uow_factory() as uow:
            existing_accounts = uow.accounts.list_all()

        rows: list[ImportRowDTO] = []
        seen_profile_ids: set[str] = set()
        seen_emails: set[str] = set()

        valid_count = 0
        dup_count = 0
        err_count = 0

        for idx, r in enumerate(raw_rows, start=1):
            # Normalize column names case-insensitively
            normalized: dict[str, str] = {k.strip().lower(): (v or "").strip() for k, v in r.items()}

            profile_id = (
                normalized.get("profile_id")
                or normalized.get("uid")
                or normalized.get("id")
                or normalized.get("account_id")
                or ""
            )
            display_name = (
                normalized.get("display_name")
                or normalized.get("name")
                or normalized.get("label")
                or profile_id
            )
            email = normalized.get("email") or normalized.get("primary_email") or ""
            phone = normalized.get("phone") or normalized.get("primary_phone") or normalized.get("mobile") or ""
            category_id = normalized.get("category") or normalized.get("category_id") or ""
            notes = normalized.get("notes") or normalized.get("remark") or ""
            status = normalized.get("status") or "ACTIVE"

            # Validation
            is_valid = True
            val_error: Optional[str] = None

            if not profile_id and not email:
                is_valid = False
                val_error = "Missing profile ID and email."
            elif not display_name:
                display_name = profile_id or email

            # Duplicate Check
            is_dup = False
            dup_reason: Optional[str] = None

            if is_valid:
                # Check within batch
                if profile_id and profile_id in seen_profile_ids:
                    is_dup = True
                    dup_reason = f"Duplicate profile ID in import batch: {profile_id}"
                elif email and email.lower() in seen_emails:
                    is_dup = True
                    dup_reason = f"Duplicate email in import batch: {email}"

                # Check against database
                if not is_dup:
                    matches = self._dedup.check_duplicates_in_collection(
                        target_profile_id=profile_id,
                        target_emails=[email] if email else [],
                        target_phones=[phone] if phone else [],
                        existing_accounts=existing_accounts,
                    )
                    if matches:
                        m = matches[0]
                        is_dup = True
                        dup_reason = f"Matches existing account '{m.display_name}' ({m.match_field}: {m.match_value})"

                if profile_id:
                    seen_profile_ids.add(profile_id)
                if email:
                    seen_emails.add(email.lower())

            if not is_valid:
                err_count += 1
            elif is_dup:
                dup_count += 1
            else:
                valid_count += 1

            rows.append(
                ImportRowDTO(
                    row_index=idx,
                    display_name=display_name,
                    profile_id=profile_id,
                    email=email,
                    phone=phone,
                    category_id=category_id,
                    notes=notes,
                    status=status,
                    is_valid=is_valid,
                    validation_error=val_error,
                    is_duplicate=is_dup,
                    duplicate_reason=dup_reason,
                )
            )

        return ImportPreviewDTO(
            total_rows=len(rows),
            valid_count=valid_count,
            duplicate_count=dup_count,
            error_count=err_count,
            rows=rows,
        )

    def execute_import(
        self,
        rows: list[ImportRowDTO],
        skip_duplicates: bool = True,
    ) -> ImportResultDTO:
        """Commit selected rows into the system."""
        imported = 0
        skipped = 0
        errors: list[str] = []

        for row in rows:
            if not row.is_valid:
                skipped += 1
                continue

            if row.is_duplicate and skip_duplicates:
                skipped += 1
                continue

            cmd = CreateAccountCommand(
                display_name=row.display_name,
                profile_id=row.profile_id or row.email,
                primary_email=row.email if row.email else None,
                primary_phone=row.phone if row.phone else None,
                category_id=row.category_id if row.category_id else None,
                notes=row.notes if row.notes else None,
                allow_duplicates=(not skip_duplicates),
            )

            res = self._create_handler.handle(cmd)
            if res.is_success:
                imported += 1
            else:
                errors.append(f"Row {row.row_index} ({row.display_name}): {res.error.message}")

        return ImportResultDTO(
            imported_count=imported,
            skipped_count=skipped,
            error_count=len(errors),
            errors=errors,
        )
