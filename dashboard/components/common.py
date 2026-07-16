"""Shared headers, KPI cards, states, and analytical callouts."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import streamlit as st

STATUS_COLORS = {
    "BAIK": "green",
    "STABIL": "blue",
    "PERLU PERHATIAN": "orange",
    "PRIORITAS": "red",
    "DATA TERBATAS": "gray",
}


@dataclass(frozen=True)
class KpiCard:
    title: str
    value: str
    comparison: str | None = None
    status: str | None = None
    denominator: str | None = None
    help_text: str | None = None


def render_page_header(title: str, decision_question: str, data_version: str) -> None:
    """Render a consistent decision-oriented page introduction."""
    with st.container(key="page-header"):
        st.title(title)
        st.markdown(f"**{decision_question}**")
        st.caption(
            f"Data cross-sectional tingkat rumah sakit · versi `{data_version}` · "
            "hasil bersifat deskriptif, bukan kausal"
        )


def render_filter_context(summary: str, shown: int, total: int) -> None:
    """Keep active filter state and denominator visible above each analysis."""
    with st.container(border=True, key="active-filter-summary"):
        st.markdown(f":blue-badge[Filter aktif] {summary}")
        st.caption(f"Menampilkan {shown} dari {total} rumah sakit.")


def render_kpi_card(card: KpiCard, key: str) -> None:
    """Render one KPI with explicit comparison, status, and denominator."""
    with st.container(border=True, key=key, height="stretch"):
        st.metric(
            label=card.title,
            value=card.value,
            delta=card.comparison,
            delta_color="off",
            help=card.help_text,
        )
        if card.status:
            st.badge(card.status, color=STATUS_COLORS.get(card.status, "gray"))
        if card.denominator:
            st.caption(card.denominator)


def render_kpi_row(cards: Iterable[KpiCard], key: str) -> None:
    """Render a responsive row of bordered KPI cards."""
    with st.container(horizontal=True, key=key):
        for index, card in enumerate(cards):
            render_kpi_card(card, key=f"{key}-card-{index}")


def render_empty_state() -> None:
    st.warning(
        "Tidak ada rumah sakit yang sesuai dengan kombinasi filter aktif. "
        "Ubah atau reset filter untuk melanjutkan.",
        icon=":material/filter_alt_off:",
    )


def render_limited_data(message: str) -> None:
    st.warning(message, icon=":material/data_alert:")


def render_method_note(title: str, content: str) -> None:
    with st.expander(title, icon=":material/info:"):
        st.markdown(content)
