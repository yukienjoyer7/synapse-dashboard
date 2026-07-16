"""Consistent Indonesian-facing number formatting."""

from __future__ import annotations

from numbers import Number

import pandas as pd

MISSING_TEXT = "Data tidak tersedia"


def is_missing(value: object) -> bool:
    """Return whether a scalar should be displayed as missing."""
    return value is None or bool(pd.isna(value))


def _localized_number(value: Number, decimals: int) -> str:
    formatted = f"{float(value):,.{decimals}f}"
    return formatted.replace(",", "_").replace(".", ",").replace("_", ".")


def format_integer(value: Number | None) -> str:
    return MISSING_TEXT if is_missing(value) else _localized_number(round(float(value)), 0)


def format_decimal(value: Number | None, decimals: int = 1) -> str:
    return MISSING_TEXT if is_missing(value) else _localized_number(value, decimals)


def format_percentage(value: Number | None, decimals: int = 1) -> str:
    return MISSING_TEXT if is_missing(value) else f"{_localized_number(value, decimals)}%"


def format_minutes(value: Number | None, decimals: int = 1) -> str:
    return MISSING_TEXT if is_missing(value) else f"{_localized_number(value, decimals)} menit"


def format_days(value: Number | None, decimals: int = 1) -> str:
    return MISSING_TEXT if is_missing(value) else f"{_localized_number(value, decimals)} hari"


def format_score(value: Number | None, decimals: int = 1, scale: float = 1.0) -> str:
    if is_missing(value):
        return MISSING_TEXT
    return _localized_number(float(value) * scale, decimals)


def format_currency_idr_million(value: Number | None, decimals: int = 1) -> str:
    return MISSING_TEXT if is_missing(value) else f"Rp{_localized_number(value, decimals)} juta"


def format_signed(value: Number | None, decimals: int = 1, suffix: str = "") -> str:
    if is_missing(value):
        return MISSING_TEXT
    numeric = float(value)
    sign = "+" if numeric > 0 else ""
    return f"{sign}{_localized_number(numeric, decimals)}{suffix}"


def format_p_value(value: Number | None) -> str:
    if is_missing(value):
        return MISSING_TEXT
    numeric = float(value)
    if numeric < 0.001:
        return "<0,001"
    return _localized_number(numeric, 3)
