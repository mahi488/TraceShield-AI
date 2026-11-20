
from correlation_engine.correlator import correlate_artifacts


def test_correlate_identity_across_three_files():
    artifacts = [
        {
            "filename": "employee.txt",
            "text": "Contact: alex@example.com"
        },
        {
            "filename": "users.txt",
            "text": "username=alex"
        },
        {
            "filename": "sessions.json",
            "text": '{"username": "alex", "session_token": "abc123xyz987"}'
        }
    ]

    results = correlate_artifacts(artifacts)

    assert len(results) == 1
    assert results[0]["matched_identity"] == "a***"
    assert len(results[0]["related_files"]) == 3
    assert results[0]["risk_level"] == "HIGH"
    assert "SESSION_TOKEN" in results[0]["evidence_types"]


def test_no_correlation_for_unrelated_artifacts():
    artifacts = [
        {
            "filename": "employee.txt",
            "text": "Contact: alex@example.com"
        },
        {
            "filename": "users.txt",
            "text": "username=john"
        }
    ]

    results = correlate_artifacts(artifacts)

    assert results == []
