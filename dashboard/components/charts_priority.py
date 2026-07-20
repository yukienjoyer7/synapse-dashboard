"""Charts for intervention prioritization and bottleneck evidence."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dashboard.components.chart_theme import COLORS, TIER_COLORS, apply_chart_theme, shorten_label


def build_priority_matrix(
    dataframe: pd.DataFrame,
    *,
    selected_hospital_id: str | None,
) -> go.Figure:
    """Show all three precomputed priority score dimensions."""
    plot_df = dataframe.assign(
        bubble_size=dataframe["investment_underperformance_score"].fillna(0) + 0.04
    )
    figure = px.scatter(
        plot_df,
        x="digital_deficit_score",
        y="operational_burden_score",
        size="bubble_size",
        color="intervention_tier",
        color_discrete_map=TIER_COLORS,
        category_orders={"intervention_tier": list(TIER_COLORS)},
        custom_data=[
            "id_rumah_sakit",
            "nama_rumah_sakit",
            "kelas_rumah_sakit",
            "investment_underperformance_score",
            "intervention_priority_score",
            "root_cause_primary",
        ],
        labels={
            "digital_deficit_score": "Skor defisit digital",
            "operational_burden_score": "Skor beban operasional",
            "bubble_size": "Underperformance investasi",
            "intervention_tier": "Tier intervensi",
        },
    )
    figure.update_traces(
        marker={"opacity": 0.76, "line": {"color": "#FBEFD3", "width": 0.8}},
        hovertemplate=(
            "<b>%{customdata[1]}</b><br>ID: %{customdata[0]} · Kelas %{customdata[2]}<br>"
            "Defisit digital: %{x:.3f}<br>Beban operasional: %{y:.3f}<br>"
            "Underperformance investasi: %{customdata[3]:.3f}<br>"
            "Skor prioritas: %{customdata[4]:.3f}<br>"
            "Hambatan: %{customdata[5]}<extra></extra>"
        ),
    )
    figure.add_vline(x=0.75, line_dash="dash", line_color=COLORS["secondary"])
    figure.add_hline(y=0.75, line_dash="dash", line_color=COLORS["secondary"])
    if selected_hospital_id:
        selected = plot_df.loc[plot_df["id_rumah_sakit"].eq(selected_hospital_id)]
        if not selected.empty:
            row = selected.iloc[0]
            figure.add_trace(
                go.Scatter(
                    x=[row["digital_deficit_score"]],
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
                    showlegend=False,
                )
            )
    figure.update_xaxes(range=[0, 1.02], tickformat=".0%")
    figure.update_yaxes(range=[0, 1.02], tickformat=".0%")
    return apply_chart_theme(figure, height=500)


def build_root_cause_pareto(dataframe: pd.DataFrame) -> go.Figure:
    """Count primary bottlenecks and show their cumulative share."""
    counts = dataframe["root_cause_primary"].value_counts().rename_axis("hambatan").reset_index()
    counts.columns = ["hambatan", "jumlah"]
    counts["hambatan"] = counts["hambatan"].map(shorten_label)
    counts["kumulatif"] = counts["jumlah"].cumsum() / counts["jumlah"].sum()
    figure = make_subplots(specs=[[{"secondary_y": True}]])
    figure.add_trace(
        go.Bar(
            x=counts["hambatan"],
            y=counts["jumlah"],
            marker_color=COLORS["primary"],
            name="Rumah sakit",
            hovertemplate="%{x}<br>%{y} rumah sakit<extra></extra>",
        ),
        secondary_y=False,
    )
    figure.add_trace(
        go.Scatter(
            x=counts["hambatan"],
            y=counts["kumulatif"],
            mode="lines+markers",
            line={"color": COLORS["watch"], "width": 2},
            marker={"size": 7},
            name="Share kumulatif",
            hovertemplate="%{x}<br>Kumulatif %{y:.1%}<extra></extra>",
        ),
        secondary_y=True,
    )
    figure.update_yaxes(title_text="Jumlah rumah sakit", secondary_y=False)
    figure.update_yaxes(
        title_text="Share kumulatif", range=[0, 1.05], tickformat=".0%", secondary_y=True
    )
    figure.update_xaxes(tickangle=-35)
    return apply_chart_theme(figure, height=520)


def build_priority_ranking(dataframe: pd.DataFrame, limit: int = 15) -> go.Figure:
    """Render a compact ranked dot plot for the top visible hospitals."""
    ranked = dataframe.nsmallest(limit, "priority_rank").sort_values("intervention_priority_score")
    labels = ranked["id_rumah_sakit"] + " · " + ranked["nama_rumah_sakit"]
    figure = go.Figure()
    for _, row in ranked.iterrows():
        label = f"{row['id_rumah_sakit']} · {row['nama_rumah_sakit']}"
        figure.add_trace(
            go.Scatter(
                x=[0, row["intervention_priority_score"]],
                y=[label, label],
                mode="lines",
                line={"color": "#E8DFC0", "width": 2},
                hoverinfo="skip",
                showlegend=False,
            )
        )
    figure.add_trace(
        go.Scatter(
            x=ranked["intervention_priority_score"],
            y=labels,
            mode="markers",
            marker={
                "size": 11,
                "color": ranked["intervention_tier"].map(TIER_COLORS),
                "line": {"color": "#FBEFD3", "width": 1},
            },
            customdata=ranked[
                [
                    "id_rumah_sakit",
                    "root_cause_primary",
                    "priority_rank",
                    "intervention_tier",
                ]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{y}</b><br>Peringkat: %{customdata[2]}<br>"
                "Skor: %{x:.3f}<br>Tier: %{customdata[3]}<br>"
                "Hambatan: %{customdata[1]}<extra></extra>"
            ),
            showlegend=False,
        )
    )
    figure.update_xaxes(range=[0, 1], title="Skor prioritas intervensi")
    figure.update_yaxes(title=None)
    return apply_chart_theme(figure, height=max(460, 34 * len(ranked)))
