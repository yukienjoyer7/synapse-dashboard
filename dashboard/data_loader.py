"""Cached loading and validation for notebook-produced dashboard artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = PROJECT_ROOT / "synapse_artifacts"
EXPECTED_HOSPITAL_COUNT = 276


class ArtifactContractError(ValueError):
    """Raised when an analytics artifact cannot satisfy the dashboard contract."""


@dataclass(frozen=True)
class ArtifactBundle:
    """All immutable, precomputed inputs used by the dashboard."""

    hospitals: pd.DataFrame
    priority: pd.DataFrame
    peers: pd.DataFrame
    root_causes: pd.DataFrame
    recommendations: pd.DataFrame
    executive_findings: pd.DataFrame
    outcome_associations: pd.DataFrame
    adjusted_associations: pd.DataFrame
    adjusted_model_summary: pd.DataFrame
    data_quality: pd.DataFrame
    analysis_config: dict[str, Any]
    model_metrics: dict[str, Any]
    data_version: str


REQUIRED_COLUMNS: dict[str, set[str]] = {
    "hospital_features_scored.csv": {
        "id_rumah_sakit",
        "nama_rumah_sakit",
        "provinsi",
        "kota_kabupaten",
        "kelas_rumah_sakit",
        "kepemilikan",
        "jumlah_tempat_tidur",
        "jumlah_jenis_layanan",
        "jumlah_tenaga_kerja",
        "tingkat_keterisian_tempat_tidur_persen",
        "rata_rata_lama_rawat_hari",
        "kunjungan_pasien_per_bulan",
        "status_implementasi_rme",
        "status_terhubung_satusehat",
        "skor_kematangan_digital",
        "rata_rata_waktu_respons_rujukan_menit",
        "anggaran_it_per_bed",
        "staf_it_per_100_bed",
        "iot_per_100_bed",
        "telemedicine_rate_per_1000",
        "pasien_per_tenaga_kerja",
        "bor_pressure",
        "expected_digital_maturity_oof",
        "digital_conversion_gap",
        "investment_intensity_score",
        "conversion_underperformance_flag",
        "investment_conversion_segment",
        "investment_underperformance_score",
        "maturity_tertile",
        "maturity_peer_pct",
        "digital_deficit_score",
        "referral_burden",
        "bor_burden",
        "los_burden",
        "workload_burden",
        "operational_burden_score",
        "double_inefficiency",
        "root_cause_primary",
        "root_cause_secondary",
        "root_cause_multilabel",
        "intervention_priority_score",
        "priority_rank",
        "intervention_tier",
        "recommended_intervention",
    },
    "hospital_priority.csv": {
        "id_rumah_sakit",
        "priority_rank",
        "intervention_tier",
        "intervention_priority_score",
        "double_inefficiency",
        "root_cause_primary",
        "recommended_intervention",
    },
    "peer_benchmarks.csv": {
        "id_rumah_sakit",
        "peer_median_skor_kematangan_digital",
        "peer_median_rata_rata_waktu_respons_rujukan_menit",
        "peer_median_anggaran_it_per_bed",
        "peer_median_staf_it_per_100_bed",
        "peer_median_iot_per_100_bed",
    },
    "root_cause_scores.csv": {
        "id_rumah_sakit",
        "root_cause_primary",
        "root_cause_multilabel",
        "root_cause_strength",
        "cause_score_it_capability",
        "cause_score_infrastructure",
        "cause_score_adoption",
        "cause_score_investment_conversion",
        "cause_score_capacity",
        "cause_score_integration",
    },
    "intervention_recommendations.csv": {
        "root_cause_primary",
        "recommended_intervention",
        "owner",
        "timeline",
        "kpi",
        "risiko_utama",
    },
    "executive_findings.csv": {"area", "temuan"},
    "outcome_association.csv": {
        "outcome",
        "arah_interpretasi",
        "n",
        "spearman_rho_dengan_maturity",
        "spearman_p",
    },
    "adjusted_association_hc3.csv": {
        "model",
        "term",
        "coefficient",
        "std_error_hc3",
        "ci_95_low",
        "ci_95_high",
        "p_value",
        "term_label",
    },
    "adjusted_model_summary.csv": {
        "model",
        "n",
        "p",
        "r2",
        "condition_number",
        "focal_terms",
    },
    "data_quality_audit.csv": {
        "variabel",
        "dtype",
        "missing_count",
        "missing_pct",
        "unique_count",
    },
}


def validate_columns(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    artifact_name: str,
) -> None:
    """Validate the minimum columns required from one artifact."""
    missing_columns = required_columns - set(dataframe.columns)
    if missing_columns:
        raise ArtifactContractError(
            f"{artifact_name} tidak memiliki kolom wajib: {sorted(missing_columns)}"
        )
    if dataframe.empty:
        raise ArtifactContractError(f"{artifact_name} tidak boleh kosong.")


def _read_csv(filename: str) -> pd.DataFrame:
    path = ARTIFACT_DIR / filename
    if not path.exists():
        raise ArtifactContractError(
            f"Artefak {filename} tidak ditemukan. Jalankan notebook analitik dan export ulang."
        )
    dataframe = pd.read_csv(path)
    validate_columns(dataframe, REQUIRED_COLUMNS[filename], filename)
    return dataframe


def _read_json(filename: str) -> dict[str, Any]:
    path = ARTIFACT_DIR / filename
    if not path.exists():
        raise ArtifactContractError(f"Artefak {filename} tidak ditemukan.")
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict) or not payload:
        raise ArtifactContractError(f"Artefak {filename} harus berupa objek JSON non-kosong.")
    return payload


def _validate_hospital_key(name: str, dataframe: pd.DataFrame, hospital_ids: set[str]) -> None:
    if "id_rumah_sakit" not in dataframe.columns:
        return
    if dataframe["id_rumah_sakit"].isna().any():
        raise ArtifactContractError(f"{name} memiliki ID rumah sakit kosong.")
    if not dataframe["id_rumah_sakit"].is_unique:
        raise ArtifactContractError(f"{name} memiliki duplikasi ID rumah sakit.")
    orphan_ids = set(dataframe["id_rumah_sakit"]) - hospital_ids
    if orphan_ids:
        raise ArtifactContractError(f"{name} memiliki ID tanpa induk: {sorted(orphan_ids)[:5]}")


def _validate_bundle(bundle: ArtifactBundle) -> None:
    hospitals = bundle.hospitals
    if len(hospitals) != EXPECTED_HOSPITAL_COUNT:
        raise ArtifactContractError(
            f"Primary dataset harus berisi {EXPECTED_HOSPITAL_COUNT} rumah sakit; "
            f"ditemukan {len(hospitals)}."
        )
    if hospitals["id_rumah_sakit"].isna().any() or not hospitals["id_rumah_sakit"].is_unique:
        raise ArtifactContractError("id_rumah_sakit pada primary dataset harus unik dan lengkap.")

    hospital_ids = set(hospitals["id_rumah_sakit"])
    for name, dataframe in {
        "hospital_priority.csv": bundle.priority,
        "peer_benchmarks.csv": bundle.peers,
        "root_cause_scores.csv": bundle.root_causes,
    }.items():
        _validate_hospital_key(name, dataframe, hospital_ids)
        if set(dataframe["id_rumah_sakit"]) != hospital_ids:
            raise ArtifactContractError(f"{name} tidak mencakup seluruh rumah sakit.")

    weights = bundle.analysis_config.get("priority_weights", {})
    if not weights or abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ArtifactContractError("Bobot priority score harus lengkap dan berjumlah 1,0.")


def _data_version() -> str:
    digest = hashlib.sha256()
    with (ARTIFACT_DIR / "hospital_features_scored.csv").open("rb") as file:
        for chunk in iter(lambda: file.read(64 * 1024), b""):
            digest.update(chunk)
    return f"data-{digest.hexdigest()[:12]}"


@st.cache_data(show_spinner="Memuat artefak analitik...")
def load_artifacts() -> ArtifactBundle:
    """Load and validate the complete immutable runtime artifact bundle."""
    bundle = ArtifactBundle(
        hospitals=_read_csv("hospital_features_scored.csv"),
        priority=_read_csv("hospital_priority.csv"),
        peers=_read_csv("peer_benchmarks.csv"),
        root_causes=_read_csv("root_cause_scores.csv"),
        recommendations=_read_csv("intervention_recommendations.csv"),
        executive_findings=_read_csv("executive_findings.csv"),
        outcome_associations=_read_csv("outcome_association.csv"),
        adjusted_associations=_read_csv("adjusted_association_hc3.csv"),
        adjusted_model_summary=_read_csv("adjusted_model_summary.csv"),
        data_quality=_read_csv("data_quality_audit.csv"),
        analysis_config=_read_json("analysis_config.json"),
        model_metrics=_read_json("model_metrics.json"),
        data_version=_data_version(),
    )
    _validate_bundle(bundle)
    return bundle

