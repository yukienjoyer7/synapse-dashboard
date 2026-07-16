"""Shared Streamlit application router used by canonical and compatibility launchers."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from dashboard.components.style import load_styles
from dashboard.data_loader import ArtifactContractError, load_artifacts
from dashboard.filters import render_global_filters
from dashboard.state import initialize_session_state

PAGE_DIR = Path(__file__).resolve().parent / "app_pages"


def run_dashboard() -> None:
    """Configure and run the complete multipage dashboard for one Streamlit rerun."""
    st.set_page_config(
        page_title="SYNAPSE HealthOps",
        page_icon=":material/health_metrics:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    load_styles()
    initialize_session_state()

    pages = [
        st.Page(
            PAGE_DIR / "executive_summary.py",
            title="Ringkasan eksekutif",
            icon=":material/dashboard:",
            url_path="ringkasan",
            default=True,
        ),
        st.Page(
            PAGE_DIR / "digital_investment.py",
            title="Kesiapan digital & investasi",
            icon=":material/hub:",
            url_path="kesiapan-digital",
        ),
        st.Page(
            PAGE_DIR / "operational_impact.py",
            title="Dampak terhadap operasional",
            icon=":material/query_stats:",
            url_path="dampak-operasional",
        ),
        st.Page(
            PAGE_DIR / "intervention_priority.py",
            title="Prioritas intervensi",
            icon=":material/priority_high:",
            url_path="prioritas",
        ),
        st.Page(
            PAGE_DIR / "hospital_explorer.py",
            title="Eksplorasi rumah sakit",
            icon=":material/domain:",
            url_path="rumah-sakit",
        ),
        st.Page(
            PAGE_DIR / "methodology.py",
            title="Metodologi & kualitas data",
            icon=":material/fact_check:",
            url_path="metodologi",
        ),
    ]

    navigation = st.navigation(pages, position="sidebar")

    try:
        artifacts = load_artifacts()
    except ArtifactContractError as error:
        st.error(str(error), icon=":material/error:")
        st.stop()

    with st.sidebar:
        st.caption("SYNAPSE HealthOps · Smart Hospital Analytics")
        render_global_filters(artifacts.hospitals)
        st.caption(f"Versi data: `{artifacts.data_version}` · n={len(artifacts.hospitals)}")

    navigation.run()
