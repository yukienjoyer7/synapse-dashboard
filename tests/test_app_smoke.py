"""Headless Streamlit smoke coverage for the shell and every page."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

APP_TEST_SCRIPT = """
from pathlib import Path
import sys

from streamlit.testing.v1 import AppTest

app = AppTest.from_file(str(Path(sys.argv[1]))).run(timeout=30)
if app.exception:
    for exception in app.exception:
        print(exception.value, file=sys.stderr)
    raise SystemExit(1)
"""

APP_FILES = [
    Path("streamlit_app.py"),
    Path("dashboard/app.py"),
    *sorted(
        path for path in Path("dashboard/app_pages").glob("*.py") if path.name != "__init__.py"
    ),
]


@pytest.mark.parametrize("app_file", APP_FILES, ids=lambda path: path.stem)
def test_streamlit_entrypoints_have_no_exceptions(app_file: Path) -> None:
    # Components v2 are registered against a Streamlit runtime. Isolating each
    # smoke render mirrors production startup and prevents one AppTest runtime
    # from inheriting another runtime's cached Python modules.
    result = subprocess.run(
        [sys.executable, "-c", APP_TEST_SCRIPT, str(app_file)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_legacy_launcher_resolves_package_outside_repository(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "dashboard/app.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0
    assert "ModuleNotFoundError" not in result.stderr
