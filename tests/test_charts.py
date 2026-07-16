"""Chart builders must accept the governed artifacts without runtime errors."""

from __future__ import annotations

from collections.abc import Callable

import plotly.graph_objects as go
import pytest

from dashboard.components.charts_digital import (
    build_actual_expected,
    build_conversion_matrix,
    build_investment_components,
    build_maturity_distribution,
)
from dashboard.components.charts_executive import (
    build_priority_quadrant,
    build_province_heatmap,
)
from dashboard.components.charts_hospital import (
    build_burden_decomposition,
    build_peer_benchmark_profile,
    build_priority_decomposition,
)
from dashboard.components.charts_methodology import build_missingness_chart
from dashboard.components.charts_operational import (
    build_adjusted_coefficients,
    build_maturity_outcome_medians,
    build_maturity_referral_scatter,
    build_operational_heatmap,
)
from dashboard.components.charts_priority import (
    build_priority_matrix,
    build_priority_ranking,
    build_root_cause_pareto,
)
from dashboard.data_loader import ArtifactBundle


def _builders(bundle: ArtifactBundle) -> list[Callable[[], go.Figure]]:
    hospitals = bundle.hospitals
    selected = hospitals.iloc[0]
    peers = hospitals.loc[hospitals["kelas_rumah_sakit"].eq(selected["kelas_rumah_sakit"])]
    return [
        lambda: build_priority_quadrant(
            hospitals,
            digital_threshold=bundle.analysis_config["digital_deficit_quantile"],
            operational_threshold=bundle.analysis_config["operational_burden_quantile"],
            selected_hospital_id=None,
        ),
        lambda: build_province_heatmap(hospitals),
        lambda: build_maturity_distribution(hospitals, "kelas_rumah_sakit"),
        lambda: build_actual_expected(hospitals, None),
        lambda: build_conversion_matrix(hospitals),
        lambda: build_investment_components(hospitals),
        lambda: build_priority_matrix(hospitals, selected_hospital_id=None),
        lambda: build_priority_ranking(hospitals),
        lambda: build_root_cause_pareto(hospitals),
        lambda: build_peer_benchmark_profile(selected, peers, hospitals),
        lambda: build_burden_decomposition(selected),
        lambda: build_priority_decomposition(selected, bundle.analysis_config["priority_weights"]),
        lambda: build_adjusted_coefficients(bundle.adjusted_associations),
        lambda: build_maturity_referral_scatter(hospitals),
        lambda: build_maturity_outcome_medians(bundle.outcome_associations),
        lambda: build_operational_heatmap(hospitals),
        lambda: build_missingness_chart(bundle.data_quality),
    ]


@pytest.mark.parametrize("builder_index", range(17))
def test_chart_builders_return_nonempty_figures(bundle: ArtifactBundle, builder_index: int) -> None:
    figure = _builders(bundle)[builder_index]()
    assert isinstance(figure, go.Figure)
    assert len(figure.data) > 0
