"""Account duplicate detection service."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Iterable, Optional

from spfarm.domain.accounts.models import Account
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork


def normalize_email(email: str | None) -> str:
    """Normalize email address for case-insensitive matching."""
    if not email:
        return ""
    return email.strip().lower()


def normalize_phone(phone: str | None) -> str:
    """Normalize phone number to digits only for reliable matching."""
    if not phone:
        return ""
    return re.sub(r"[^\d]", "", phone)


@dataclass(frozen=True)
class DuplicateMatch:
    """Record of a duplicate match against an existing account."""

    account_id: str
    display_name: str
    match_field: str  # "profile_id", "email", "phone"
    match_value: str


class AccountDuplicateDetector:
    """Detects duplicate account records across profile IDs, emails, and phone numbers."""

    def __init__(self, uow_factory: Optional[Callable[[], IUnitOfWork]] = None) -> None:
        self._uow_factory = uow_factory

    def check_duplicates_in_collection(
        self,
        target_profile_id: str,
        target_emails: Iterable[str],
        target_phones: Iterable[str],
        existing_accounts: Iterable[Account],
        exclude_account_id: Optional[str] = None,
    ) -> list[DuplicateMatch]:
        """Check duplicate matches against a provided in-memory collection of accounts."""
        matches: list[DuplicateMatch] = []

        norm_target_pid = (target_profile_id or "").strip()
        norm_target_emails = {normalize_email(e) for e in target_emails if normalize_email(e)}
        norm_target_phones = {normalize_phone(p) for p in target_phones if normalize_phone(p)}

        for acc in existing_accounts:
            if exclude_account_id and acc.id == exclude_account_id:
                continue

            # 1. Profile ID match
            if norm_target_pid and acc.profile_id.strip() == norm_target_pid:
                matches.append(
                    DuplicateMatch(
                        account_id=acc.id,
                        display_name=acc.display_name,
                        match_field="profile_id",
                        match_value=acc.profile_id,
                    )
                )
                continue

            # 2. Email match
            acc_emails = {
                normalize_email(e.address) for e in acc.emails if normalize_email(e.address)
            }
            email_overlap = norm_target_emails.intersection(acc_emails)
            if email_overlap:
                matches.append(
                    DuplicateMatch(
                        account_id=acc.id,
                        display_name=acc.display_name,
                        match_field="email",
                        match_value=list(email_overlap)[0],
                    )
                )
                continue

            # 3. Phone match
            acc_phones = [
                normalize_phone(p.number) for p in acc.phones if normalize_phone(p.number)
            ]
            matched_phone: Optional[str] = None
            for tp in norm_target_phones:
                for ap in acc_phones:
                    if tp == ap or (
                        len(tp) >= 7 and len(ap) >= 7 and (tp.endswith(ap) or ap.endswith(tp))
                    ):
                        matched_phone = tp
                        break
                if matched_phone:
                    break

            if matched_phone:
                matches.append(
                    DuplicateMatch(
                        account_id=acc.id,
                        display_name=acc.display_name,
                        match_field="phone",
                        match_value=matched_phone,
                    )
                )

        return matches

    def check_duplicates(
        self,
        target_profile_id: str,
        target_emails: Iterable[str],
        target_phones: Iterable[str],
        exclude_account_id: Optional[str] = None,
    ) -> list[DuplicateMatch]:
        """Check duplicate matches against the persistent UnitOfWork database."""
        if not self._uow_factory:
            return []

        with self._uow_factory() as uow:
            existing_accounts = uow.accounts.list_all()
            return self.check_duplicates_in_collection(
                target_profile_id=target_profile_id,
                target_emails=target_emails,
                target_phones=target_phones,
                existing_accounts=existing_accounts,
                exclude_account_id=exclude_account_id,
            )
