"""Shared immutable artifact fixtures."""

from __future__ import annotations

import pytest

from dashboard.data_loader import ArtifactBundle, load_artifacts


@pytest.fixture(scope="session")
def bundle() -> ArtifactBundle:
    return load_artifacts()
