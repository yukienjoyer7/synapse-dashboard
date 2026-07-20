"""Native Streamlit table patterns with pagination and row selection."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

import pandas as pd
import streamlit as st

from dashboard.components.healthops_ui import mount_healthops_ui
from dashboard.state import set_selected_hospital


def render_paginated_table(
    dataframe: pd.DataFrame,
    *,
    key: str,
    column_config: Mapping[str, Any] | None = None,
    column_order: Iterable[str] | None = None,
    page_size: int = 15,
    selectable: bool = True,
    height: int = 520,
) -> str | None:
    """Render a native table page and return a selected hospital ID when available."""
    if dataframe.empty:
        st.caption("Tidak ada baris untuk ditampilkan.")
        return None

    page_count = max(1, (len(dataframe) + page_size - 1) // page_size)
    page = st.pagination(page_count, key=f"table_page_{key}")
    start = (page - 1) * page_size
    visible = dataframe.iloc[start : start + page_size].reset_index(drop=True)
    kwargs: dict[str, Any] = {
        "data": visible,
        "column_config": column_config,
        "column_order": column_order,
        "hide_index": True,
        "width": "stretch",
        "height": height,
        "placeholder": "—",
        "key": f"table_selection_{key}",
    }
    if selectable and "id_rumah_sakit" in visible.columns:
        kwargs.update(on_select="rerun", selection_mode="single-row")
    event = st.dataframe(**kwargs)

    hospital_id = None
    if selectable and "id_rumah_sakit" in visible.columns:
        rows = getattr(getattr(event, "selection", None), "rows", [])
        if rows:
            selected = visible.iloc[rows[0]]
            hospital_id = str(selected["id_rumah_sakit"])
            set_selected_hospital(hospital_id, str(selected.get("nama_rumah_sakit", "")))

    mount_healthops_ui(
        "table_footer",
        {
            "start": start + 1,
            "end": start + len(visible),
            "total": len(dataframe),
            "page": page,
            "pages": page_count,
            "selectable": selectable and "id_rumah_sakit" in visible.columns,
        },
        key=f"healthops-table-footer-{key}",
    )
    return hospital_id
