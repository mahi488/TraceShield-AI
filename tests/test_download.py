
from fastapi.testclient import TestClient

from backend.main import app
import backend.upload as upload_module


client = TestClient(app)


def test_download_redacted_file_success(tmp_path, monkeypatch):
    """A valid file ID should download the redacted file."""

    file_path = tmp_path / "redacted_test.txt"
    file_path.write_text(
        "Email: [REDACTED:EMAIL]",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        upload_module,
        "get_redacted_file",
        lambda file_id: file_path
    )

    response = client.get(
        "/api/redacted/12345678901234567890123456789012"
    )

    assert response.status_code == 200
    assert response.text == "Email: [REDACTED:EMAIL]"
    assert "attachment" in response.headers["content-disposition"]


def test_download_invalid_file_id():
    """An invalid file ID should return HTTP 400."""

    response = client.get("/api/redacted/invalid-id")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid redacted file ID"


def test_download_missing_file(tmp_path, monkeypatch):
    """A valid but nonexistent file ID should return HTTP 404."""

    def missing_file(file_id):
        raise FileNotFoundError("Redacted file not found")

    monkeypatch.setattr(
        upload_module,
        "get_redacted_file",
        missing_file
    )

    response = client.get(
        "/api/redacted/12345678901234567890123456789012"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Redacted file not found"
