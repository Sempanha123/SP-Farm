"""Account queries, DTOs, and query service for scalable table and inspector views."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from spfarm.application.queries.base import Query
from spfarm.domain.interfaces.unit_of_work import IUnitOfWork

logger = logging.getLogger(__name__)


def mask_email(email: str | None) -> str:
    """Mask email for privacy, e.g. johndoe@gmail.com -> j***e@gmail.com."""
    if not email:
        return "—"
    parts = email.split("@")
    if len(parts) != 2:
        return email[:2] + "***"
    local, domain = parts
    if len(local) <= 2:
        masked_local = local[0] + "***" if local else "***"
    else:
        masked_local = local[0] + "***" + local[-1]
    return f"{masked_local}@{domain}"


def mask_phone(phone: str | None) -> str:
    """Mask phone for privacy, e.g. +18551234567 -> +1 (***) ***-**67."""
    if not phone:
        return "—"
    digits = re.sub(r"[^\d]", "", phone)
    if len(digits) < 4:
        return "***"
    return f"***-***-{digits[-4:]}"


@dataclass(frozen=True)
class AccountSummaryDTO:
    """Lightweight projection of an Account aggregate for high-speed table rendering."""

    id: str
    profile_id: str
    display_name: str
    masked_contact: str
    status: str
    health_state: str
    pages_count: int
    groups_count: int
    device_name: str
    last_activity_at: Optional[str] = None
    category_id: Optional[str] = None
    notes: Optional[str] = None
    is_archived: bool = False


@dataclass(frozen=True)
class AccountDetailDTO:
    """Fully hydrated projection of an Account aggregate for the inspector panel."""

    id: str
    profile_id: str
    display_name: str
    status: str
    health_state: str
    priority: int
    locale: str
    timezone: str
    category_id: Optional[str]
    notes: Optional[str]
    created_at: str
    last_activity_at: Optional[str]
    emails: list[dict[str, Any]] = field(default_factory=list)
    phones: list[dict[str, Any]] = field(default_factory=list)
    security: dict[str, Any] = field(default_factory=dict)
    pages: list[dict[str, Any]] = field(default_factory=list)
    groups: list[dict[str, Any]] = field(default_factory=list)
    environment: Optional[dict[str, Any]] = None
    runtime_device: Optional[dict[str, Any]] = None


@dataclass(frozen=True)
class AccountFilterCriteria:
    """Filter parameters for querying accounts."""

    search: str = ""
    status: Optional[str] = None
    health_state: Optional[str] = None
    category_id: Optional[str] = None
    include_archived: bool = False
    limit: int = 10000
    offset: int = 0


@dataclass(frozen=True)
class ListAccountsQuery(Query):
    """Query to list accounts matching filter criteria."""

    criteria: AccountFilterCriteria = field(default_factory=AccountFilterCriteria)


@dataclass(frozen=True)
class GetAccountDetailQuery(Query):
    """Query to get hydrated account details by ID."""

    account_id: str


class AccountQueryService:
    """Service providing high-performance query projections for accounts."""

    def __init__(self, uow_factory: Callable[[], IUnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def list_accounts(
        self, criteria: Optional[AccountFilterCriteria] = None
    ) -> list[AccountSummaryDTO]:
        """Query and filter accounts with high speed."""
        crit = criteria or AccountFilterCriteria()
        results: list[AccountSummaryDTO] = []

        search_term = crit.search.strip().lower()

        try:
            with self._uow_factory() as uow:
                accounts = uow.accounts.list_all()

                # Pre-fetch environments and devices for fast joining
                envs_by_acc: dict[str, Any] = {}
                for env in uow.environments.list_all():
                    envs_by_acc[env.account_id] = env

            devices_by_id: dict[str, Any] = {}
            for dev in uow.devices.list_all():
                devices_by_id[dev.id] = dev

            for acc in accounts:
                is_archived = acc.status.value == "ARCHIVED"
                if not crit.include_archived and is_archived:
                    continue

                if crit.status and acc.status.value.lower() != crit.status.lower():
                    continue

                if (
                    crit.health_state
                    and acc.health_state.value.lower() != crit.health_state.lower()
                ):
                    continue

                if crit.category_id and acc.category_id != crit.category_id:
                    continue

                # Search filter across name, profile ID, emails, notes
                if search_term:
                    match_found = False
                    if (
                        search_term in acc.display_name.lower()
                        or search_term in acc.profile_id.lower()
                        or acc.notes
                        and search_term in acc.notes.lower()
                    ):
                        match_found = True
                    else:
                        for em in acc.emails:
                            if search_term in em.address.lower():
                                match_found = True
                                break
                    if not match_found:
                        continue

                # Primary contact
                p_email = acc.primary_email
                p_phone = acc.primary_phone
                if p_email:
                    contact_str = mask_email(p_email.address)
                elif p_phone:
                    contact_str = mask_phone(p_phone.number)
                else:
                    contact_str = "—"

                # Device name
                device_name = "Unassigned"
                env = envs_by_acc.get(acc.id)
                if env and env.last_device_id and env.last_device_id in devices_by_id:
                    d = devices_by_id[env.last_device_id]
                    device_name = d.custom_name or d.id

                results.append(
                    AccountSummaryDTO(
                        id=acc.id,
                        profile_id=acc.profile_id,
                        display_name=acc.display_name,
                        masked_contact=contact_str,
                        status=acc.status.value,
                        health_state=acc.health_state.value,
                        pages_count=len(acc.pages),
                        groups_count=len(acc.groups),
                        device_name=device_name,
                        last_activity_at=acc.last_activity_at,
                        category_id=acc.category_id,
                        notes=acc.notes,
                        is_archived=is_archived,
                    )
                )

        except Exception as exc:
            logger.warning("Could not list accounts from UnitOfWork: %s", exc)
            return []

        if crit.offset > 0:
            results = results[crit.offset :]
        if crit.limit > 0:
            results = results[: crit.limit]

        return results

    def get_account_detail(self, account_id: str) -> Optional[AccountDetailDTO]:
        """Fetch fully hydrated account detail projection."""
        try:
            with self._uow_factory() as uow:
                acc = uow.accounts.get_by_id(account_id)
                if not acc:
                    return None

            # Environment & Device
            env_dict: Optional[dict[str, Any]] = None
            dev_dict: Optional[dict[str, Any]] = None

            envs = [e for e in uow.environments.list_all() if e.account_id == account_id]
            if envs:
                env = envs[0]
                env_dict = {
                    "id": env.id,
                    "app_channel": env.app_channel.value,
                    "android_version": env.android_version,
                    "locale": env.locale,
                    "timezone": env.timezone,
                    "user_agent": env.user_agent,
                    "storage_dir": env.storage_dir,
                    "revision": env.revision,
                }
                if env.last_device_id:
                    dev = uow.devices.get_by_id(env.last_device_id)
                    if dev:
                        dev_dict = {
                            "id": dev.id,
                            "custom_name": dev.custom_name or dev.id,
                            "provider": dev.provider.value,
                            "state": dev.state.value,
                            "adb_serial": dev.adb_serial,
                            "adb_port": dev.adb_port,
                        }

            emails_list = [
                {
                    "id": em.id,
                    "address": em.address,
                    "masked": mask_email(em.address),
                    "is_primary": em.is_primary,
                    "is_verified": em.is_verified,
                }
                for em in acc.emails
            ]

            phones_list = [
                {
                    "id": ph.id,
                    "number": ph.number,
                    "masked": mask_phone(ph.number),
                    "is_primary": ph.is_primary,
                    "is_verified": ph.is_verified,
                }
                for ph in acc.phones
            ]

            sec_dict: dict[str, Any] = {}
            if acc.security:
                sec = acc.security
                sec_dict = {
                    "two_factor_enabled": sec.two_factor_enabled,
                    "two_factor_method": sec.two_factor_method.value,
                    "password_secret_ref": sec.password_secret_ref,
                    "totp_secret_ref": sec.totp_secret_ref,
                    "recovery_codes_secret_ref": sec.recovery_codes_secret_ref,
                    "last_security_review_at": sec.last_security_review_at,
                }

            pages_list = [
                {
                    "id": pg.id,
                    "platform_page_id": pg.platform_page_id,
                    "name": pg.name,
                    "category": pg.category,
                    "followers": pg.followers,
                    "status": pg.status,
                    "publishing_enabled": pg.publishing_enabled,
                }
                for pg in acc.pages
            ]

            groups_list = [
                {
                    "id": gr.id,
                    "platform_group_id": gr.platform_group_id,
                    "name": gr.name,
                    "role": gr.role,
                    "members": gr.members,
                    "posting_permission": gr.posting_permission,
                }
                for gr in acc.groups
            ]

            return AccountDetailDTO(
                id=acc.id,
                profile_id=acc.profile_id,
                display_name=acc.display_name,
                status=acc.status.value,
                health_state=acc.health_state.value,
                priority=acc.priority,
                locale=acc.locale,
                timezone=acc.timezone,
                category_id=acc.category_id,
                notes=acc.notes,
                created_at=acc.created_at,
                last_activity_at=acc.last_activity_at,
                emails=emails_list,
                phones=phones_list,
                security=sec_dict,
                pages=pages_list,
                groups=groups_list,
                environment=env_dict,
                runtime_device=dev_dict,
            )
        except Exception as exc:
            logger.warning("Could not get account detail from UnitOfWork: %s", exc)
            return None
