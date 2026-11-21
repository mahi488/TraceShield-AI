from prevention_engine.redactor import redact_sensitive_data


def test_redact_email():
    text = "Contact alex@example.com for support."

    findings = [{
        "type": "EMAIL",
        "value": "alex@example.com",
        "start": 8,
        "end": 24
    }]

    result = redact_sensitive_data(text, findings)

    assert result == "Contact [REDACTED:EMAIL] for support."


def test_redact_multiple_findings():
    text = "Email: alex@example.com Phone: 9876543210"

    findings = [
        {
            "type": "EMAIL",
            "value": "alex@example.com",
            "start": 7,
            "end": 23
        },
        {
            "type": "PHONE",
            "value": "9876543210",
            "start": 31,
            "end": 41
        }
    ]

    result = redact_sensitive_data(text, findings)

    assert "[REDACTED:EMAIL]" in result
    assert "[REDACTED:PHONE]" in result
    assert "alex@example.com" not in result
    assert "9876543210" not in result


def test_redact_without_findings():
    text = "This is a normal message."

    result = redact_sensitive_data(text, [])

    assert result == text


def test_invalid_finding_is_ignored():
    text = "Contact alex@example.com"

    findings = [{
        "type": "EMAIL",
        "value": "wrong@example.com",
        "start": 8,
        "end": 25
    }]

    result = redact_sensitive_data(text, findings)

    assert result == text