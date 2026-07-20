"""Decision charts for the executive portfolio page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.components.chart_theme import COLORS, TIER_COLORS, apply_chart_theme


def build_priority_quadrant(
    dataframe: pd.DataFrame,
    *,
    digital_threshold: float,
    operational_threshold: float,
    selected_hospital_id: str | None,
) -> go.Figure:
    """Show class-relative maturity against operational burden."""
    plot_df = dataframe.copy()
    figure = px.scatter(
        plot_df,
        x="maturity_peer_pct",
        y="operational_burden_score",
        size="jumlah_tempat_tidur",
        color="intervention_tier",
        color_discrete_map=TIER_COLORS,
        category_orders={"intervention_tier": list(TIER_COLORS)},
        custom_data=[
            "id_rumah_sakit",
            "nama_rumah_sakit",
            "provinsi",
            "kelas_rumah_sakit",
            "skor_kematangan_digital",
            "rata_rata_waktu_respons_rujukan_menit",
            "intervention_priority_score",
        ],
        labels={
            "maturity_peer_pct": "Persentil kematangan dalam kelas",
            "operational_burden_score": "Skor beban operasional",
            "intervention_tier": "Tier intervensi",
            "jumlah_tempat_tidur": "Jumlah tempat tidur",
        },
    )
    figure.update_traces(
        marker={"opacity": 0.78, "line": {"color": "#FBEFD3", "width": 0.8}},
        hovertemplate=(
            "<b>%{customdata[1]}</b><br>"
            "ID: %{customdata[0]}<br>Provinsi: %{customdata[2]}<br>"
            "Kelas: %{customdata[3]}<br>Kematangan: %{customdata[4]:.1f}<br>"
            "Respons rujukan: %{customdata[5]:.1f} menit<br>"
            "Skor prioritas: %{customdata[6]:.3f}<extra></extra>"
        ),
    )
    figure.add_vline(
        x=digital_threshold,
        line_dash="dash",
        line_color=COLORS["secondary"],
        annotation_text=f"Kuartil bawah kelas ({digital_threshold:.2f})",
        annotation_position="top right",
    )
    figure.add_hline(
        y=operational_threshold,
        line_dash="dash",
        line_color=COLORS["secondary"],
        annotation_text=f"Beban tinggi ({operational_threshold:.2f})",
        annotation_position="bottom right",
    )
    figure.add_annotation(
        x=0.05,
        y=0.96,
        text="Prioritas intervensi",
        showarrow=False,
        font={"color": COLORS["danger"], "size": 12},
    )
    figure.add_annotation(
        x=0.94,
        y=0.28,
        text="Siap dan lebih stabil",
        showarrow=False,
        font={"color": COLORS["teal"], "size": 12},
    )
    if selected_hospital_id:
        selected = plot_df.loc[plot_df["id_rumah_sakit"].eq(selected_hospital_id)]
        if not selected.empty:
            row = selected.iloc[0]
            figure.add_trace(
                go.Scatter(
                    x=[row["maturity_peer_pct"]],
                    y=[row["operational_burden_score"]],
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
                    name="Rumah sakit terpilih",
                    showlegend=False,
                )
            )
    figure.update_xaxes(range=[0, 1.02], tickformat=".0%")
    figure.update_yaxes(range=[0, 1.02], tickformat=".0%")
    return apply_chart_theme(figure, height=500)


def build_province_heatmap(dataframe: pd.DataFrame) -> go.Figure:
    """Summarize the strongest portfolio signals by province."""
    grouped = (
        dataframe.assign(satusehat_gap=1 - dataframe["satusehat_bin"])
        .groupby("provinsi", observed=True)
        .agg(
            defisit_digital=("digital_deficit_score", "median"),
            gap_satusehat=("satusehat_gap", "mean"),
            beban_rujukan=("referral_burden", "median"),
            deviasi_bor=("bor_burden", "median"),
            inefisiensi_ganda=("double_inefficiency", "mean"),
            jumlah=("id_rumah_sakit", "size"),
        )
    )
    metric_columns = [
        "defisit_digital",
        "gap_satusehat",
        "beban_rujukan",
        "deviasi_bor",
        "inefisiensi_ganda",
    ]
    grouped["signal"] = grouped[metric_columns].mean(axis=1)
    grouped = grouped.sort_values("signal", ascending=False).head(15).sort_values("signal")
    labels = [
        "Defisit digital",
        "Gap SatuSehat",
        "Beban rujukan",
        "Deviasi BOR",
        "Inefisiensi ganda",
    ]
    figure = go.Figure(
        go.Heatmap(
            z=grouped[metric_columns].to_numpy(),
            x=labels,
            y=grouped.index,
            zmin=0,
            zmax=1,
            colorscale=[
                [0.0, "#F1E9D0"],
                [0.5, "#F6D68A"],
                [1.0, COLORS["danger"]],
            ],
            colorbar={"title": "Sinyal<br>relatif", "tickformat": ".0%"},
            hovertemplate="%{y}<br>%{x}: %{z:.1%}<extra></extra>",
        )
    )
    figure.update_xaxes(side="top")
    return apply_chart_theme(figure, height=510)
