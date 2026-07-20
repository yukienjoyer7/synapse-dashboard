"""HealthOps Plotly color and layout conventions."""

from __future__ import annotations

import plotly.graph_objects as go

COLORS = {
    "ink": "#212B32",
    "secondary": "#4C6272",
    "muted": "#768692",
    "grid": "#E8EDEE",
    "surface": "#FFFFFF",
    "primary": "#1F4F3F",
    "primary_dark": "#2A6354",
    "teal": "#3C7863",
    "lime": "#9DC03F",
    "purple": "#6929C4",
    "cyan": "#1192E8",
    "success": "#006747",
    "watch": "#B28600",
    "danger": "#A2191F",
    "critical": "#750E13",
    "unknown": "#AEB7BD",
}

CATEGORICAL = [
    "#1F4F3F",
    "#3C7863",
    "#6929C4",
    "#1192E8",
    "#9F1853",
    "#198038",
    "#002D9C",
    "#B28600",
]

MATURITY_SCALE = [
    [0.00, "#EFF4F3"],
    [0.20, "#9AB9AE"],
    [0.40, "#457E6A"],
    [0.60, "#306A59"],
    [0.80, "#265C4D"],
    [1.00, "#1F4F3F"],
]

TIER_COLORS = {
    "Tier 1 — Inefisiensi Ganda": COLORS["danger"],
    "Tier 2 — Early Warning": COLORS["watch"],
    "Tier 3 — Monitoring": COLORS["unknown"],
}


LEGEND_LABEL_MAX_LENGTH = 26


def shorten_label(text: str, max_length: int = LEGEND_LABEL_MAX_LENGTH) -> str:
    """Drop a trailing ' — qualifier' clause and cap the length for legend display.

    Plotly can't wrap a single legend entry or axis tick onto a second line, so a long
    category name gets silently clipped by the chart card's overflow:hidden on narrow
    widths. The em-dash qualifier is always redundant with the KPI card, table column, or
    insight sentence next to the chart. The length cap is a safety net so any category
    name, current or future, stays inside the width that fits on a 360px-wide chart card.
    """
    if not isinstance(text, str):
        return text
    short = text.split(" — ", 1)[0]
    if len(short) > max_length:
        short = short[: max_length - 1].rstrip() + "…"
    return short


def apply_chart_theme(figure: go.Figure, *, height: int = 420) -> go.Figure:
    """Apply the design system without constraining responsive width."""
    figure.for_each_trace(
        lambda trace: trace.update(name=shorten_label(trace.name)) if trace.name else None
    )
    figure.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor=COLORS["surface"],
        plot_bgcolor=COLORS["surface"],
        font={
            "family": "Source Sans 3, Source Sans Pro, Arial, sans-serif",
            "color": COLORS["ink"],
            "size": 12,
        },
        margin={"l": 46, "r": 18, "t": 22, "b": 48},
        hoverlabel={
            "bgcolor": COLORS["surface"],
            "bordercolor": "#D8DDE0",
            "font": {"color": COLORS["ink"], "size": 12},
            "align": "left",
            "namelength": -1,
        },
        legend={
            "title": None,
            "orientation": "v",
            "x": 0,
            "xanchor": "left",
            "y": -0.14,
            "yanchor": "top",
            "font": {"color": COLORS["secondary"], "size": 11},
            "itemclick": "toggle",
            "itemdoubleclick": "toggleothers",
        },
        colorway=CATEGORICAL,
        clickmode="event+select",
        hovermode="closest",
        separators=",.",
        uniformtext={"minsize": 10, "mode": "hide"},
        uirevision="healthops",
    )
    figure.update_xaxes(
        showgrid=False,
        showline=True,
        zeroline=False,
        linecolor=COLORS["grid"],
        linewidth=1,
        ticks="outside",
        ticklen=4,
        tickcolor=COLORS["grid"],
        tickfont={"color": COLORS["secondary"], "size": 11},
        title_font={"color": COLORS["secondary"], "size": 12},
        automargin=True,
    )
    figure.update_yaxes(
        showgrid=True,
        gridcolor=COLORS["grid"],
        gridwidth=1,
        showline=False,
        zeroline=False,
        tickfont={"color": COLORS["secondary"], "size": 11},
        title_font={"color": COLORS["secondary"], "size": 12},
        automargin=True,
    )
    return figure
