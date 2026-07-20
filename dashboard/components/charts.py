"""Shared rendering and selection behavior for Plotly figures."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st

from dashboard.components.healthops_ui import mount_healthops_ui
from dashboard.state import set_selected_hospital

PLOTLY_CONFIG = {
    "displaylogo": False,
    "displayModeBar": "hover",
    "responsive": True,
    "scrollZoom": False,
    "modeBarButtonsToRemove": [
        "autoScale2d",
        "lasso2d",
        "pan2d",
        "select2d",
        "zoom2d",
        "zoomIn2d",
        "zoomOut2d",
    ],
    "toImageButtonOptions": {"format": "png", "filename": "synapse-healthops-chart"},
}


def _selected_hospital_id(event: Any) -> str | None:
    points = getattr(getattr(event, "selection", None), "points", [])
    if not points:
        return None
    customdata = points[0].get("customdata")
    if isinstance(customdata, (list, tuple)):
        customdata = customdata[0] if customdata else None
    return str(customdata) if customdata else None


def render_chart(
    figure: go.Figure,
    *,
    title: str,
    subtitle: str,
    insight: str,
    key: str,
    selectable: bool = False,
) -> str | None:
    """Render an analytical chart card and optionally persist point selection."""
    with st.container(border=True, key=f"{key}-card"):
        mount_healthops_ui(
            "chart_header",
            {"title": title, "subtitle": subtitle, "label": "ANALISIS"},
            key=f"healthops-chart-header-{key}",
        )
        if selectable:
            event = st.plotly_chart(
                figure,
                theme=None,
                key=key,
                width="stretch",
                on_select="rerun",
                selection_mode="points",
                config=PLOTLY_CONFIG,
            )
            hospital_id = _selected_hospital_id(event)
            if hospital_id:
                set_selected_hospital(hospital_id)
        else:
            st.plotly_chart(
                figure,
                theme=None,
                key=key,
                width="stretch",
                config=PLOTLY_CONFIG,
            )
            hospital_id = None
        mount_healthops_ui(
            "chart_insight",
            {"insight": insight},
            key=f"healthops-chart-insight-{key}",
        )
    return hospital_id
