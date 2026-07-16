"""HealthOps Plotly color and layout conventions."""

from __future__ import annotations

import plotly.graph_objects as go

COLORS = {
    "ink": "#212B32",
    "secondary": "#4C6272",
    "muted": "#768692",
    "grid": "#D8DDE0",
    "surface": "#FFFFFF",
    "primary": "#005EB8",
    "primary_dark": "#003087",
    "teal": "#007D79",
    "purple": "#6929C4",
    "cyan": "#1192E8",
    "success": "#006747",
    "watch": "#B28600",
    "danger": "#DA1E28",
    "critical": "#750E13",
    "unknown": "#AEB7BD",
}

CATEGORICAL = [
    "#005EB8",
    "#007D79",
    "#6929C4",
    "#1192E8",
    "#9F1853",
    "#198038",
    "#002D9C",
    "#B28600",
]

MATURITY_SCALE = [
    [0.00, "#EAF5FC"],
    [0.20, "#CDE6F7"],
    [0.40, "#8FCDEB"],
    [0.60, "#41B6E6"],
    [0.80, "#005EB8"],
    [1.00, "#003087"],
]

TIER_COLORS = {
    "Tier 1 — Inefisiensi Ganda": COLORS["danger"],
    "Tier 2 — Early Warning": COLORS["watch"],
    "Tier 3 — Monitoring": COLORS["unknown"],
}


def apply_chart_theme(figure: go.Figure, *, height: int = 420) -> go.Figure:
    """Apply the design system without constraining responsive width."""
    figure.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        font={
            "family": "Source Sans 3, Source Sans Pro, Arial, sans-serif",
            "color": COLORS["ink"],
            "size": 13,
        },
        margin={"l": 52, "r": 24, "t": 28, "b": 52},
        hoverlabel={
            "bgcolor": COLORS["surface"],
            "bordercolor": "#AEB7BD",
            "font": {"color": COLORS["ink"], "size": 13},
        },
        legend={"title": None, "orientation": "h", "y": -0.2},
        colorway=CATEGORICAL,
        clickmode="event+select",
        uirevision="healthops",
    )
    figure.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#AEB7BD",
        tickfont={"color": COLORS["secondary"]},
        title_font={"color": COLORS["secondary"]},
    )
    figure.update_yaxes(
        showgrid=True,
        gridcolor="#E8EDEE",
        zeroline=False,
        linecolor="#AEB7BD",
        tickfont={"color": COLORS["secondary"]},
        title_font={"color": COLORS["secondary"]},
    )
    return figure
