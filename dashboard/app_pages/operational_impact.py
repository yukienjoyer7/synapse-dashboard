"""Operational impact and adjusted-association page."""

from __future__ import annotations

import streamlit as st

from dashboard.components.charts import render_chart
from dashboard.components.charts_operational import (
    build_adjusted_coefficients,
    build_maturity_outcome_medians,
    build_maturity_referral_scatter,
    build_operational_heatmap,
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
    format_days,
    format_decimal,
    format_minutes,
    format_percentage,
    format_signed,
)

context = get_page_context()
bundle = context.bundle
hospitals = context.hospitals
portfolio = bundle.hospitals

render_page_header(
    "Dampak terhadap operasional",
    "Apakah kesiapan digital berkaitan dengan performa operasional yang lebih baik?",
    bundle.data_version,
)
render_filter_context(context.filter_summary, len(hospitals), len(portfolio))

if hospitals.empty:
    render_empty_state()
    st.stop()

bor_lower, bor_upper = bundle.analysis_config["bor_reference_range"]
outside_bor = ~hospitals["tingkat_keterisian_tempat_tidur_persen"].between(bor_lower, bor_upper)
portfolio_outside_bor = ~portfolio["tingkat_keterisian_tempat_tidur_persen"].between(
    bor_lower, bor_upper
)
median_referral = hospitals["rata_rata_waktu_respons_rujukan_menit"].median()
portfolio_referral = portfolio["rata_rata_waktu_respons_rujukan_menit"].median()
median_bor = hospitals["tingkat_keterisian_tempat_tidur_persen"].median()
portfolio_bor = portfolio["tingkat_keterisian_tempat_tidur_persen"].median()
median_los = hospitals["rata_rata_lama_rawat_hari"].median()
portfolio_los = portfolio["rata_rata_lama_rawat_hari"].median()
median_telemedicine = hospitals["telemedicine_rate_per_1000"].median()
portfolio_telemedicine = portfolio["telemedicine_rate_per_1000"].median()

render_kpi_row(
    [
        KpiCard(
            "Median Respons Rujukan",
            format_minutes(median_referral),
            f"{format_signed(median_referral - portfolio_referral, suffix=' menit')} vs nasional",
            "STABIL" if median_referral <= portfolio_referral else "PERLU PERHATIAN",
            f"n={hospitals['rata_rata_waktu_respons_rujukan_menit'].notna().sum()} valid",
        ),
        KpiCard(
            "Median BOR",
            format_percentage(median_bor),
            f"{format_signed(median_bor - portfolio_bor, suffix=' pp')} vs nasional",
            "STABIL" if bor_lower <= median_bor <= bor_upper else "PERLU PERHATIAN",
            f"Rentang referensi konfigurasi: {bor_lower}–{bor_upper}%",
        ),
        KpiCard(
            "Di Luar Rentang BOR",
            format_percentage(outside_bor.mean() * 100),
            format_signed(
                (outside_bor.mean() - portfolio_outside_bor.mean()) * 100,
                suffix=" pp vs nasional",
            ),
            "PERLU PERHATIAN" if outside_bor.any() else "STABIL",
            f"{int(outside_bor.sum())} dari {len(hospitals)} rumah sakit",
        ),
        KpiCard(
            "Median LOS",
            format_days(median_los),
            f"{format_signed(median_los - portfolio_los, suffix=' hari')} vs nasional",
            "DATA TERBATAS",
            "Interpretasi memerlukan case mix",
        ),
        KpiCard(
            "Median Telemedicine / 1.000",
            format_decimal(median_telemedicine, 1),
            f"{format_signed(median_telemedicine - portfolio_telemedicine)} vs nasional",
            "STABIL" if median_telemedicine >= portfolio_telemedicine else "PERLU PERHATIAN",
            f"n={hospitals['telemedicine_rate_per_1000'].notna().sum()} valid",
        ),
    ],
    key="kpi-row-operational",
)

combined_summary = bundle.adjusted_model_summary.loc[
    bundle.adjusted_model_summary["model"].eq("Gabungan")
].iloc[0]
render_chart(
    build_adjusted_coefficients(bundle.adjusted_associations),
    title="Estimasi model gabungan menunjukkan arah dan ketidakpastian yang berbeda",
    subtitle=(
        f"Outcome: waktu respons rujukan · HC3 95% CI · n={int(combined_summary['n'])} · "
        f"R²={combined_summary['r2']:.3f}"
    ),
    insight=(
        "Kematangan dihitung per kenaikan 10 poin; RME dan SatuSehat adalah perbedaan terhadap "
        "kategori referensi. Interval yang melintasi nol menunjukkan ketidakpastian arah."
    ),
    key="operational-adjusted-coefficients",
)

render_chart(
    build_maturity_referral_scatter(hospitals),
    title="Sebaran rumah sakit memperlihatkan variasi besar pada tingkat kematangan yang sama",
    subtitle=(
        f"Cohort filter aktif · garis titik = median cohort · n="
        f"{hospitals['rata_rata_waktu_respons_rujukan_menit'].notna().sum()}"
    ),
    insight=(
        "Tidak ada garis regresi yang dihitung ulang di dashboard. Gunakan estimasi tersesuaikan "
        "di atas untuk inferensi asosiasi; klik titik untuk memilih rumah sakit."
    ),
    key="operational-maturity-referral",
    selectable=True,
)

