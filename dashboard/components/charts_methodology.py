"""Data-quality visualizations for the methodology page."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from dashboard.components.chart_theme import COLORS, apply_chart_theme


def build_missingness_chart(data_quality: pd.DataFrame) -> go.Figure:
    """Rank source variables by persisted pre-cleaning missingness."""
    ranked = data_quality.sort_values(["missing_pct", "variabel"], ascending=[True, True]).copy()
    colors = [
        COLORS["watch"] if value > 0 else COLORS["primary"] for value in ranked["missing_pct"]
    ]
    figure = go.Figure(
        go.Bar(
            x=ranked["missing_pct"],
            y=ranked["variabel"],
            orientation="h",
            marker_color=colors,
            customdata=ranked[["missing_count", "unique_count", "dtype"]].to_numpy(),
            text=ranked["missing_pct"].map(lambda value: f"{value:.1f}%"),
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>Missing: %{customdata[0]} (%{x:.2f}%)<br>"
                "Nilai unik: %{customdata[1]}<br>Tipe: %{customdata[2]}<extra></extra>"
            ),
        )
    )
    figure.update_xaxes(range=[0, max(3.4, ranked["missing_pct"].max() * 1.2)])
    figure.update_xaxes(title="Persentase missing pada data sumber", ticksuffix="%")
    figure.update_yaxes(title=None)
    return apply_chart_theme(figure, height=660)
