"""Operational association and burden-profile charts."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dashboard.components.chart_theme import CATEGORICAL, COLORS, apply_chart_theme

MATURITY_ORDER = ["Rendah", "Menengah", "Tinggi"]


def build_adjusted_coefficients(associations: pd.DataFrame) -> go.Figure:
    """Plot the persisted combined-model estimates with robust confidence intervals."""
    combined = associations.loc[associations["model"].eq("Gabungan")].copy()
    combined["error_plus"] = combined["ci_95_high"] - combined["coefficient"]
    combined["error_minus"] = combined["coefficient"] - combined["ci_95_low"]
    figure = go.Figure(
        go.Scatter(
            x=combined["coefficient"],
            y=combined["term_label"],
            mode="markers",
            marker={"size": 12, "color": COLORS["primary"]},
            error_x={
                "type": "data",
                "array": combined["error_plus"],
                "arrayminus": combined["error_minus"],
                "color": COLORS["secondary"],
                "thickness": 2,
                "width": 6,
            },
            customdata=combined[["ci_95_low", "ci_95_high", "p_value"]].to_numpy(),
            hovertemplate=(
                "<b>%{y}</b><br>Perubahan estimasi: %{x:+.2f} menit<br>"
                "95% CI: %{customdata[0]:+.2f} hingga %{customdata[1]:+.2f}<br>"
                "p: %{customdata[2]:.3g}<extra></extra>"
            ),
        )
    )
    figure.add_vline(x=0, line_dash="dash", line_color=COLORS["secondary"])
    figure.update_xaxes(title="Perubahan estimasi waktu respons rujukan (menit)")
    figure.update_yaxes(title=None, autorange="reversed")
    return apply_chart_theme(figure, height=360)


def build_maturity_referral_scatter(dataframe: pd.DataFrame) -> go.Figure:
    """Show hospital-level maturity and referral response without fitting a runtime model."""
    plot_data = dataframe.dropna(
        subset=["skor_kematangan_digital", "rata_rata_waktu_respons_rujukan_menit"]
    )
    figure = px.scatter(
        plot_data,
        x="skor_kematangan_digital",
        y="rata_rata_waktu_respons_rujukan_menit",
        color="kelas_rumah_sakit",
        color_discrete_sequence=CATEGORICAL,
        custom_data=[
            "id_rumah_sakit",
            "nama_rumah_sakit",
            "kelas_rumah_sakit",
            "tingkat_keterisian_tempat_tidur_persen",
            "rata_rata_lama_rawat_hari",
        ],
        labels={
            "skor_kematangan_digital": "Skor kematangan digital",
            "rata_rata_waktu_respons_rujukan_menit": "Waktu respons rujukan (menit)",
            "kelas_rumah_sakit": "Kelas",
        },
    )
    figure.update_traces(
        marker={"size": 8, "opacity": 0.72, "line": {"color": "white", "width": 0.6}},
        hovertemplate=(
            "<b>%{customdata[1]}</b><br>ID: %{customdata[0]} · "
            "Kelas %{customdata[2]}<br>Kematangan: %{x:.1f}<br>"
            "Respons rujukan: %{y:.1f} menit<br>BOR: %{customdata[3]:.1f}%<br>"
            "LOS: %{customdata[4]:.1f} hari<extra></extra>"
        ),
    )
    figure.add_vline(
        x=plot_data["skor_kematangan_digital"].median(),
        line_dash="dot",
        line_color=COLORS["muted"],
    )
    figure.add_hline(
        y=plot_data["rata_rata_waktu_respons_rujukan_menit"].median(),
        line_dash="dot",
        line_color=COLORS["muted"],
    )
    return apply_chart_theme(figure, height=500)


def build_maturity_outcome_medians(outcomes: pd.DataFrame) -> go.Figure:
    """Render notebook-persisted maturity-tertile medians on outcome-specific scales."""
    figure = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=outcomes["outcome"].tolist(),
        vertical_spacing=0.24,
        horizontal_spacing=0.14,
    )
    median_columns = [
        "median_maturity_rendah",
        "median_maturity_menengah",
        "median_maturity_tinggi",
    ]
    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for (index, outcome), (row, column) in zip(
        outcomes.reset_index(drop=True).iterrows(), positions, strict=True
    ):
        values = outcome[median_columns].astype(float).tolist()
        figure.add_trace(
            go.Scatter(
                x=MATURITY_ORDER,
                y=values,
                mode="lines+markers",
                line={"color": CATEGORICAL[index], "width": 2},
                marker={"size": 9},
                customdata=[[outcome["arah_interpretasi"]]] * 3,
                hovertemplate=("%{x}<br>Median: %{y:.2f}<br>%{customdata[0]}<extra></extra>"),
                showlegend=False,
            ),
            row=row,
            col=column,
        )
    figure.update_xaxes(
        categoryorder="array", categoryarray=MATURITY_ORDER, title=None, tickangle=-30
    )
    figure.update_yaxes(title=None)
    return apply_chart_theme(figure, height=560)


def build_operational_heatmap(dataframe: pd.DataFrame) -> go.Figure:
    """Aggregate precomputed within-class burden percentiles by maturity cohort."""
    components = {
        "referral_burden": "Respons rujukan",
        "bor_burden": "Deviasi BOR",
        "los_burden": "LOS",
        "workload_burden": "Beban kerja",
        "operational_burden_score": "Beban gabungan",
    }
    grouped = (
        dataframe.groupby("maturity_tertile", observed=True)[list(components)]
        .mean()
        .reindex(MATURITY_ORDER)
        .dropna(how="all")
    )
    figure = go.Figure(
        go.Heatmap(
            z=grouped.to_numpy(),
            x=list(components.values()),
            y=grouped.index,
            zmin=0,
            zmax=1,
            colorscale=[
                [0.0, "#EFF4F3"],
                [0.5, "#457E6A"],
                [0.75, COLORS["watch"]],
                [1.0, COLORS["danger"]],
            ],
            text=grouped.to_numpy(),
            texttemplate="%{text:.0%}",
            colorbar={"title": "Beban", "tickformat": ".0%"},
            hovertemplate="%{y}<br>%{x}: %{z:.1%}<extra></extra>",
        )
    )
    figure.update_xaxes(title=None)
    figure.update_yaxes(title="Tertile kematangan", autorange="reversed")
    return apply_chart_theme(figure, height=420)
