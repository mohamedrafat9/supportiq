
import pytest

from app.services.text_cleaning import clean_text


def test_normalize_unicode():
    text = "cafe\u0301"

    result = clean_text(text)

    assert result == "café"


def test_normalize_line_endings():
    text = "First line\r\nSecond line\rThird line"

    result = clean_text(text)

    assert result == "First line\nSecond line\nThird line"


def test_remove_extra_spaces_and_tabs():
    text = "Hello    world\t\tSupportIQ"

    result = clean_text(text)

    assert result == "Hello world SupportIQ"


def test_preserve_paragraphs():
    text = "First paragraph\n\n\nSecond paragraph"

    result = clean_text(text)

    assert result == "First paragraph\n\nSecond paragraph"


def test_remove_control_characters():
    text = "Hello\x00World\x01SupportIQ"

    result = clean_text(text)

    assert result == "HelloWorldSupportIQ"


def test_remove_spaces_around_line_breaks():
    text = "  First line  \n  Second line  "

    result = clean_text(text)

    assert result == "First line\nSecond line"


def test_strip_outer_whitespace():
    text = "  SupportIQ text  \n"

    result = clean_text(text)

    assert result == "SupportIQ text"


def test_empty_string():
    assert clean_text("") == ""


def test_whitespace_only():
    assert clean_text("   \n\t  ") == ""


def test_reject_non_string_input():
    with pytest.raises(TypeError):
        clean_text(None)
