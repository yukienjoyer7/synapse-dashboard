"""Load the small, design-system-approved CSS enhancement layer."""

from pathlib import Path

import streamlit as st

STYLE_PATH = Path(__file__).resolve().parents[1] / "styles" / "main.css"


@st.cache_data(show_spinner=False)
def _read_styles() -> str:
    return STYLE_PATH.read_text(encoding="utf-8")


def load_styles() -> None:
    """Inject scoped component styling while leaving theme colors to config.toml."""
    st.html(f"<style>{_read_styles()}</style>")