left, right = st.columns(2, gap="large")
with left:
    render_chart(
        build_maturity_outcome_medians(bundle.outcome_associations),
        title="Median outcome berubah dengan tertile kematangan",
        subtitle="Ringkasan deskriptif seluruh portofolio dari artefak notebook",
        insight=(
            "Setiap panel memakai skala outcome sendiri. Tekanan BOR adalah deviasi dari rentang "
            "referensi, bukan BOR mentah."
        ),
        key="operational-outcome-medians",
    )
with right:
    render_chart(
        build_operational_heatmap(hospitals),
        title="Profil beban menyoroti komponen operasional yang berbeda",
        subtitle="Rata-rata persentil beban dalam kelas · cohort filter aktif",
        insight=(
            "Nilai lebih tinggi selalu berarti posisi beban yang lebih berat. Komponen telah "
            "dihitung oleh notebook sebelum dashboard dimuat."
        ),
        key="operational-burden-heatmap",
    )

combined_estimate = bundle.adjusted_associations.loc[
    (bundle.adjusted_associations["model"].eq("Gabungan"))
    & (bundle.adjusted_associations["term"].eq("maturity_per_10"))
].iloc[0]
governance = bundle.model_metrics["model_governance"]
with st.container(border=True, key="operational-interpretation"):
    st.subheader("Interpretasi untuk keputusan", anchor=False)
    st.markdown(
        f"""
- Dalam model gabungan, kenaikan **10 poin kematangan digital berkaitan dengan perubahan
  {combined_estimate["coefficient"]:.2f} menit** pada waktu respons rujukan
  (95% CI {combined_estimate["ci_95_low"]:.2f} hingga
  {combined_estimate["ci_95_high"]:.2f}; n={int(combined_summary["n"])}).
- Model asosiasi menjelaskan **{combined_summary["r2"]:.1%}** variasi outcome dan memakai
  {int(combined_summary["p"])} parameter, termasuk kematangan, RME, dan koneksi SatuSehat.
- Model prediktif individual tidak melewati validation gate
  (Ridge CV R² ≈ {bundle.model_metrics["operational_model"][0]["R2_mean"]:.3f};
  eligibility skenario = **{governance["scenario_model_eligible"]}**). Dashboard karena itu tidak
  menampilkan prediksi atau simulasi per rumah sakit.
- Temuan ini **observasional, bukan kausal**. BOR perlu konteks kelas dan kapasitas; LOS perlu
  case mix; status implementasi biner tidak mengukur kualitas penggunaan.
"""
    )

st.subheader("Tabel pembanding operasional", anchor=False)
operational_table = hospitals.sort_values("rata_rata_waktu_respons_rujukan_menit", ascending=False)
render_paginated_table(
    operational_table,
    key="operational-comparison",
    column_order=[
        "id_rumah_sakit",
        "nama_rumah_sakit",
        "kelas_rumah_sakit",
        "skor_kematangan_digital",
        "rata_rata_waktu_respons_rujukan_menit",
        "tingkat_keterisian_tempat_tidur_persen",
        "rata_rata_lama_rawat_hari",
        "telemedicine_rate_per_1000",
        "pasien_per_tenaga_kerja",
        "operational_burden_score",
    ],
    column_config={
        "id_rumah_sakit": st.column_config.TextColumn("ID", pinned=True),
        "nama_rumah_sakit": st.column_config.TextColumn("Rumah sakit", pinned=True),
        "kelas_rumah_sakit": "Kelas",
        "skor_kematangan_digital": st.column_config.NumberColumn("Kematangan", format="%.1f"),
        "rata_rata_waktu_respons_rujukan_menit": st.column_config.NumberColumn(
            "Respons (menit)", format="%.1f"
        ),
        "tingkat_keterisian_tempat_tidur_persen": st.column_config.NumberColumn(
            "BOR", format="%.1f%%"
        ),
        "rata_rata_lama_rawat_hari": st.column_config.NumberColumn("LOS (hari)", format="%.1f"),
        "telemedicine_rate_per_1000": st.column_config.NumberColumn(
            "Telemedicine/1.000", format="%.1f"
        ),
        "pasien_per_tenaga_kerja": st.column_config.NumberColumn(
            "Pasien/tenaga kerja", format="%.2f"
        ),
        "operational_burden_score": st.column_config.ProgressColumn(
            "Beban", min_value=0, max_value=1, format="%.2f"
        ),
    },
)

render_method_note(
    "Metode asosiasi dan batas interpretasi",
    """
Koefisien dan confidence interval berasal langsung dari `adjusted_association_hc3.csv`; dashboard
tidak memodelkan ulang data. Model gabungan menggunakan standard error robust HC3. Ringkasan
tertile berasal dari `outcome_association.csv` dan bersifat deskriptif. Rentang BOR 60–85% adalah
parameter konfigurasi analisis, bukan standar universal. Seluruh hasil harus dibaca bersama
konteks kelas rumah sakit, kapasitas, kualitas implementasi, dan case mix.
""",
)
