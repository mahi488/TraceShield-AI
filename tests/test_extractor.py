
import pytest

from detection_engine import extractor


def test_extract_txt_file():
    result = extractor.extract_text(
        b"Hello TraceShield",
        "sample.txt"
    )
    assert result == "Hello TraceShield"


def test_extract_txt_with_utf8_bom():
    result = extractor.extract_text(
        b"\xef\xbb\xbfHello TraceShield",
        "sample.txt"
    )
    assert result == "Hello TraceShield"


def test_extract_csv_file():
    result = extractor.extract_text(
        b"name,email\nAlice,alice@example.com",
        "users.csv"
    )
    assert result == "name, email\nAlice, alice@example.com"


def test_extract_json_file():
    result = extractor.extract_text(
        b'{"name":"Alice","active":true}',
        "users.json"
    )
    assert '"name": "Alice"' in result
    assert '"active": true' in result


def test_extract_invalid_json():
    with pytest.raises(ValueError, match="invalid JSON format"):
        extractor.extract_text(
            b'{"name":',
            "users.json"
        )


def test_extract_invalid_text_encoding():
    with pytest.raises(ValueError, match="unsupported text encoding"):
        extractor.extract_text(
            b"\xff\xfe\xfa",
            "sample.txt"
        )


def test_extract_empty_content():
    with pytest.raises(ValueError, match="empty"):
        extractor.extract_text(b"", "sample.txt")


def test_extract_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported extraction format"):
        extractor.extract_text(
            b"sample content",
            "sample.exe"
        )


def test_extract_pdf_text(monkeypatch):
    class FakePage:
        def extract_text(self):
            return "PDF test content"

    class FakeReader:
        is_encrypted = False
        pages = [FakePage()]

        def __init__(self, stream):
            self.stream = stream

    monkeypatch.setattr(extractor, "PdfReader", FakeReader)

    result = extractor.extract_text(
        b"fake pdf content",
        "sample.pdf"
    )

    assert result == "PDF test content"


def test_extract_encrypted_pdf(monkeypatch):
    class FakeReader:
        is_encrypted = True

        def __init__(self, stream):
            self.stream = stream

    monkeypatch.setattr(extractor, "PdfReader", FakeReader)

    with pytest.raises(ValueError, match="Encrypted PDF"):
        extractor.extract_text(
            b"fake pdf content",
            "sample.pdf"
        )


def test_extract_invalid_pdf(monkeypatch):
    class FakeReader:
        def __init__(self, stream):
            raise RuntimeError("internal parser detail")

    monkeypatch.setattr(extractor, "PdfReader", FakeReader)

    with pytest.raises(ValueError, match="PDF extraction failed"):
        extractor.extract_text(
            b"invalid pdf content",
            "sample.pdf"
        )
