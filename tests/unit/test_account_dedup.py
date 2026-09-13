"""Unit tests for AccountDuplicateDetector."""

from __future__ import annotations

from spfarm.application.services.account_dedup import (
    AccountDuplicateDetector,
    normalize_email,
    normalize_phone,
)
from spfarm.domain.accounts.models import Account, AccountEmail, AccountPhone


def test_normalization():
    assert normalize_email("  Test.User@GMAIL.COM  ") == "test.user@gmail.com"
    assert normalize_phone("+1 (555) 123-4567") == "15551234567"
    assert normalize_email(None) == ""
    assert normalize_phone(None) == ""


def test_duplicate_detector_matching():
    acc1 = Account(id="acc_1", profile_id="100099", display_name="Account One")
    acc1.add_email(AccountEmail(account_id="acc_1", address="john@example.com"))
    acc1.add_phone(AccountPhone(account_id="acc_1", number="+1 555-0011"))

    acc2 = Account(id="acc_2", profile_id="200088", display_name="Account Two")
    acc2.add_email(AccountEmail(account_id="acc_2", address="sarah@example.com"))

    accounts = [acc1, acc2]
    detector = AccountDuplicateDetector()

    # 1. Profile ID collision
    matches = detector.check_duplicates_in_collection(
        target_profile_id="100099",
        target_emails=["different@example.com"],
        target_phones=[],
        existing_accounts=accounts,
    )
    assert len(matches) == 1
    assert matches[0].account_id == "acc_1"
    assert matches[0].match_field == "profile_id"

    # 2. Email collision (case insensitive)
    matches_email = detector.check_duplicates_in_collection(
        target_profile_id="999999",
        target_emails=["  JOHN@example.com "],
        target_phones=[],
        existing_accounts=accounts,
    )
    assert len(matches_email) == 1
    assert matches_email[0].account_id == "acc_1"
    assert matches_email[0].match_field == "email"

    # 3. Phone collision
    matches_phone = detector.check_duplicates_in_collection(
        target_profile_id="999999",
        target_emails=[],
        target_phones=["(555) 001-1"],
        existing_accounts=accounts,
    )
    assert len(matches_phone) == 1
    assert matches_phone[0].account_id == "acc_1"
    assert matches_phone[0].match_field == "phone"

    # 4. Self exclusion
    matches_self = detector.check_duplicates_in_collection(
        target_profile_id="100099",
        target_emails=["john@example.com"],
        target_phones=[],
        existing_accounts=accounts,
        exclude_account_id="acc_1",
    )
    assert len(matches_self) == 0

    # 5. Clean / unique candidate
    matches_clean = detector.check_duplicates_in_collection(
        target_profile_id="300077",
        target_emails=["unique@example.com"],
        target_phones=["+1 555-9999"],
        existing_accounts=accounts,
    )
    assert len(matches_clean) == 0
