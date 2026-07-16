"""Digital readiness and investment page."""

from __future__ import annotations

import streamlit as st

from dashboard.components.charts import render_chart
from dashboard.components.charts_digital import (
    build_actual_expected,
    build_conversion_matrix,
    build_investment_components,
    build_maturity_distribution,
)
from dashboard.components.common import (
    KpiCard,
    render_empty_state,
    render_filter_context,
    render_kpi_row,
    render_method_note,
    render_page_header,
)
from dashboard.components.tables import render_paginated_table
from dashboard.context import get_page_context
from dashboard.utils.formatting import (
    format_decimal,
    format_percentage,
    format_score,
    format_signed,
)

context = get_page_context()
bundle = context.bundle
hospitals = context.hospitals
portfolio = bundle.hospitals

render_page_header(
    "Kesiapan digital & investasi",
    "Apakah sumber daya IT berhasil dikonversi menjadi kemampuan digital?",
    bundle.data_version,
)
render_filter_context(context.filter_summary, len(hospitals), len(portfolio))

if hospitals.empty:
    render_empty_state()
    st.stop()


def _share(column: str, expected: object = True) -> float:
    return float(hospitals[column].eq(expected).mean() * 100)


median_maturity = hospitals["skor_kematangan_digital"].median()
national_maturity = portfolio["skor_kematangan_digital"].median()
rme_rate = _share("status_implementasi_rme", "Ya")
satusehat_rate = _share("status_terhubung_satusehat", "Ya")
failure_rate = _share("conversion_underperformance_flag")
median_staff = hospitals["staf_it_per_100_bed"].median()
national_staff = portfolio["staf_it_per_100_bed"].median()

render_kpi_row(
    [
        KpiCard(
            "Median Kematangan Digital",
            format_score(median_maturity),
            f"{format_signed(median_maturity - national_maturity)} vs nasional",
            "STABIL" if median_maturity >= national_maturity else "PERLU PERHATIAN",
            f"n={len(hospitals)}",
        ),
        KpiCard(
            "Implementasi RME",
            format_percentage(rme_rate),
            "Status adopsi biner",
            "BAIK" if rme_rate >= 90 else "PERLU PERHATIAN",
            f"{int(hospitals['status_implementasi_rme'].eq('Ya').sum())} rumah sakit",
        ),
        KpiCard(
            "Koneksi SatuSehat",
            format_percentage(satusehat_rate),
            "Status koneksi biner",
            "BAIK" if satusehat_rate >= 85 else "PERLU PERHATIAN",
            f"{int(hospitals['status_terhubung_satusehat'].eq('Ya').sum())} rumah sakit",
        ),
        KpiCard(
            "Outlier Konversi Investasi",
            format_percentage(failure_rate),
            "Definisi ketat notebook",
            "PERLU PERHATIAN" if failure_rate > 0 else "STABIL",
            f"{int(hospitals['conversion_underperformance_flag'].sum())} rumah sakit",
        ),
        KpiCard(
            "Median Staf IT per 100 Bed",
            format_decimal(median_staff, 2),
            f"{format_signed(median_staff - national_staff, 2)} vs nasional",
            "STABIL" if median_staff >= national_staff else "PERLU PERHATIAN",
            f"n={hospitals['staf_it_per_100_bed'].notna().sum()} valid",
        ),
    ],
    key="kpi-row-digital",
)

left, right = st.columns(2, gap="large")
with left:
    render_chart(
        build_maturity_distribution(hospitals, "kelas_rumah_sakit"),
        title="Kematangan digital berbeda di dalam dan antar kelas",
        subtitle=f"Distribusi lengkap dan titik rumah sakit · n={len(hospitals)}",
        insight="Median saja tidak menangkap variasi kesiapan digital di dalam kelas yang sama.",
        key="digital-maturity-class",
    )
with right:
    render_chart(
        build_maturity_distribution(hospitals, "kepemilikan"),
        title="Kepemilikan memberi konteks, bukan penjelasan tunggal",
        subtitle=f"Distribusi kematangan menurut kepemilikan · n={len(hospitals)}",
        insight=(
            "Gunakan distribusi dan ukuran cohort sebelum menarik kesimpulan antar-kepemilikan."
        ),
        key="digital-maturity-ownership",
    )

