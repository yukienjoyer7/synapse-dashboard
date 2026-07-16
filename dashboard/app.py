"""Backward-compatible launcher for deployments configured with dashboard/app.py."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

application = importlib.import_module("dashboard.application")
application.run_dashboard()
