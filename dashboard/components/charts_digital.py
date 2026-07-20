"""Charts for digital readiness and investment conversion."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.components.chart_theme import CATEGORICAL, COLORS, apply_chart_theme

SEGMENT_COLORS = {
    "Investor Digital Efektif": COLORS["teal"],
    "Pemimpin Efisien Sumber Daya": COLORS["primary"],
    "Pemantauan Konversi Investasi": COLORS["watch"],
    "Outlier Konversi Investasi — definisi ketat": COLORS["danger"],
    "Keterbatasan Sumber Daya": COLORS["unknown"],
}


def build_maturity_distribution(dataframe: pd.DataFrame, group_column: str) -> go.Figure:
    """Show the full maturity distribution instead of only group means."""
    labels = {
        "kelas_rumah_sakit": "Kelas rumah sakit",
        "kepemilikan": "Kepemilikan",
        "skor_kematangan_digital": "Skor kematangan digital",
    }
    order = sorted(dataframe[group_column].dropna().unique())
    figure = px.box(
        dataframe,
        x=group_column,
        y="skor_kematangan_digital",
        color=group_column,
        points="all",
        category_orders={group_column: order},
        color_discrete_sequence=CATEGORICAL,
        labels=labels,
        custom_data=["nama_rumah_sakit", "id_rumah_sakit"],
    )
    figure.update_traces(
        jitter=0.35,
        pointpos=0,
        marker={"size": 5, "opacity": 0.55},
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>ID: %{customdata[1]}<br>Kematangan: %{y:.1f}<extra></extra>"
        ),
    )
    figure.update_layout(showlegend=False)
    figure.update_yaxes(range=[0, 100])
    return apply_chart_theme(figure, height=440)


def build_actual_expected(dataframe: pd.DataFrame, selected_hospital_id: str | None) -> go.Figure:
    """Compare actual maturity with the out-of-fold expected value."""
    figure = px.scatter(
        dataframe,
        x="expected_digital_maturity_oof",
        y="skor_kematangan_digital",
        size="investment_intensity_score",
        color="investment_conversion_segment",
        color_discrete_map=SEGMENT_COLORS,
        custom_data=[
            "id_rumah_sakit",
            "nama_rumah_sakit",
            "digital_conversion_gap",
            "anggaran_it_per_bed",
            "staf_it_per_100_bed",
            "iot_per_100_bed",
        ],
        labels={
            "expected_digital_maturity_oof": "Kematangan ekspektasian (OOF)",
            "skor_kematangan_digital": "Kematangan aktual",
            "investment_conversion_segment": "Segmen konversi",
            "investment_intensity_score": "Intensitas investasi",
        },
    )
    minimum = min(
        dataframe["expected_digital_maturity_oof"].min(),
        dataframe["skor_kematangan_digital"].min(),
    )
    maximum = max(
        dataframe["expected_digital_maturity_oof"].max(),
        dataframe["skor_kematangan_digital"].max(),
    )
    figure.add_shape(
        type="line",
        x0=minimum,
        y0=minimum,
        x1=maximum,
        y1=maximum,
        line={"color": COLORS["secondary"], "dash": "dash"},
    )
    figure.update_traces(
        marker={"opacity": 0.75, "line": {"color": "#FBEFD3", "width": 0.8}},
        hovertemplate=(
            "<b>%{customdata[1]}</b><br>ID: %{customdata[0]}<br>"
            "Aktual: %{y:.1f}<br>Ekspektasi: %{x:.1f}<br>"
            "Gap: %{customdata[2]:+.1f}<br>Anggaran/bed: Rp%{customdata[3]:.1f} juta<br>"
            "Staf IT/100 bed: %{customdata[4]:.2f}<br>IoT/100 bed: %{customdata[5]:.1f}"
            "<extra></extra>"
        ),
    )
    if selected_hospital_id:
        selected = dataframe.loc[dataframe["id_rumah_sakit"].eq(selected_hospital_id)]
        if not selected.empty:
            row = selected.iloc[0]
            figure.add_trace(
                go.Scatter(
                    x=[row["expected_digital_maturity_oof"]],
                    y=[row["skor_kematangan_digital"]],
                    mode="markers+text",
                    text=[row["id_rumah_sakit"]],
                    textposition="top center",
                    marker={
                        "size": 24,
                        "symbol": "circle-open",
                        "color": COLORS["primary_dark"],
                        "line": {"width": 3},
                    },
                    customdata=[[selected_hospital_id]],
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
    return apply_chart_theme(figure, height=500)


def build_conversion_matrix(dataframe: pd.DataFrame) -> go.Figure:
    """Place investment intensity and conversion gap in a transparent matrix."""
    figure = px.scatter(
        dataframe,
        x="investment_intensity_score",
        y="digital_conversion_gap",
        color="investment_conversion_segment",
        color_discrete_map=SEGMENT_COLORS,
        custom_data=["id_rumah_sakit", "nama_rumah_sakit", "kelas_rumah_sakit"],
        labels={
            "investment_intensity_score": "Skor intensitas investasi IT",
            "digital_conversion_gap": "Kesenjangan konversi digital",
            "investment_conversion_segment": "Segmen konversi",
        },
    )
    figure.update_traces(
        marker={"size": 8, "opacity": 0.72},
        hovertemplate=(
            "<b>%{customdata[1]}</b><br>ID: %{customdata[0]} · Kelas %{customdata[2]}<br>"
            "Intensitas: %{x:.3f}<br>Gap konversi: %{y:+.1f}<extra></extra>"
        ),
    )
    figure.add_vline(x=0.5, line_dash="dash", line_color=COLORS["secondary"])
    figure.add_hline(y=0, line_dash="dash", line_color=COLORS["secondary"])
    return apply_chart_theme(figure, height=470)


def build_investment_components(dataframe: pd.DataFrame) -> go.Figure:
    """Compare normalized resource components across conversion segments."""
    columns = {
        "anggaran_it_per_bed_pct": "Anggaran IT/bed",
        "staf_it_per_100_bed_pct": "Staf IT/100 bed",
        "iot_per_100_bed_pct": "IoT/100 bed",
    }
    grouped = (
        dataframe.groupby("investment_conversion_segment", observed=True)[list(columns)]
        .median()
        .rename(columns=columns)
        .reset_index()
        .melt(
            id_vars="investment_conversion_segment",
            var_name="Komponen",
            value_name="Persentil median",
        )
    )
    figure = px.bar(
        grouped,
        x="Persentil median",
        y="investment_conversion_segment",
        color="Komponen",
        barmode="group",
        orientation="h",
        labels={"investment_conversion_segment": "Segmen konversi"},
        color_discrete_sequence=[COLORS["primary"], COLORS["teal"], COLORS["purple"]],
    )
    figure.update_xaxes(range=[0, 1], tickformat=".0%")
    figure.update_traces(hovertemplate="%{y}<br>%{fullData.name}: %{x:.1%}<extra></extra>")
    return apply_chart_theme(figure, height=510)
