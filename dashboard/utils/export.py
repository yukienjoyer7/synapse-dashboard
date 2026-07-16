"""Metadata-aware CSV exports for auditable dashboard handoffs."""

from __future__ import annotations

from datetime import UTC, datetime

import pandas as pd
import streamlit as st

METADATA_COLUMNS = [
    "export_timestamp_utc",
    "active_filters",
    "benchmark_definition",
    "data_version",
]


def prepare_csv_export(
    dataframe: pd.DataFrame,
    *,
    active_filters: str,
    benchmark_definition: str,
    data_version: str,
    timestamp: datetime | None = None,
) -> bytes:
    """Return a UTF-8 BOM CSV with provenance repeated on every exported row."""
    exported = dataframe.copy()
    exported["export_timestamp_utc"] = (timestamp or datetime.now(UTC)).isoformat()
    exported["active_filters"] = active_filters
    exported["benchmark_definition"] = benchmark_definition
    exported["data_version"] = data_version
    original_columns = [column for column in dataframe.columns if column not in METADATA_COLUMNS]
    exported = exported[METADATA_COLUMNS + original_columns]
    return exported.to_csv(index=False, lineterminator="\n").encode("utf-8-sig")


def render_csv_download(
    dataframe: pd.DataFrame,
    *,
    label: str,
    filename: str,
    key: str,
    active_filters: str,
    benchmark_definition: str,
    data_version: str,
) -> None:
    """Render one consistent download button with embedded audit metadata."""
    st.download_button(
        label,
        data=prepare_csv_export(
            dataframe,
            active_filters=active_filters,
            benchmark_definition=benchmark_definition,
            data_version=data_version,
        ),
        file_name=filename,
        mime="text/csv",
        key=key,
        icon=":material/download:",
        on_click="ignore",
    )
