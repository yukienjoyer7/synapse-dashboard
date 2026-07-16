"""Executive summary page."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from dashboard.components.charts import render_chart
from dashboard.components.charts_executive import (
    build_priority_quadrant,
    build_province_heatmap,
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
from dashboard.utils.export import render_csv_download
from dashboard.utils.formatting import (
    format_decimal,
    format_minutes,
    format_percentage,
    format_score,
    format_signed,
)

context = get_page_context()
bundle = context.bundle
hospitals = context.hospitals
portfolio = bundle.hospitals

render_page_header(
    "Ringkasan eksekutif",
    "Di bagian mana konsorsium harus memusatkan perhatian?",
    bundle.data_version,
)
render_filter_context(context.filter_summary, len(hospitals), len(portfolio))

if hospitals.empty:
    render_empty_state()
    st.stop()


def _share(mask: pd.Series) -> float:
    return float(mask.mean() * 100)


median_maturity = hospitals["skor_kematangan_digital"].median()
national_maturity = portfolio["skor_kematangan_digital"].median()
satusehat_coverage = _share(hospitals["status_terhubung_satusehat"].eq("Ya"))
national_satusehat = _share(portfolio["status_terhubung_satusehat"].eq("Ya"))
median_referral = hospitals["rata_rata_waktu_respons_rujukan_menit"].median()
national_referral = portfolio["rata_rata_waktu_respons_rujukan_menit"].median()
outside_bor = _share(hospitals["bor_pressure"].gt(0))
national_outside_bor = _share(portfolio["bor_pressure"].gt(0))
conversion_failure = _share(hospitals["conversion_underperformance_flag"].astype(bool))
double_inefficiency = int(hospitals["double_inefficiency"].sum())

render_kpi_row(
    [
        KpiCard(
            "Median Kematangan Digital",
            format_score(median_maturity),
            f"{format_signed(median_maturity - national_maturity)} vs median nasional",
            "STABIL" if median_maturity >= national_maturity else "PERLU PERHATIAN",
            f"n={len(hospitals)} rumah sakit",
            "Median skor kematangan digital pada filter aktif; semakin tinggi semakin matang.",
        ),
        KpiCard(
            "Cakupan SatuSehat",
            format_percentage(satusehat_coverage),
            f"{format_signed(satusehat_coverage - national_satusehat, suffix=' pp')} vs nasional",
            "BAIK" if satusehat_coverage >= national_satusehat else "PERLU PERHATIAN",
            f"{int(hospitals['status_terhubung_satusehat'].eq('Ya').sum())} dari {len(hospitals)}",
            "Persentase rumah sakit berstatus terhubung SatuSehat.",
        ),
        KpiCard(
            "Median Respons Rujukan",
            format_minutes(median_referral),
            f"{format_signed(median_referral - national_referral, suffix=' menit')} vs nasional",
            "STABIL" if median_referral <= national_referral else "PERLU PERHATIAN",
            f"n={hospitals['rata_rata_waktu_respons_rujukan_menit'].notna().sum()} valid",
            "Median waktu respons rujukan; semakin rendah semakin baik.",
        ),
        KpiCard(
            "Di Luar Rentang BOR",
            format_percentage(outside_bor),
            f"{format_signed(outside_bor - national_outside_bor, suffix=' pp')} vs nasional",
            "STABIL" if outside_bor <= national_outside_bor else "PERLU PERHATIAN",
            "Rentang referensi 60–85%",
            "Share rumah sakit dengan BOR di bawah 60% atau di atas 85%.",
        ),
        KpiCard(
            "Outlier Konversi Investasi",
            format_percentage(conversion_failure),
            "Definisi ketat notebook",
            "PERLU PERHATIAN" if conversion_failure > 0 else "STABIL",
            f"{int(hospitals['conversion_underperformance_flag'].sum())} rumah sakit",
            "Investasi relatif tinggi dengan kematangan di bawah ekspektasi model.",
        ),
        KpiCard(
            "Inefisiensi Ganda",
            format_decimal(double_inefficiency, 0),
            format_percentage(double_inefficiency / len(hospitals) * 100),
            "PRIORITAS" if double_inefficiency > 0 else "STABIL",
            f"{double_inefficiency} dari {len(hospitals)}",
            "Kuartil bawah kematangan dalam kelas dan kuartil atas beban operasional.",
        ),
    ],
    key="kpi-row-executive",
)

digital_threshold = float(bundle.analysis_config["digital_deficit_quantile"])
operational_threshold = float(bundle.analysis_config["operational_burden_quantile"])
selected_hospital_id = st.session_state.get("selected_hospital_id")
quadrant = build_priority_quadrant(
    hospitals,
    digital_threshold=digital_threshold,
    operational_threshold=operational_threshold,
    selected_hospital_id=selected_hospital_id,
)
render_chart(
    quadrant,
    title="Kematangan relatif kelas dan beban operasional memisahkan prioritas asesmen",
    subtitle=f"Ukuran titik = jumlah tempat tidur · n={len(hospitals)} · klik titik untuk memilih",
    insight=(
        f"{double_inefficiency} rumah sakit pada cohort aktif memenuhi kedua threshold. "
        "Status ini adalah skrining deskriptif, bukan diagnosis kinerja."
    ),
    key="executive-priority-quadrant",
    selectable=True,
)

left, right = st.columns([1.25, 1], gap="large")
with left:
    heatmap = build_province_heatmap(hospitals)
    render_chart(
        heatmap,
        title="Provinsi dengan konsentrasi sinyal tertinggi",
        subtitle="Maksimal 15 provinsi; nilai adalah median atau share pada filter aktif",
        insight=(
            "Gunakan heatmap untuk memusatkan investigasi, bukan untuk menyimpulkan efek geografis."
        ),
        key="executive-province-heatmap",
    )
with right:
    with st.container(border=True):
        st.subheader("Temuan portofolio", anchor=False)
        st.caption(
            "Temuan berikut berasal langsung dari artefak notebook dan berlaku untuk "
            "seluruh sampel."
        )
        finding_order = ["Scope", "Prioritas", "Keputusan"]
        findings = bundle.executive_findings.set_index("area")["temuan"]
        for area in finding_order:
            st.markdown(f"**{area}**")
            st.write(findings.get(area, "Temuan tidak tersedia."))

st.subheader("Rumah sakit dengan prioritas tertinggi", anchor=False)
visible_ids = set(hospitals["id_rumah_sakit"])
watchlist = bundle.priority.loc[bundle.priority["id_rumah_sakit"].isin(visible_ids)].head(10)
render_paginated_table(
    watchlist,
    key="executive-watchlist",
    page_size=10,
    height=430,
    column_order=[
        "priority_rank",
        "id_rumah_sakit",
        "nama_rumah_sakit",
        "provinsi",
        "kelas_rumah_sakit",
        "intervention_priority_score",
        "root_cause_primary",
    ],
    column_config={
        "priority_rank": st.column_config.NumberColumn("Peringkat", format="%d"),
        "id_rumah_sakit": st.column_config.TextColumn("ID", pinned=True),
        "nama_rumah_sakit": st.column_config.TextColumn("Rumah sakit", pinned=True),
        "provinsi": "Provinsi",
        "kelas_rumah_sakit": "Kelas",
        "intervention_priority_score": st.column_config.ProgressColumn(
            "Skor prioritas", min_value=0, max_value=1, format="%.3f"
        ),
        "root_cause_primary": "Hambatan dominan",
    },
)
render_csv_download(
    hospitals,
    label="Unduh portofolio terfilter",
    filename="healthops_portofolio_terfilter.csv",
    key="download-executive-portfolio",
    active_filters=context.filter_summary,
    benchmark_definition="Seluruh portofolio nasional; peer tetap menurut kelas",
    data_version=bundle.data_version,
)

if st.session_state.get("selected_hospital_id"):
    with st.container(horizontal=True, horizontal_alignment="right"):
        if st.button(
            "Lihat rumah sakit terpilih",
            icon=":material/open_in_new:",
            type="primary",
        ):
            st.switch_page(Path(__file__).with_name("hospital_explorer.py"))

render_method_note(
    "Cara membaca ringkasan",
    "\n".join(
        [
            "- Benchmark KPI menggunakan median atau share seluruh portofolio dan tidak "
            "berubah diam-diam saat filter aktif.",
            "- Inefisiensi ganda menggunakan definisi notebook: persentil kematangan "
            "dalam kelas ≤ 0,25 dan beban operasional ≥ 0,75.",
            "- Skor prioritas adalah indeks deskriptif untuk mengurutkan asesmen, bukan "
            "probabilitas risiko klinis.",
        ]
    ),
)
