"""Headless Streamlit smoke coverage for the shell and every page."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_FILES = [
    Path("streamlit_app.py"),
    Path("dashboard/app.py"),
    *sorted(
        path for path in Path("dashboard/app_pages").glob("*.py") if path.name != "__init__.py"
    ),
]


@pytest.mark.parametrize("app_file", APP_FILES, ids=lambda path: path.stem)
def test_streamlit_entrypoints_have_no_exceptions(app_file: Path) -> None:
    app = AppTest.from_file(str(app_file)).run(timeout=30)
    assert not app.exception


def test_legacy_launcher_resolves_package_outside_repository(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, str(project_root / "dashboard/app.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0
    assert "ModuleNotFoundError" not in result.stderr
