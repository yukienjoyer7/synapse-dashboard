"""Regression checks for the notebook-to-dashboard data contract."""

from __future__ import annotations

import re

import pandas as pd
import pytest

from dashboard.data_loader import ArtifactBundle, ArtifactContractError, validate_columns


def test_primary_portfolio_identity_and_governed_counts(bundle: ArtifactBundle) -> None:
    hospitals = bundle.hospitals
    assert len(hospitals) == 276
    assert hospitals["id_rumah_sakit"].notna().all()
    assert hospitals["id_rumah_sakit"].is_unique
    assert hospitals["status_implementasi_rme"].eq("Ya").sum() == 254
    assert hospitals["status_terhubung_satusehat"].eq("Ya").sum() == 237
    assert hospitals["conversion_underperformance_flag"].sum() == 17
    assert hospitals["double_inefficiency"].sum() == 7
    assert hospitals["intervention_tier"].eq("Tier 1 — Inefisiensi Ganda").sum() == 7
    assert hospitals["intervention_tier"].eq("Tier 2 — Early Warning").sum() == 21


def test_supporting_artifacts_have_exact_hospital_coverage(bundle: ArtifactBundle) -> None:
    expected_ids = set(bundle.hospitals["id_rumah_sakit"])
    for dataframe in (bundle.priority, bundle.peers, bundle.root_causes):
        assert len(dataframe) == len(expected_ids)
        assert dataframe["id_rumah_sakit"].is_unique
        assert set(dataframe["id_rumah_sakit"]) == expected_ids


def test_configuration_and_model_governance_are_preserved(bundle: ArtifactBundle) -> None:
    assert sum(bundle.analysis_config["priority_weights"].values()) == pytest.approx(1.0)
    assert bundle.analysis_config["bor_reference_range"] == [60, 85]
    governance = bundle.model_metrics["model_governance"]
    assert governance["scenario_model_eligible"] is False
    assert governance["explainability_model_eligible"] is False
    assert governance["explainability_method"].startswith("Tidak dilaporkan")


def test_data_version_and_source_missingness_are_stable(bundle: ArtifactBundle) -> None:
    assert re.fullmatch(r"data-[0-9a-f]{12}", bundle.data_version)
    assert bundle.data_quality["missing_count"].sum() == 24
    missing_variables = set(
        bundle.data_quality.loc[bundle.data_quality["missing_count"].gt(0), "variabel"]
    )
    assert missing_variables == {
        "jumlah_staf_it",
        "kunjungan_telemedicine_per_bulan",
        "anggaran_it_tahunan_juta_rupiah",
    }


def test_column_validation_reports_missing_contract_fields() -> None:
    with pytest.raises(ArtifactContractError, match="kolom wajib"):
        validate_columns(pd.DataFrame({"present": [1]}), {"present", "missing"}, "x.csv")
