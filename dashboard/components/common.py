"""Shared headers, KPI cards, states, and analytical callouts."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import streamlit as st

from dashboard.components.healthops_ui import mount_healthops_ui


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
    mount_healthops_ui(
        "page_header",
        {
            "title": title,
            "question": decision_question,
            "data_version": data_version,
            "eyebrow": "SYNAPSE · Portfolio intelligence",
            "meta": (
                "Data cross-sectional tingkat rumah sakit · hasil bersifat deskriptif, bukan kausal"
            ),
        },
        key="healthops-page-header",
    )


def render_filter_context(summary: str, shown: int, total: int) -> None:
    """Keep active filter state and denominator visible above each analysis."""
    mount_healthops_ui(
        "filter_context",
        {"summary": summary, "shown": shown, "total": total},
        key="healthops-filter-context",
    )


def render_kpi_row(cards: Iterable[KpiCard], key: str) -> None:
    """Render a responsive, semantic CCv2 KPI grid."""
    serialized = [
        {
            "title": card.title,
            "value": card.value,
            "comparison": card.comparison,
            "status": card.status,
            "denominator": card.denominator,
            "help_text": card.help_text,
        }
        for card in cards
    ]
    mount_healthops_ui(
        "kpi_grid",
        {"cards": serialized, "aria_label": "Indikator utama halaman"},
        key=f"healthops-{key}",
    )


def render_section_header(
    title: str,
    *,
    subtitle: str | None = None,
    kicker: str | None = None,
    key: str,
) -> None:
    """Render a consistent section boundary without another boxed container."""
    mount_healthops_ui(
        "section_header",
        {"title": title, "subtitle": subtitle, "kicker": kicker},
        key=f"healthops-section-{key}",
    )


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
