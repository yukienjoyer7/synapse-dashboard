"""Headless Streamlit smoke coverage for the shell and every page."""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_FILES = [
    Path("dashboard/app.py"),
    *sorted(
        path for path in Path("dashboard/app_pages").glob("*.py") if path.name != "__init__.py"
    ),
]


@pytest.mark.parametrize("app_file", APP_FILES, ids=lambda path: path.stem)
def test_streamlit_entrypoints_have_no_exceptions(app_file: Path) -> None:
    app = AppTest.from_file(str(app_file)).run(timeout=30)
    assert not app.exception
