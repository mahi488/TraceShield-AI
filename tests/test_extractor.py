
import json
from io import BytesIO

from pypdf import PdfWriter

from detection_engine.extractor import extract_pdf_text, extract_text


def create_test_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)

    pdf_bytes = BytesIO()
    writer.write(pdf_bytes)

    return pdf_bytes.getvalue()


def test_extract_pdf_returns_string():
    result = extract_pdf_text(create_test_pdf())
    assert isinstance(result, str)


def test_extract_pdf_handles_empty_pdf_text():
    result = extract_pdf_text(create_test_pdf())
    assert result == ""


def test_extract_txt():
    content = b"Employee: Alex Kumar"
    result = extract_text(content, "test.txt")
    assert "Alex Kumar" in result


def test_extract_csv():
    content = b"username,email\nalex,alex@example.com"
    result = extract_text(content, "test.csv")
    assert "alex@example.com" in result


def test_extract_json():
    content = json.dumps({
        "username": "alex",
        "email": "alex@example.com"
    }).encode("utf-8")

    result = extract_text(content, "test.json")
    assert "alex@example.com" in result


def test_extract_python_file():
    content = b"password = 'test123'"
    result = extract_text(content, "test.py")
    assert "password" in result


def test_unsupported_file_format():
    try:
        extract_text(b"sample", "test.exe")
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "Unsupported extraction format" in str(error)
