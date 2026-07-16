"""CSV provenance and encoding behavior."""

from __future__ import annotations

from datetime import UTC, datetime
from io import BytesIO

import pandas as pd

from dashboard.utils.export import METADATA_COLUMNS, prepare_csv_export


def test_csv_export_embeds_provenance_and_utf8_bom() -> None:
    source = pd.DataFrame(
        {
            "id_rumah_sakit": ["RS0001", "RS0002"],
            "nama_rumah_sakit": ["RS Cempaka", "RS Sehat"],
        }
    )
    timestamp = datetime(2026, 7, 16, 12, 0, tzinfo=UTC)
    payload = prepare_csv_export(
        source,
        active_filters="Provinsi: Jawa Barat",
        benchmark_definition="Peer kelas tetap",
        data_version="data-abc123def456",
        timestamp=timestamp,
    )

    assert payload.startswith(b"\xef\xbb\xbf")
    exported = pd.read_csv(BytesIO(payload))
    assert exported.columns.tolist()[:4] == METADATA_COLUMNS
    assert exported["export_timestamp_utc"].eq(timestamp.isoformat()).all()
    assert exported["active_filters"].eq("Provinsi: Jawa Barat").all()
    assert exported["benchmark_definition"].eq("Peer kelas tetap").all()
    assert exported["data_version"].eq("data-abc123def456").all()
    assert source.columns.tolist() == ["id_rumah_sakit", "nama_rumah_sakit"]


def test_empty_export_retains_metadata_and_source_headers() -> None:
    payload = prepare_csv_export(
        pd.DataFrame(columns=["id_rumah_sakit"]),
        active_filters="Tidak ada hasil",
        benchmark_definition="Peer kelas tetap",
        data_version="data-abc123def456",
    )
    header = payload.decode("utf-8-sig").splitlines()[0]
    assert header.split(",") == [*METADATA_COLUMNS, "id_rumah_sakit"]
