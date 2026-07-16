"""Per-session interface state for the multipage dashboard."""

from __future__ import annotations

from typing import TypedDict

import streamlit as st


class FilterState(TypedDict):
    """Serializable global portfolio filter values."""

    provinsi: list[str]
    kelas_rumah_sakit: list[str]
    kepemilikan: list[str]
    status_implementasi_rme: list[str]
    status_terhubung_satusehat: list[str]
    priority_only: bool


SESSION_DEFAULTS: dict[str, object] = {
    "filter_provinsi": [],
    "filter_kelas": [],
    "filter_kepemilikan": [],
    "filter_rme": [],
    "filter_satusehat": [],
    "priority_only": False,
    "hospital_search": None,
    "selected_hospital_id": None,
    "selected_hospital_name": None,
}


def initialize_session_state() -> None:
    """Initialize all state shared across pages in one place."""
    for key, default in SESSION_DEFAULTS.items():
        st.session_state.setdefault(key, default.copy() if isinstance(default, list) else default)


def get_filter_state() -> FilterState:
    """Return global filter values without widget-specific names."""
    return FilterState(
        provinsi=list(st.session_state.get("filter_provinsi", [])),
        kelas_rumah_sakit=list(st.session_state.get("filter_kelas", [])),
        kepemilikan=list(st.session_state.get("filter_kepemilikan", [])),
        status_implementasi_rme=list(st.session_state.get("filter_rme", [])),
        status_terhubung_satusehat=list(st.session_state.get("filter_satusehat", [])),
        priority_only=bool(st.session_state.get("priority_only", False)),
    )


def set_selected_hospital(hospital_id: str | None, hospital_name: str | None = None) -> None:
    """Persist a hospital selection made from a chart, table, or search."""
    st.session_state.selected_hospital_id = hospital_id
    st.session_state.selected_hospital_name = hospital_name


def reset_dashboard_state() -> None:
    """Reset all global filters, selection, and page-local table state."""
    for key, default in SESSION_DEFAULTS.items():
        st.session_state[key] = default.copy() if isinstance(default, list) else default
    for key in list(st.session_state):
        if key.startswith(("table_page_", "table_search_", "table_selection_")):
            del st.session_state[key]
