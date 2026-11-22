
from detection_engine.detector import detect_sensitive_data


# Existing detection tests

def test_detect_email():
    findings = detect_sensitive_data("Contact alex@example.com")
    assert any(item["type"] == "EMAIL" for item in findings)


def test_detect_phone():
    findings = detect_sensitive_data("Phone: 9876543210")
    assert any(item["type"] == "PHONE" for item in findings)


def test_detect_pan():
    findings = detect_sensitive_data("PAN: ABCDE1234F")
    assert any(item["type"] == "PAN" for item in findings)


def test_detect_aadhaar_like():
    findings = detect_sensitive_data("Number: 1234 5678 9012")
    assert any(item["type"] == "AADHAAR_LIKE" for item in findings)


def test_detect_ip_address():
    findings = detect_sensitive_data("Server: 192.168.1.10")
    assert any(item["type"] == "IP_ADDRESS" for item in findings)


def test_detect_password():
    findings = detect_sensitive_data("password = test123")
    assert any(item["type"] == "PASSWORD" for item in findings)


def test_detect_api_key():
    findings = detect_sensitive_data("api_key = abc123xyz")
    assert any(item["type"] == "API_KEY" for item in findings)


def test_no_sensitive_data():
    findings = detect_sensitive_data("Hello, welcome to TraceShield AI")
    assert findings == []


# New detection tests

def test_detect_credit_card():
    findings = detect_sensitive_data(
        "Card: 4111 1111 1111 1111"
    )
    assert any(item["type"] == "CREDIT_CARD" for item in findings)


def test_detect_date_of_birth():
    findings = detect_sensitive_data(
        "DOB: 2004-05-21"
    )
    assert any(item["type"] == "DATE_OF_BIRTH" for item in findings)


def test_detect_aws_access_key():
    findings = detect_sensitive_data(
        "AWS key: AKIAIOSFODNN7EXAMPLE"
    )
    assert any(item["type"] == "AWS_ACCESS_KEY" for item in findings)


def test_detect_jwt_token():
    findings = detect_sensitive_data(
        "Token: eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbGV4In0.signature123"
    )
    assert any(item["type"] == "JWT_TOKEN" for item in findings)
def test_detect_api_key_with_space():
    findings = detect_sensitive_data(
        "API Key: test_api_key_12345"
    )
    assert any(
        item["type"] == "API_KEY"
        for item in findings
    )
    # Regression test: prevent credit card from being detected as Aadhaar

def test_credit_card_not_detected_as_aadhaar():
    findings = detect_sensitive_data(
        "Card: 4111 1111 1111 1111"
    )

    assert any(
        item["type"] == "CREDIT_CARD"
        for item in findings
    )

    assert not any(
        item["type"] == "AADHAAR_LIKE"
        for item in findings
    )

# Phase 2 regression tests

def test_valid_ipv4_address():
    findings = detect_sensitive_data("Server: 192.168.1.10")

    assert any(
        item["type"] == "IP_ADDRESS"
        for item in findings
    )


def test_invalid_ipv4_address_is_ignored():
    findings = detect_sensitive_data("Server: 999.999.999.999")

    assert not any(
        item["type"] == "IP_ADDRESS"
        for item in findings
    )


def test_valid_credit_card_passes_luhn():
    findings = detect_sensitive_data(
        "Card: 4111 1111 1111 1111"
    )

    assert any(
        item["type"] == "CREDIT_CARD"
        for item in findings
    )


def test_invalid_credit_card_fails_luhn():
    findings = detect_sensitive_data(
        "Card: 4111 1111 1111 1112"
    )

    assert not any(
        item["type"] == "CREDIT_CARD"
        for item in findings
    )


def test_aadhaar_like_number_is_still_detected():
    findings = detect_sensitive_data(
        "Number: 1234 5678 9012"
    )

    assert any(
        item["type"] == "AADHAAR_LIKE"
        for item in findings
    )


def test_credit_card_is_not_classified_as_aadhaar():
    findings = detect_sensitive_data(
        "Card: 4111 1111 1111 1111"
    )

    assert any(
        item["type"] == "CREDIT_CARD"
        for item in findings
    )

    assert not any(
        item["type"] == "AADHAAR_LIKE"
        for item in findings
    )
