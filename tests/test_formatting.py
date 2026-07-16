"""Indonesian-facing scalar formatting."""

from __future__ import annotations

import math

import pytest

from dashboard.utils.formatting import (
    MISSING_TEXT,
    format_days,
    format_decimal,
    format_integer,
    format_minutes,
    format_p_value,
    format_percentage,
    format_signed,
)


@pytest.mark.parametrize("value", [None, math.nan])
def test_missing_values_have_explicit_label(value: float | None) -> None:
    assert format_decimal(value) == MISSING_TEXT


def test_numbers_use_indonesian_separators_and_units() -> None:
    assert format_integer(1234.6) == "1.235"
    assert format_decimal(1234.56, 1) == "1.234,6"
    assert format_percentage(92.04, 1) == "92,0%"
    assert format_minutes(4.25, 1) == "4,2 menit"
    assert format_days(3.75, 1) == "3,8 hari"


def test_signed_and_p_value_formatting() -> None:
    assert format_signed(4.25, suffix=" pp") == "+4,2 pp"
    assert format_signed(-4.25, 2) == "-4,25"
    assert format_signed(0) == "0,0"
    assert format_p_value(0.00001) == "<0,001"
    assert format_p_value(0.1254) == "0,125"