selected_hospital_id = st.session_state.get("selected_hospital_id")
render_chart(
    build_actual_expected(hospitals, selected_hospital_id),
    title="Investasi tidak selalu dikonversi menjadi kematangan sesuai ekspektasi",
    subtitle="Aktual vs estimasi out-of-fold · garis diagonal menunjukkan aktual = ekspektasi",
    insight=(
        f"{int(hospitals['conversion_underperformance_flag'].sum())} rumah sakit pada cohort aktif "
        "memenuhi definisi ketat outlier konversi dan perlu audit sebelum ekspansi anggaran."
    ),
    key="digital-actual-expected",
    selectable=True,
)

left, right = st.columns(2, gap="large")
with left:
    render_chart(
        build_conversion_matrix(hospitals),
        title="Segmen konversi memisahkan keterbatasan sumber daya dari underperformance",
        subtitle="Intensitas investasi dan gap aktual terhadap ekspektasi model",
        insight=(
            "Segmen adalah alat diagnosis portofolio; gap negatif tidak membuktikan "
            "investasi gagal."
        ),
        key="digital-conversion-matrix",
        selectable=True,
    )
with right:
    render_chart(
        build_investment_components(hospitals),
        title="Komponen investasi menunjukkan jenis sumber daya yang berbeda",
        subtitle="Median persentil nasional per segmen konversi",
        insight="Bandingkan staf, infrastruktur, dan anggaran sebelum memilih intervensi.",
        key="digital-investment-components",
    )

st.subheader("Daftar investigasi konversi investasi", anchor=False)
search = st.text_input(
    "Cari rumah sakit pada tabel",
    placeholder="Ketik nama, ID, atau provinsi",
    key="table_search_digital",
)
action_table = hospitals.sort_values("digital_conversion_gap", ascending=True)
if search:
    query = search.casefold()
    action_table = action_table.loc[
        action_table[["id_rumah_sakit", "nama_rumah_sakit", "provinsi"]]
        .astype(str)
        .apply(lambda column: column.str.casefold().str.contains(query, regex=False))
        .any(axis=1)
    ]
render_paginated_table(
    action_table,
    key="digital-action",
    column_order=[
        "id_rumah_sakit",
        "nama_rumah_sakit",
        "provinsi",
        "kelas_rumah_sakit",
        "skor_kematangan_digital",
        "expected_digital_maturity_oof",
        "digital_conversion_gap",
        "anggaran_it_per_bed",
        "staf_it_per_100_bed",
        "iot_per_100_bed",
        "investment_conversion_segment",
    ],
    column_config={
        "id_rumah_sakit": st.column_config.TextColumn("ID", pinned=True),
        "nama_rumah_sakit": st.column_config.TextColumn("Rumah sakit", pinned=True),
        "provinsi": "Provinsi",
        "kelas_rumah_sakit": "Kelas",
        "skor_kematangan_digital": st.column_config.NumberColumn("Aktual", format="%.1f"),
        "expected_digital_maturity_oof": st.column_config.NumberColumn("Ekspektasi", format="%.1f"),
        "digital_conversion_gap": st.column_config.NumberColumn("Gap", format="%+.1f"),
        "anggaran_it_per_bed": st.column_config.NumberColumn(
            "Anggaran/bed (Rp juta)", format="%.1f"
        ),
        "staf_it_per_100_bed": st.column_config.NumberColumn("Staf IT/100 bed", format="%.2f"),
        "iot_per_100_bed": st.column_config.NumberColumn("IoT/100 bed", format="%.1f"),
        "investment_conversion_segment": "Segmen konversi",
    },
)

if st.session_state.get("selected_hospital_id"):
    with st.container(horizontal=True, horizontal_alignment="right"):
        if st.button(
            "Buka profil rumah sakit",
            icon=":material/open_in_new:",
            type="primary",
        ):
            st.switch_page("app_pages/hospital_explorer.py")

render_method_note(
    "Definisi konversi investasi",
    """
Kematangan ekspektasian adalah prediksi out-of-fold dari model kematangan digital. Kesenjangan
konversi = kematangan aktual − kematangan ekspektasian. Nilai negatif menunjukkan posisi di bawah
ekspektasi model, bukan bukti kausal bahwa investasi tidak efektif. Seluruh score dan segmentasi
berasal dari notebook dan tidak dihitung ulang oleh dashboard.
""",
)
