"""Shared page context assembled from cached data and session filters."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from dashboard.data_loader import ArtifactBundle, load_artifacts
from dashboard.filters import active_filter_summary, filter_hospitals
from dashboard.state import FilterState, get_filter_state


@dataclass(frozen=True)
class PageContext:
    bundle: ArtifactBundle
    filters: FilterState
    hospitals: pd.DataFrame
    filter_summary: str


def get_page_context() -> PageContext:
    """Return the immutable artifacts and current filtered portfolio."""
    bundle = load_artifacts()
    filters = get_filter_state()
    return PageContext(
        bundle=bundle,
        filters=filters,
        hospitals=filter_hospitals(bundle.hospitals, filters),
        filter_summary=active_filter_summary(filters),
    )
