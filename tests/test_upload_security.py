
from fastapi.testclient import TestClient

from backend.main import app
import backend.upload as upload_module


client = TestClient(app)


def test_sanitize_filename_removes_path_traversal():
    result = upload_module.sanitize_filename(
        "../../private/employee.txt"
    )

    assert result == "employee.txt"


def test_sanitize_filename_handles_windows_paths():
    result = upload_module.sanitize_filename(
        r"..\..\private\employee.txt"
    )

    assert result == "employee.txt"


def test_sanitize_filename_removes_control_characters():
    result = upload_module.sanitize_filename(
        "employee\x00.txt"
    )

    assert result == "employee.txt"


def test_sanitize_filename_rejects_empty_name():
    try:
        upload_module.sanitize_filename("...")
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_sanitize_filename_limits_length():
    result = upload_module.sanitize_filename(
        "a" * 300 + ".txt"
    )

    assert len(result) == 255


def test_upload_rejects_unsupported_extension():
    response = client.post(
        "/api/upload",
        files=[
            ("files", ("malware.exe", b"sample content"))
        ]
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported file type"


def test_upload_rejects_empty_file():
    response = client.post(
        "/api/upload",
        files=[
            ("files", ("empty.txt", b""))
        ]
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty"


def test_upload_rejects_oversized_file():
    oversized_content = b"A" * (
        upload_module.MAX_FILE_SIZE + 1
    )

    response = client.post(
        "/api/upload",
        files=[
            ("files", ("large.txt", oversized_content))
        ]
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "File exceeds 10 MB limit"


def test_upload_sanitizes_filename_before_processing(monkeypatch):
    captured = {}

    def fake_extract_text(content, filename):
        captured["filename"] = filename
        return content.decode("utf-8")

    monkeypatch.setattr(
        upload_module,
        "extract_text",
        fake_extract_text
    )

    monkeypatch.setattr(
        upload_module,
        "detect_sensitive_data",
        lambda text: []
    )

    monkeypatch.setattr(
        upload_module,
        "redact_sensitive_data",
        lambda text, findings: text
    )

    monkeypatch.setattr(
        upload_module,
        "save_redacted_file",
        lambda content: (
            "12345678901234567890123456789012",
            None
        )
    )

    response = client.post(
        "/api/upload",
        files=[
            (
                "files",
                ("../../private/employee.txt", b"Safe test content")
            )
        ]
    )

    assert response.status_code == 200
    assert captured["filename"] == "employee.txt"
    assert response.json()["files"][0]["filename"] == "employee.txt"
