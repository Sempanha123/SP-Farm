"""Account repository implementation with full entity hydration."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import select

from spfarm.domain.accounts.models import (
    Account,
    AccountEmail,
    AccountPhone,
    AccountSecurity,
    Group,
    Page,
)
from spfarm.domain.enums import AccountHealthState, AccountStatus, TwoFactorMethod
from spfarm.infrastructure.database.models import (
    AccountEmailModel,
    AccountModel,
    AccountPhoneModel,
    AccountSecurityModel,
    GroupModel,
    PageModel,
)
from spfarm.infrastructure.database.repositories.base import BaseRepository


class AccountRepository(BaseRepository[Account]):
    """Repository managing Account aggregates."""

    def add(self, account: Account) -> None:
        """Persist or update an Account aggregate."""
        model = self.session.get(AccountModel, account.id)
        if not model:
            model = AccountModel(id=account.id, profile_id=account.profile_id, display_name=account.display_name, created_at=account.created_at)
            self.session.add(model)

        # Update scalar fields
        model.platform = account.platform
        model.profile_id = account.profile_id
        model.display_name = account.display_name
        model.first_name = account.first_name
        model.middle_name = account.middle_name
        model.last_name = account.last_name
        model.username = account.username
        model.profile_url = account.profile_url
        model.avatar_asset_id = account.avatar_asset_id
        model.birthday = account.birthday
        model.gender_optional = account.gender_optional
        model.country = account.country
        model.city = account.city
        model.language = account.language
        model.locale = account.locale
        model.timezone = account.timezone
        model.status = account.status.value
        model.health_state = account.health_state.value
        model.priority = account.priority
        model.workspace_id = account.workspace_id
        model.category_id = account.category_id
        model.notes = account.notes
        model.imported_at = account.imported_at
        model.last_synced_at = account.last_synced_at
        model.last_activity_at = account.last_activity_at
        model.archived_at = account.archived_at

        # Sync emails
        model.emails.clear()
        for em in account.emails:
            model.emails.append(
                AccountEmailModel(
                    id=em.id,
                    account_id=account.id,
                    address=em.address,
                    label=em.label,
                    is_primary=em.is_primary,
                    is_verified=em.is_verified,
                    added_at=em.added_at,
                    last_checked_at=em.last_checked_at,
                )
            )

        # Sync phones
        model.phones.clear()
        for ph in account.phones:
            model.phones.append(
                AccountPhoneModel(
                    id=ph.id,
                    account_id=account.id,
                    number=ph.number,
                    country=ph.country,
                    label=ph.label,
                    is_primary=ph.is_primary,
                    is_verified=ph.is_verified,
                    added_at=ph.added_at,
                    last_checked_at=ph.last_checked_at,
                )
            )

        # Sync security
        if account.security:
            sec = account.security
            model.security = AccountSecurityModel(
                account_id=account.id,
                two_factor_enabled=sec.two_factor_enabled,
                two_factor_method=sec.two_factor_method.value,
                recovery_email_status=sec.recovery_email_status,
                recovery_phone_status=sec.recovery_phone_status,
                manual_review_required=sec.manual_review_required,
                restriction_state=sec.restriction_state,
                last_security_review_at=sec.last_security_review_at,
                password_secret_ref=sec.password_secret_ref,
                totp_secret_ref=sec.totp_secret_ref,
                recovery_codes_secret_ref=sec.recovery_codes_secret_ref,
                cookie_vault_ref=sec.cookie_vault_ref,
                session_vault_ref=sec.session_vault_ref,
                access_token_secret_ref=sec.access_token_secret_ref,
                session_updated_at=sec.session_updated_at,
            )

        # Sync pages
        model.pages.clear()
        for pg in account.pages:
            model.pages.append(
                PageModel(
                    id=pg.id,
                    account_id=account.id,
                    platform_page_id=pg.platform_page_id,
                    name=pg.name,
                    category=pg.category,
                    profile_url=pg.profile_url,
                    followers=pg.followers,
                    status=pg.status,
                    publishing_enabled=pg.publishing_enabled,
                    last_synced_at=pg.last_synced_at,
                    last_published_at=pg.last_published_at,
                    notes=pg.notes,
                )
            )

        # Sync groups
        model.groups.clear()
        for gr in account.groups:
            model.groups.append(
                GroupModel(
                    id=gr.id,
                    account_id=account.id,
                    platform_group_id=gr.platform_group_id,
                    name=gr.name,
                    role=gr.role,
                    members=gr.members,
                    posting_permission=gr.posting_permission,
                    last_synced_at=gr.last_synced_at,
                    notes=gr.notes,
                )
            )

    def get_by_id(self, account_id: str) -> Optional[Account]:
        """Retrieve an Account domain entity by UUID."""
        model = self.session.get(AccountModel, account_id)
        if not model:
            return None
        return self._to_domain(model)

    def get_by_profile_id(self, profile_id: str) -> Optional[Account]:
        """Retrieve an Account domain entity by platform profile ID."""
        stmt = select(AccountModel).where(AccountModel.profile_id == profile_id)
        model = self.session.execute(stmt).scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    def list_all(self) -> list[Account]:
        """List all accounts."""
        stmt = select(AccountModel)
        models = self.session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def delete(self, account_id: str) -> bool:
        """Delete an account by UUID."""
        model = self.session.get(AccountModel, account_id)
        if model:
            self.session.delete(model)
            return True
        return False

    def _to_domain(self, m: AccountModel) -> Account:
        """Convert ORM model to pure Domain entity."""
        account = Account(
            id=m.id,
            platform=m.platform,
            profile_id=m.profile_id,
            display_name=m.display_name,
            first_name=m.first_name,
            middle_name=m.middle_name,
            last_name=m.last_name,
            username=m.username,
            profile_url=m.profile_url,
            avatar_asset_id=m.avatar_asset_id,
            birthday=m.birthday,
            gender_optional=m.gender_optional,
            country=m.country,
            city=m.city,
            language=m.language,
            locale=m.locale,
            timezone=m.timezone,
            status=AccountStatus(m.status),
            health_state=AccountHealthState(m.health_state),
            priority=m.priority,
            workspace_id=m.workspace_id,
            category_id=m.category_id,
            notes=m.notes,
            created_at=m.created_at,
            imported_at=m.imported_at,
            last_synced_at=m.last_synced_at,
            last_activity_at=m.last_activity_at,
            archived_at=m.archived_at,
        )

        for em in m.emails:
            account.emails.append(
                AccountEmail(
                    id=em.id,
                    account_id=account.id,
                    address=em.address,
                    label=em.label,
                    is_primary=em.is_primary,
                    is_verified=em.is_verified,
                    added_at=em.added_at,
                    last_checked_at=em.last_checked_at,
                )
            )

        for ph in m.phones:
            account.phones.append(
                AccountPhone(
                    id=ph.id,
                    account_id=account.id,
                    number=ph.number,
                    country=ph.country,
                    label=ph.label,
                    is_primary=ph.is_primary,
                    is_verified=ph.is_verified,
                    added_at=ph.added_at,
                    last_checked_at=ph.last_checked_at,
                )
            )

        if m.security:
            sec = m.security
            account.security = AccountSecurity(
                account_id=account.id,
                two_factor_enabled=sec.two_factor_enabled,
                two_factor_method=TwoFactorMethod(sec.two_factor_method),
                recovery_email_status=sec.recovery_email_status,
                recovery_phone_status=sec.recovery_phone_status,
                manual_review_required=sec.manual_review_required,
                restriction_state=sec.restriction_state,
                last_security_review_at=sec.last_security_review_at,
                password_secret_ref=sec.password_secret_ref,
                totp_secret_ref=sec.totp_secret_ref,
                recovery_codes_secret_ref=sec.recovery_codes_secret_ref,
                cookie_vault_ref=sec.cookie_vault_ref,
                session_vault_ref=sec.session_vault_ref,
                access_token_secret_ref=sec.access_token_secret_ref,
                session_updated_at=sec.session_updated_at,
            )

        for pg in m.pages:
            account.pages.append(
                Page(
                    id=pg.id,
                    account_id=account.id,
                    platform_page_id=pg.platform_page_id,
                    name=pg.name,
                    category=pg.category,
                    profile_url=pg.profile_url,
                    followers=pg.followers,
                    status=pg.status,
                    publishing_enabled=pg.publishing_enabled,
                    last_synced_at=pg.last_synced_at,
                    last_published_at=pg.last_published_at,
                    notes=pg.notes,
                )
            )

        for gr in m.groups:
            account.groups.append(
                Group(
                    id=gr.id,
                    account_id=account.id,
                    platform_group_id=gr.platform_group_id,
                    name=gr.name,
                    role=gr.role,
                    members=gr.members,
                    posting_permission=gr.posting_permission,
                    last_synced_at=gr.last_synced_at,
                    notes=gr.notes,
                )
            )

        return account
