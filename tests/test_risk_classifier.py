
from ai_engine.risk_classifier import classify_risk


def test_low_risk():
    result = classify_risk([], 1)

    assert result["risk_level"] == "LOW"
    assert result["risk_score"] == 0


def test_medium_risk():
    result = classify_risk(["PASSWORD"], 1)

    assert result["risk_level"] == "MEDIUM"
    assert result["risk_score"] == 4


def test_high_risk():
    result = classify_risk(
        ["EMAIL", "USERNAME", "SESSION_TOKEN"],
        3
    )

    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] == 8


def test_critical_risk():
    result = classify_risk(
        ["PAN", "AADHAAR_LIKE", "API_KEY"],
        3
    )

    assert result["risk_level"] == "CRITICAL"
    assert result["risk_score"] == 12
