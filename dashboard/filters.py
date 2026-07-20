"""Global filter widgets and deterministic portfolio filtering."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.state import FilterState, get_filter_state, reset_dashboard_state

FILTER_LABELS = {
    "provinsi": "Provinsi",
    "kelas_rumah_sakit": "Kelas",
    "kepemilikan": "Kepemilikan",
    "status_implementasi_rme": "RME",
    "status_terhubung_satusehat": "SatuSehat",
}


def _sync_hospital_search(hospitals: pd.DataFrame) -> None:
    hospital_id = st.session_state.get("hospital_search")
    if hospital_id is None:
        st.session_state.selected_hospital_id = None
        st.session_state.selected_hospital_name = None
        return
    match = hospitals.loc[hospitals["id_rumah_sakit"].eq(hospital_id), "nama_rumah_sakit"]
    st.session_state.selected_hospital_id = hospital_id
    st.session_state.selected_hospital_name = match.iloc[0] if not match.empty else None


def render_global_filter_toolbar(hospitals: pd.DataFrame) -> FilterState:
    """Render shared portfolio controls in a compact main-area command bar."""
    ordered = hospitals.sort_values(["nama_rumah_sakit", "id_rumah_sakit"])
    name_by_id = ordered.set_index("id_rumah_sakit")["nama_rumah_sakit"].to_dict()

    filter_count = active_filter_count(get_filter_state())
    filter_label = "Filter portofolio" if not filter_count else f"Filter · {filter_count} aktif"

    with st.container(key="global-filter-toolbar", border=True):
        with st.container(
            key="global-filter-actions",
            horizontal=True,
            vertical_alignment="bottom",
            gap="xsmall",
        ):
            st.selectbox(
                "Cari rumah sakit",
                ordered["id_rumah_sakit"].tolist(),
                index=None,
                key="hospital_search",
                placeholder="Cari nama atau ID rumah sakit",
                format_func=lambda hospital_id: f"{hospital_id} · {name_by_id[hospital_id]}",
                on_change=_sync_hospital_search,
                args=(hospitals,),
                width=520,
            )

            with st.popover(
                filter_label,
                icon=":material/filter_list:",
                type="primary" if filter_count else "secondary",
                key="global-filter-popover",
            ):
                st.caption("PERSEMPIT PORTOFOLIO")
                st.multiselect(
                    "Provinsi",
                    sorted(hospitals["provinsi"].dropna().unique()),
                    key="filter_provinsi",
                    placeholder="Semua provinsi",
                )
                st.pills(
                    "Kelas rumah sakit",
                    sorted(hospitals["kelas_rumah_sakit"].dropna().unique()),
                    selection_mode="multi",
                    key="filter_kelas",
                    width="stretch",
                )
                st.multiselect(
                    "Kepemilikan",
                    sorted(hospitals["kepemilikan"].dropna().unique()),
                    key="filter_kepemilikan",
                    placeholder="Semua kepemilikan",
                )
                st.pills(
                    "Status implementasi RME",
                    sorted(hospitals["status_implementasi_rme"].dropna().unique()),
                    selection_mode="multi",
                    key="filter_rme",
                    width="stretch",
                )
                st.pills(
                    "Status koneksi SatuSehat",
                    sorted(hospitals["status_terhubung_satusehat"].dropna().unique()),
                    selection_mode="multi",
                    key="filter_satusehat",
                    width="stretch",
                )

            st.toggle(
                "Hanya prioritas",
                key="priority_only",
                help="Menampilkan Tier 1 Inefisiensi Ganda dan Tier 2 Early Warning.",
            )
            st.button(
                "Reset",
                key="reset-global-filters",
                icon=":material/restart_alt:",
                type="tertiary",
                on_click=reset_dashboard_state,
            )

    return get_filter_state()


def filter_hospitals(hospitals: pd.DataFrame, filters: FilterState) -> pd.DataFrame:
    """Apply global filters without changing analytical benchmark definitions."""
    mask = pd.Series(True, index=hospitals.index)
    for column in FILTER_LABELS:
        values = filters[column]
        if values:
            mask &= hospitals[column].isin(values)
    if filters["priority_only"]:
        mask &= hospitals["intervention_tier"].ne("Tier 3 — Monitoring")
    return hospitals.loc[mask].copy()


def active_filter_summary(filters: FilterState) -> str:
    """Build a compact, human-readable description of active filters."""
    parts: list[str] = []
    for column, label in FILTER_LABELS.items():
        values = filters[column]
        if values:
            value_text = ", ".join(values[:3])
            if len(values) > 3:
                value_text += f" +{len(values) - 3}"
            parts.append(f"{label}: {value_text}")
    if filters["priority_only"]:
        parts.append("Prioritas: Tier 1–2")
    return " | ".join(parts) if parts else "Seluruh portofolio rumah sakit"


def active_filter_count(filters: FilterState) -> int:
    """Count active filter groups for the toolbar status affordance."""
    dimension_count = sum(bool(filters[column]) for column in FILTER_LABELS)
    return dimension_count + int(filters["priority_only"])
