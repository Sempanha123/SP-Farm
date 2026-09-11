"""Unit tests for ErrorCenter repeated error grouping and multi-entity correlation tracing."""

from spfarm.application.services.error_center import ErrorCenterService


def test_repeated_error_grouping() -> None:
    svc = ErrorCenterService()

    # Trigger 5 errors with slightly different parameterized messages
    for i in range(5):
        try:
            raise ConnectionRefusedError(f"Failed connecting to ADB daemon on port {5555 + i} after attempt {i}")
        except Exception as exc:
            svc.record_error(
                exc,
                correlation_context={"job_id": f"job_{i}", "device_id": "emulator-5554"},
                location="adb_client.py:connect",
            )

    errors = svc.list_errors()
    # All 5 occurrences must be grouped into a single GroupedError
    assert len(errors) == 1
    grouped = errors[0]
    assert grouped.error_type == "ConnectionRefusedError"
    assert grouped.count == 5
    assert grouped.status == "active"
    assert len(grouped.correlated_job_ids) == 5
    assert grouped.correlated_device_ids == {"emulator-5554"}


def test_multi_entity_correlation_trace() -> None:
    """Acceptance criteria: Trace Job -> Environment -> Device -> Account."""
    svc = ErrorCenterService()

    ctx = {
        "job_id": "job_campaign_daily_01",
        "environment_id": "env_pixel7_us_profile",
        "device_id": "device_ldplayer_instance_02",
        "account_id": "account_corporate_marketing",
        "page_id": "page_sp_enterprise",
    }

    try:
        raise TimeoutError("Appium session command timed out after 60 seconds")
    except Exception as exc:
        err = svc.record_error(exc, correlation_context=ctx, location="session_runner.py:execute")

    trace = svc.trace_error(err.fingerprint)
    assert trace is not None
    chain = trace["trace_chain"]

    # Verify complete chain: Job -> Environment -> Device -> Account
    assert chain["jobs"] == ["job_campaign_daily_01"]
    assert chain["environments"] == ["env_pixel7_us_profile"]
    assert chain["devices"] == ["device_ldplayer_instance_02"]
    assert chain["accounts"] == ["account_corporate_marketing"]
    assert chain["pages"] == ["page_sp_enterprise"]


def test_error_lifecycle_transitions() -> None:
    svc = ErrorCenterService()

    err = svc.record_error("Test application exception", location="worker.py:run")
    assert err.status == "active"

    # Acknowledge
    assert svc.acknowledge_error(err.fingerprint) is True
    assert svc.get_error(err.fingerprint).status == "acknowledged"

    # Resolve
    assert svc.resolve_error(err.fingerprint) is True
    assert svc.get_error(err.fingerprint).status == "resolved"

    # Recurring error reactivates resolved error
    reactivated = svc.record_error("Test application exception", location="worker.py:run")
    assert reactivated.status == "active"
    assert reactivated.count == 2
