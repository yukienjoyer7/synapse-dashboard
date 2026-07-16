"""Hospital-level peer, burden, and priority charts."""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd
import plotly.graph_objects as go

from dashboard.components.chart_theme import COLORS, apply_chart_theme

BENCHMARK_METRICS: list[tuple[str, str, str]] = [
    ("skor_kematangan_digital", "Kematangan Digital", "skor"),
    ("anggaran_it_per_bed", "Anggaran IT/bed", "Rp juta"),
    ("staf_it_per_100_bed", "Staf IT/100 bed", "staf"),
    ("iot_per_100_bed", "IoT/100 bed", "perangkat"),
    ("tingkat_keterisian_tempat_tidur_persen", "BOR", "%"),
    ("rata_rata_lama_rawat_hari", "Rata-rata LOS", "hari"),
    ("rata_rata_waktu_respons_rujukan_menit", "Respons rujukan", "menit"),
    ("pasien_per_tenaga_kerja", "Pasien/tenaga kerja", "rasio"),
    ("telemedicine_rate_per_1000", "Telemedicine/1.000", "kunjungan"),
]


def build_peer_benchmark_profile(
    selected: pd.Series,
    peer_group: pd.DataFrame,
    portfolio: pd.DataFrame,
) -> go.Figure:
    """Normalize unlike metrics to class percentiles while retaining exact hover values."""
    rows = []
    for column, label, unit in BENCHMARK_METRICS:
        valid_peer = peer_group[column].dropna()
        actual = selected[column]
        if valid_peer.empty or pd.isna(actual):
            continue
        rows.append(
            {
                "label": label,
                "unit": unit,
                "percentile": float(valid_peer.le(actual).mean()),
                "q1_percentile": 0.25,
                "q3_percentile": 0.75,
                "actual": float(actual),
                "peer_q1": float(valid_peer.quantile(0.25)),
                "peer_median": float(valid_peer.median()),
                "peer_q3": float(valid_peer.quantile(0.75)),
                "national_median": float(portfolio[column].median()),
            }
        )
    benchmark = pd.DataFrame(rows)
    figure = go.Figure()
    for _, row in benchmark.iterrows():
        figure.add_trace(
            go.Scatter(
                x=[row["q1_percentile"], row["q3_percentile"]],
                y=[row["label"], row["label"]],
                mode="lines",
                line={"color": "#CDE6F7", "width": 12},
                hoverinfo="skip",
                showlegend=False,
            )
        )
    figure.add_trace(
        go.Scatter(
            x=benchmark["percentile"],
            y=benchmark["label"],
            mode="markers",
            marker={
                "size": 13,
                "color": COLORS["primary"],
                "line": {"color": "white", "width": 1.5},
            },
            customdata=benchmark[
                ["actual", "peer_q1", "peer_median", "peer_q3", "national_median", "unit"]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{y}</b><br>Nilai RS: %{customdata[0]:.2f} %{customdata[5]}<br>"
                "Peer Q1–Q3: %{customdata[1]:.2f}–%{customdata[3]:.2f}<br>"
                "Peer median: %{customdata[2]:.2f}<br>"
                "Median nasional: %{customdata[4]:.2f}<br>"
                "Persentil kelas: %{x:.1%}<extra></extra>"
            ),
            showlegend=False,
        )
    )
    figure.add_vline(
        x=0.5,
        line_dash="dash",
        line_color=COLORS["secondary"],
        annotation_text="Median kelas",
        annotation_position="top right",
    )
    figure.update_xaxes(range=[0, 1], tickformat=".0%", title="Persentil dalam kelas")
    figure.update_yaxes(title=None, autorange="reversed")
    return apply_chart_theme(figure, height=560)


def build_burden_decomposition(selected: pd.Series) -> go.Figure:
    """Expose every precomputed component of operational burden."""
    components = pd.DataFrame(
        {
            "Komponen": ["Respons rujukan", "Deviasi BOR", "LOS", "Beban kerja"],
            "Skor": [
                selected["referral_burden"],
                selected["bor_burden"],
                selected["los_burden"],
                selected["workload_burden"],
            ],
        }
    ).sort_values("Skor")
    colors = []
    for value in components["Skor"]:
        if value >= 0.75:
            colors.append(COLORS["danger"])
        elif value >= 0.5:
            colors.append(COLORS["watch"])
        else:
            colors.append(COLORS["primary"])
    figure = go.Figure(
        go.Bar(
            x=components["Skor"],
            y=components["Komponen"],
            orientation="h",
            marker_color=colors,
            text=components["Skor"].map(lambda value: f"{value:.0%}"),
            textposition="outside",
            hovertemplate="%{y}: %{x:.1%}<extra></extra>",
        )
    )
    figure.update_xaxes(range=[0, 1.08], tickformat=".0%", title="Persentil beban dalam kelas")
    figure.update_yaxes(title=None)
    return apply_chart_theme(figure, height=360)


def build_priority_decomposition(selected: pd.Series, weights: Mapping[str, float]) -> go.Figure:
    """Show weighted contributions to the final priority score."""
    raw = {
        "Defisit Digital": float(selected["digital_deficit_score"]),
        "Beban Operasional": float(selected["operational_burden_score"]),
        "Underperformance Investasi": float(selected["investment_underperformance_score"]),
    }
    weight_values = {
        "Defisit Digital": weights["digital_deficit"],
        "Beban Operasional": weights["operational_burden"],
        "Underperformance Investasi": weights["investment_underperformance"],
    }
    labels = list(raw)
    contributions = [raw[label] * weight_values[label] for label in labels]
    figure = go.Figure(
        go.Bar(
            x=contributions,
            y=labels,
            orientation="h",
            marker_color=[COLORS["primary"], COLORS["watch"], COLORS["purple"]],
            customdata=[[raw[label], weight_values[label]] for label in labels],
            text=[f"{value:.3f}" for value in contributions],
            textposition="outside",
            hovertemplate=(
                "%{y}<br>Skor komponen: %{customdata[0]:.3f}<br>"
                "Bobot: %{customdata[1]:.0%}<br>Kontribusi: %{x:.3f}<extra></extra>"
            ),
        )
    )
    figure.update_xaxes(range=[0, max(0.5, max(contributions) * 1.25)], title="Kontribusi berbobot")
    figure.update_yaxes(title=None)
    return apply_chart_theme(figure, height=330)
