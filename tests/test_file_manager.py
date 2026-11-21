
import re

import pytest

from prevention_engine import file_manager


def test_save_redacted_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_manager,
        "REDACTED_DIRECTORY",
        tmp_path
    )

    content = "Email: [REDACTED:EMAIL]"

    file_id, file_path = file_manager.save_redacted_file(content)

    assert re.fullmatch(r"[a-f0-9]{32}", file_id)
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == content


def test_get_existing_redacted_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_manager,
        "REDACTED_DIRECTORY",
        tmp_path
    )

    file_id, saved_path = file_manager.save_redacted_file(
        "Password: [REDACTED:PASSWORD]"
    )

    retrieved_path = file_manager.get_redacted_file(file_id)

    assert retrieved_path == saved_path
    assert retrieved_path.exists()


def test_invalid_file_id(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_manager,
        "REDACTED_DIRECTORY",
        tmp_path
    )

    with pytest.raises(ValueError):
        file_manager.get_redacted_file("../invalid")


def test_missing_redacted_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        file_manager,
        "REDACTED_DIRECTORY",
        tmp_path
    )

    valid_id = "a" * 32

    with pytest.raises(FileNotFoundError):
        file_manager.get_redacted_file(valid_id)
