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


def render_global_filters(hospitals: pd.DataFrame) -> FilterState:
    """Render sidebar controls shared by every page."""
    st.markdown("**Filter portofolio**")
    st.multiselect(
        "Provinsi",
        sorted(hospitals["provinsi"].dropna().unique()),
        key="filter_provinsi",
        placeholder="Semua provinsi",
    )
    st.multiselect(
        "Kelas rumah sakit",
        sorted(hospitals["kelas_rumah_sakit"].dropna().unique()),
        key="filter_kelas",
        placeholder="Semua kelas",
    )
    st.multiselect(
        "Kepemilikan",
        sorted(hospitals["kepemilikan"].dropna().unique()),
        key="filter_kepemilikan",
        placeholder="Semua kepemilikan",
    )
    st.multiselect(
        "Status implementasi RME",
        sorted(hospitals["status_implementasi_rme"].dropna().unique()),
        key="filter_rme",
        placeholder="Semua status",
    )
    st.multiselect(
        "Status koneksi SatuSehat",
        sorted(hospitals["status_terhubung_satusehat"].dropna().unique()),
        key="filter_satusehat",
        placeholder="Semua status",
    )
    st.toggle(
        "Hanya rumah sakit prioritas",
        key="priority_only",
        help="Menampilkan Tier 1 Inefisiensi Ganda dan Tier 2 Early Warning.",
    )

    st.markdown("**Pilih rumah sakit**")
    ordered = hospitals.sort_values(["nama_rumah_sakit", "id_rumah_sakit"])
    name_by_id = ordered.set_index("id_rumah_sakit")["nama_rumah_sakit"].to_dict()
    st.selectbox(
        "Cari nama atau ID rumah sakit",
        [None, *ordered["id_rumah_sakit"].tolist()],
        key="hospital_search",
        format_func=lambda hospital_id: (
            "Belum ada pilihan"
            if hospital_id is None
            else f"{hospital_id} · {name_by_id[hospital_id]}"
        ),
        on_change=_sync_hospital_search,
        args=(hospitals,),
    )

    st.button(
        "Reset semua filter",
        icon=":material/restart_alt:",
        type="tertiary",
        on_click=reset_dashboard_state,
        width="stretch",
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
