"""Deterministic global filtering behavior."""

from __future__ import annotations

from dashboard.data_loader import ArtifactBundle
from dashboard.filters import active_filter_count, active_filter_summary, filter_hospitals
from dashboard.state import FilterState


def _filters(**overrides: object) -> FilterState:
    values: FilterState = {
        "provinsi": [],
        "kelas_rumah_sakit": [],
        "kepemilikan": [],
        "status_implementasi_rme": [],
        "status_terhubung_satusehat": [],
        "priority_only": False,
    }
    values.update(overrides)  # type: ignore[typeddict-item]
    return values


def test_empty_filters_return_full_portfolio(bundle: ArtifactBundle) -> None:
    filtered = filter_hospitals(bundle.hospitals, _filters())
    assert len(filtered) == 276
    assert active_filter_summary(_filters()) == "Seluruh portofolio rumah sakit"


def test_combined_filters_match_direct_boolean_selection(bundle: ArtifactBundle) -> None:
    filters = _filters(
        provinsi=["DKI Jakarta"],
        kelas_rumah_sakit=["C"],
        status_terhubung_satusehat=["Ya"],
    )
    actual = filter_hospitals(bundle.hospitals, filters)
    expected = bundle.hospitals.loc[
        bundle.hospitals["provinsi"].eq("DKI Jakarta")
        & bundle.hospitals["kelas_rumah_sakit"].eq("C")
        & bundle.hospitals["status_terhubung_satusehat"].eq("Ya")
    ]
    assert actual["id_rumah_sakit"].tolist() == expected["id_rumah_sakit"].tolist()


def test_unknown_filter_value_returns_empty_result(bundle: ArtifactBundle) -> None:
    assert filter_hospitals(bundle.hospitals, _filters(provinsi=["Provinsi tidak ada"])).empty


def test_priority_only_uses_tier_one_and_two(bundle: ArtifactBundle) -> None:
    filtered = filter_hospitals(bundle.hospitals, _filters(priority_only=True))
    assert len(filtered) == 28
    assert set(filtered["intervention_tier"]) == {
        "Tier 1 — Inefisiensi Ganda",
        "Tier 2 — Early Warning",
    }


def test_filter_summary_truncates_long_values() -> None:
    filters = _filters(provinsi=["A", "B", "C", "D"], priority_only=True)
    summary = active_filter_summary(filters)
    assert "Provinsi: A, B, C +1" in summary
    assert "Prioritas: Tier 1–2" in summary
    assert active_filter_count(filters) == 2


def test_filter_count_uses_active_groups_not_selected_value_count() -> None:
    filters = _filters(
        provinsi=["DKI Jakarta", "Jawa Barat"],
        kelas_rumah_sakit=["A", "B"],
        status_implementasi_rme=["Ya"],
    )
    assert active_filter_count(filters) == 3
