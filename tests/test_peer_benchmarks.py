"""Peer medians must remain tied to the full hospital-class cohort."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from dashboard.data_loader import ArtifactBundle

PEER_METRICS = [
    "skor_kematangan_digital",
    "rata_rata_waktu_respons_rujukan_menit",
    "anggaran_it_per_bed",
    "staf_it_per_100_bed",
    "iot_per_100_bed",
    "telemedicine_rate_per_1000",
    "pasien_per_tenaga_kerja",
]


@pytest.mark.parametrize("metric", PEER_METRICS)
def test_persisted_peer_median_matches_full_class_median(
    bundle: ArtifactBundle, metric: str
) -> None:
    hospitals = bundle.hospitals
    expected = hospitals.groupby("kelas_rumah_sakit", observed=True)[metric].transform("median")
    expected_by_id = pd.Series(
        expected.to_numpy(), index=hospitals["id_rumah_sakit"], name="expected"
    )
    peer_by_id = bundle.peers.set_index("id_rumah_sakit")[f"peer_median_{metric}"]
    actual = peer_by_id.reindex(expected_by_id.index)
    assert np.allclose(actual, expected_by_id, equal_nan=True)


@pytest.mark.parametrize("metric", PEER_METRICS)
def test_persisted_peer_gap_is_actual_minus_median(bundle: ArtifactBundle, metric: str) -> None:
    peers = bundle.peers
    expected_gap = peers[metric] - peers[f"peer_median_{metric}"]
    assert np.allclose(peers[f"gap_vs_peer_{metric}"], expected_gap, equal_nan=True)
