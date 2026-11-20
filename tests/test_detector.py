
from detection_engine.detector import detect_sensitive_data


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
