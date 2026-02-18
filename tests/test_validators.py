import pytest
from src.utils.validators import _is_valid_date

def test_is_valid_date_empty():
    assert _is_valid_date(None) is False
    assert _is_valid_date("") is False
    assert _is_valid_date(" ") is False

def test_is_valid_date_present():
    assert _is_valid_date("present") is True
    assert _is_valid_date("Present") is True
    assert _is_valid_date("PRESENT") is True
    assert _is_valid_date(" present ") is True

def test_is_valid_date_year_only():
    assert _is_valid_date("2023") is True
    assert _is_valid_date("1999") is True
    assert _is_valid_date("202") is False
    assert _is_valid_date("20233") is False
    assert _is_valid_date("abcd") is False

def test_is_valid_date_month_year():
    assert _is_valid_date("Jan 2023") is True
    assert _is_valid_date("jan 2023") is True
    assert _is_valid_date("JAN 2023") is True
    assert _is_valid_date("Feb 2024") is True
    assert _is_valid_date("Dec 2022") is True

def test_is_valid_date_full_month_name():
    # These currently fail but should probably be supported for better reliability
    assert _is_valid_date("January 2023") is True
    assert _is_valid_date("September 2023") is True

def test_is_valid_date_common_abbreviations():
    # "Sept" is a common 4-letter abbreviation for September
    assert _is_valid_date("Sept 2023") is True

def test_is_valid_date_invalid_month():
    assert _is_valid_date("Invalid 2023") is False
    assert _is_valid_date("12 2023") is False

def test_is_valid_date_invalid_year_with_month():
    assert _is_valid_date("Jan 23") is False
    assert _is_valid_date("Jan 20234") is False
    assert _is_valid_date("Jan abcd") is False

def test_is_valid_date_other_invalid_formats():
    assert _is_valid_date("Jan 2023 extra") is False
    assert _is_valid_date("2023 Jan") is False
    assert _is_valid_date("Jan-2023") is False
