"""Integration tests for SQLite WAL, SQLAlchemy 2 repositories, migrations, and backups."""

import concurrent.futures
from pathlib import Path

from spfarm.domain.accounts.models import (
    Account,
    AccountEmail,
    AccountPhone,
    AccountSecurity,
    Group,
    Page,
)
from spfarm.domain.enums import AccountHealthState, AccountStatus, TwoFactorMethod
from spfarm.infrastructure.database.backup import backup_database
from spfarm.infrastructure.database.migrator import apply_migrations
from spfarm.infrastructure.database.session import create_db_engine, create_session_factory
from spfarm.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork


def test_fresh_db_migrates_and_persists_account(tmp_path: Path) -> None:
    db_file = tmp_path / "test_spfarm.db"
    engine = create_db_engine(f"sqlite:///{db_file.as_posix()}")

    # 1. Apply schema migration
    apply_migrations(engine)
    session_factory = create_session_factory(engine)

    # 2. Persist full account aggregate using UnitOfWork
    account = Account(
        profile_id="fb-test-99",
        display_name="Enterprise User",
        status=AccountStatus.ACTIVE,
        health_state=AccountHealthState.HEALTHY,
    )
    account.add_email(AccountEmail(account_id=account.id, address="user@domain.com", is_primary=True))
    account.add_phone(AccountPhone(account_id=account.id, number="+15550001", is_primary=True))
    account.security = AccountSecurity(
        account_id=account.id,
        two_factor_enabled=True,
        two_factor_method=TwoFactorMethod.TOTP,
        password_secret_ref="vault://acc/pwd",
    )
    account.pages.append(Page(account_id=account.id, platform_page_id="page-101", name="Global Brand"))
    account.groups.append(Group(account_id=account.id, platform_group_id="grp-201", name="VIP Group"))

    with SqlAlchemyUnitOfWork(session_factory) as uow:
        uow.accounts.add(account)
        uow.commit()

    # 3. Read back in a new session and verify hydration
    with SqlAlchemyUnitOfWork(session_factory) as uow:
        loaded = uow.accounts.get_by_id(account.id)
        assert loaded is not None
        assert loaded.display_name == "Enterprise User"
        assert len(loaded.emails) == 1
        assert loaded.emails[0].address == "user@domain.com"
        assert len(loaded.phones) == 1
        assert loaded.phones[0].number == "+15550001"
        assert loaded.security is not None
        assert loaded.security.two_factor_enabled is True
        assert loaded.security.password_secret_ref == "vault://acc/pwd"
        assert len(loaded.pages) == 1
        assert loaded.pages[0].name == "Global Brand"
        assert len(loaded.groups) == 1
        assert loaded.groups[0].name == "VIP Group"


def test_transaction_rollback_on_error(tmp_path: Path) -> None:
    db_file = tmp_path / "test_rollback.db"
    engine = create_db_engine(f"sqlite:///{db_file.as_posix()}")
    apply_migrations(engine)
    session_factory = create_session_factory(engine)

    account = Account(profile_id="fb-rollback", display_name="Rollback Test")

    # Simulate an error inside the UnitOfWork block
    try:
        with SqlAlchemyUnitOfWork(session_factory) as uow:
            uow.accounts.add(account)
            # Raise exception before commit
            raise RuntimeError("Simulated mid-transaction failure")
    except RuntimeError:
        pass

    # Verify that the account was rolled back and never persisted
    with SqlAlchemyUnitOfWork(session_factory) as uow:
        loaded = uow.accounts.get_by_id(account.id)
        assert loaded is None


def test_concurrent_read_write_wal_smoke(tmp_path: Path) -> None:
    """Smoke test ensuring SQLite WAL handles concurrent multi-threaded reads and writes."""
    db_file = tmp_path / "test_wal_concurrent.db"
    engine = create_db_engine(f"sqlite:///{db_file.as_posix()}")
    apply_migrations(engine)
    session_factory = create_session_factory(engine)

    # Seed an initial account
    seed_acc = Account(profile_id="seed-001", display_name="Seed User")
    with SqlAlchemyUnitOfWork(session_factory) as uow:
        uow.accounts.add(seed_acc)
        uow.commit()

    def writer_task(writer_id: int) -> bool:
        with SqlAlchemyUnitOfWork(session_factory) as uow:
            acc = Account(profile_id=f"writer-{writer_id}", display_name=f"Writer {writer_id}")
            uow.accounts.add(acc)
            uow.commit()
        return True

    def reader_task() -> int:
        with SqlAlchemyUnitOfWork(session_factory) as uow:
            accounts = uow.accounts.list_all()
            return len(accounts)

    # Run concurrent reader and writer threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        write_futures = [executor.submit(writer_task, i) for i in range(10)]
        read_futures = [executor.submit(reader_task) for _ in range(15)]

        for wf in concurrent.futures.as_completed(write_futures):
            assert wf.result() is True

        for rf in concurrent.futures.as_completed(read_futures):
            assert rf.result() >= 1

    # Verify total accounts persisted
    with SqlAlchemyUnitOfWork(session_factory) as uow:
        total = len(uow.accounts.list_all())
        assert total == 11  # 1 seed + 10 writers


def test_database_online_backup(tmp_path: Path) -> None:
    db_file = tmp_path / "live.db"
    engine = create_db_engine(f"sqlite:///{db_file.as_posix()}")
    apply_migrations(engine)
    session_factory = create_session_factory(engine)

    # Insert test record
    with SqlAlchemyUnitOfWork(session_factory) as uow:
        uow.accounts.add(Account(profile_id="backup-test", display_name="Backup User"))
        uow.commit()

    # Perform online point-in-time backup
    backup_dir = tmp_path / "backups"
    backup_path = backup_database(
        source_db_path=db_file,
        dest_dir=backup_dir,
        backup_filename="test_snapshot.db",
    )

    assert backup_path.exists()
    assert backup_path.is_file()

    # Verify backup database can be opened and queried independently
    backup_engine = create_db_engine(f"sqlite:///{backup_path.as_posix()}")
    backup_session_factory = create_session_factory(backup_engine)
    with SqlAlchemyUnitOfWork(backup_session_factory) as uow:
        accounts = uow.accounts.list_all()
        assert len(accounts) == 1
        assert accounts[0].profile_id == "backup-test"
