"""Methodology, governance, and data-quality page."""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from dashboard.components.charts import render_chart
from dashboard.components.charts_methodology import build_missingness_chart
from dashboard.components.common import KpiCard, render_kpi_row, render_page_header
from dashboard.context import get_page_context
from dashboard.utils.export import render_csv_download
from dashboard.utils.formatting import format_integer, format_percentage

context = get_page_context()
bundle = context.bundle
hospitals = bundle.hospitals
quality = bundle.data_quality
config = bundle.analysis_config


def _render_table(dataframe: pd.DataFrame, key: str) -> None:
    st.dataframe(
        dataframe,
        key=key,
        width="stretch",
        hide_index=True,
        row_height=36,
    )


def _kpi_dictionary() -> pd.DataFrame:
    bor_lower, bor_upper = config["bor_reference_range"]
    return pd.DataFrame(
        [
            {
                "KPI": "Jumlah rumah sakit",
                "Kolom sumber": "id_rumah_sakit",
                "Formula": "count distinct ID setelah filter",
                "Unit": "rumah sakit",
                "Arah": "konteks denominator",
                "Halaman": "Ringkasan",
            },
            {
                "KPI": "Median kematangan digital",
                "Kolom sumber": "skor_kematangan_digital",
                "Formula": "median pada cohort aktif",
                "Unit": "skor 0–100",
                "Arah": "lebih tinggi = lebih matang",
                "Halaman": "Ringkasan, Digital",
            },
            {
                "KPI": "Cakupan RME",
                "Kolom sumber": "status_implementasi_rme",
                "Formula": "count(Ya) / n cohort × 100",
                "Unit": "% rumah sakit",
                "Arah": "lebih tinggi = adopsi lebih luas",
                "Halaman": "Ringkasan, Digital",
            },
            {
                "KPI": "Cakupan SatuSehat",
                "Kolom sumber": "status_terhubung_satusehat",
                "Formula": "count(Ya) / n cohort × 100",
                "Unit": "% rumah sakit",
                "Arah": "lebih tinggi = koneksi lebih luas",
                "Halaman": "Ringkasan, Digital",
            },
            {
                "KPI": "Median respons rujukan",
                "Kolom sumber": "rata_rata_waktu_respons_rujukan_menit",
                "Formula": "median pada nilai valid cohort",
                "Unit": "menit",
                "Arah": "lebih rendah = lebih cepat",
                "Halaman": "Ringkasan, Operasional",
            },
            {
                "KPI": "Di luar rentang BOR",
                "Kolom sumber": "tingkat_keterisian_tempat_tidur_persen",
                "Formula": f"share BOR < {bor_lower}% atau > {bor_upper}%",
                "Unit": "% rumah sakit",
                "Arah": "lebih rendah = lebih sedikit deviasi",
                "Halaman": "Operasional",
            },
            {
                "KPI": "Outlier konversi investasi",
                "Kolom sumber": "conversion_underperformance_flag",
                "Formula": "share flag ketat notebook",
                "Unit": "% rumah sakit",
                "Arah": "lebih rendah = lebih sedikit audit",
                "Halaman": "Digital",
            },
            {
                "KPI": "Inefisiensi ganda",
                "Kolom sumber": "double_inefficiency",
                "Formula": "share flag governed notebook",
                "Unit": "% rumah sakit",
                "Arah": "lebih rendah = lebih sedikit prioritas",
                "Halaman": "Prioritas",
            },
            {
                "KPI": "Skor Prioritas",
                "Kolom sumber": "intervention_priority_score",
                "Formula": "jumlah komponen berbobot",
                "Unit": "skor 0–1",
                "Arah": "lebih tinggi = prioritas lebih tinggi",
                "Halaman": "Prioritas, Explorer",
            },
        ]
    )


def _derived_metrics() -> pd.DataFrame:
    return pd.DataFrame(
        [
            ("Anggaran IT/bed", "anggaran IT tahunan / jumlah bed", "Rp juta/bed"),
            ("Staf IT/100 bed", "jumlah staf IT / jumlah bed × 100", "staf/100 bed"),
            ("IoT/100 bed", "jumlah perangkat IoT / jumlah bed × 100", "unit/100 bed"),
            (
                "Telemedicine/1.000",
                "kunjungan telemedicine / kunjungan pasien × 1.000",
                "kunjungan/1.000",
            ),
            (
                "Pasien/tenaga kerja",
                "kunjungan pasien bulanan / jumlah tenaga kerja",
                "rasio",
            ),
            (
                "Intensitas investasi",
                "gabungan persentil anggaran, staf IT, dan IoT",
                "skor 0–1",
            ),
            (
                "Expected maturity",
                "prediksi out-of-fold model kematangan",
                "skor 0–100",
            ),
            (
                "Conversion gap",
                "kematangan aktual − expected maturity OOF",
                "poin",
            ),
            (
                "Beban operasional",
                "gabungan beban respons, BOR, LOS, dan workload dalam kelas",
                "skor 0–1",
            ),
            (
                "Defisit digital",
                "kebalikan persentil kematangan dalam kelas",
                "skor 0–1",
            ),
            (
                "Skor Prioritas",
                "defisit digital × bobot + beban × bobot + underperformance × bobot",
                "skor 0–1",
            ),
        ],
        columns=["Metrik", "Formula/definisi", "Unit"],
    )


source_missing = int(quality["missing_count"].sum())
source_cells = len(hospitals) * len(quality)
coverage = (1 - source_missing / source_cells) * 100
duplicate_ids = int(hospitals["id_rumah_sakit"].duplicated().sum())

render_page_header(
    "Metodologi & kualitas data",
    "Dapatkah temuan dashboard dipercaya, ditelusuri, dan direproduksi?",
    bundle.data_version,
)

render_kpi_row(
    [
        KpiCard(
            "Unit Analisis",
            format_integer(len(hospitals)),
            "1 baris per rumah sakit",
            "STABIL",
            "276 ID unik",
        ),
        KpiCard(
            "Cakupan Geografis",
            format_integer(hospitals["provinsi"].nunique()),
            "provinsi pada sampel",
            "DATA TERBATAS",
            "Tidak diklaim representatif nasional",
        ),
        KpiCard(
            "Variabel Sumber",
            format_integer(len(quality)),
            f"{hospitals.shape[1]} kolom artefak scored",
            "STABIL",
            "20 kolom raw dalam audit",
        ),
        KpiCard(
            "Kelengkapan Sumber",
            format_percentage(coverage, 2),
            f"{source_missing} sel missing sebelum imputasi",
            "PERLU PERHATIAN" if source_missing else "BAIK",
            f"Denominator {source_cells:,} sel".replace(",", "."),
        ),
        KpiCard(
            "Duplikasi ID",
            format_integer(duplicate_ids),
            "validasi primary key",
            "BAIK" if duplicate_ids == 0 else "PERLU PERHATIAN",
            "Kontrak data runtime",
        ),
    ],
    key="kpi-row-methodology",
)

dataset_tab, metric_tab, priority_tab, model_tab, quality_tab, limit_tab = st.tabs(
    [
        "Dataset & KPI",
        "Derived & Peer",
        "Prioritas",
        "Model Statistik",
        "Kualitas Data",
        "Batasan & Versi",
    ]
)

with dataset_tab:
    st.subheader("Kontrak dataset", anchor=False)
    geographic_scope = f"{len(hospitals)} rumah sakit di {hospitals['provinsi'].nunique()} provinsi"
    dataset_summary = pd.DataFrame(
        [
            ("Unit analisis", "Rumah sakit; satu baris per ID"),
            ("Jenis data", "Observasional, cross-sectional, tanpa data pasien individual"),
            ("Cakupan", geographic_scope),
            ("Sumber runtime", "Artefak CSV/JSON yang dihasilkan notebook analitik"),
            ("Sumber upstream", "dataset_smart_hospital_indonesia.csv"),
            ("Data utama", "20 variabel sumber; 90 kolom pada artefak scored"),
            ("Versi data", bundle.data_version),
        ],
        columns=["Atribut", "Nilai"],
    )
    _render_table(dataset_summary, "methodology-dataset-summary")

    st.subheader("Kamus KPI", anchor=False)
    st.caption("Formula mengikuti denominator cohort aktif kecuali dinyatakan lain.")
    _render_table(_kpi_dictionary(), "methodology-kpi-dictionary")

with metric_tab:
    st.subheader("Metrik turunan", anchor=False)
    st.caption("Seluruh metrik ini dihitung oleh notebook dan hanya dibaca oleh dashboard.")
    _render_table(_derived_metrics(), "methodology-derived-metrics")

    st.subheader("Definisi peer", anchor=False)
    st.info(
        "Peer utama adalah seluruh rumah sakit dengan kelas yang sama. Benchmark peer tidak "
        "mengikuti filter dashboard, sehingga perbandingan sebuah rumah sakit tetap konsisten. "
        "Median, gap, persentil, dan komponen beban peer telah dipersistenkan oleh notebook.",
        icon=":material/groups:",
    )
    peer_sizes = (
        hospitals.groupby("kelas_rumah_sakit", observed=True)
        .size()
        .rename("Jumlah rumah sakit")
        .reset_index()
        .rename(columns={"kelas_rumah_sakit": "Kelas"})
    )
    _render_table(peer_sizes, "methodology-peer-sizes")

with priority_tab:
    st.subheader("Formula Skor Prioritas", anchor=False)
    weights = config["priority_weights"]
    st.latex(
        rf"Priority = {weights['digital_deficit']:.2f}D + "
        rf"{weights['operational_burden']:.2f}O + "
        rf"{weights['investment_underperformance']:.2f}I"
    )
    weight_table = pd.DataFrame(
        [
            ("D", "Defisit digital", weights["digital_deficit"]),
            ("O", "Beban operasional", weights["operational_burden"]),
            (
                "I",
                "Underperformance konversi investasi",
                weights["investment_underperformance"],
            ),
        ],
        columns=["Simbol", "Komponen", "Bobot"],
    )
    _render_table(weight_table, "methodology-priority-weights")

    st.subheader("Threshold yang dikelola konfigurasi", anchor=False)
    thresholds = pd.DataFrame(
        [
            ("Rentang referensi BOR", str(config["bor_reference_range"]), "%"),
            ("Quantile defisit digital", config["digital_deficit_quantile"], "quantile"),
            (
                "Quantile beban operasional",
                config["operational_burden_quantile"],
                "quantile",
            ),
            (
                "Conversion underperformance",
                config["conversion_underperformance_z"],
                "peer z-score",
            ),
            (
                "Primary root cause",
                config["root_cause_primary_threshold"],
                "score",
            ),
            (
                "Secondary root cause",
                config["root_cause_secondary_threshold"],
                "score",
            ),
        ],
        columns=["Parameter", "Nilai", "Unit/interpretasi"],
    )
    thresholds["Nilai"] = thresholds["Nilai"].astype(str)
    _render_table(thresholds, "methodology-thresholds")
    st.warning(
        "Skor Prioritas adalah alat triase portofolio, bukan probabilitas risiko klinis, "
        "peringkat mutu, atau bukti manfaat intervensi.",
        icon=":material/warning:",
    )

with model_tab:
    st.subheader("Model asosiasi waktu respons rujukan", anchor=False)
    st.caption(
        "OLS dengan standard error robust HC3. Dashboard membaca koefisien dan ringkasan yang "
        "telah dipersistenkan; tidak menjalankan regresi."
    )
    association_summary = bundle.adjusted_model_summary.rename(
        columns={
            "model": "Model",
            "n": "n",
            "p": "Parameter",
            "r2": "R²",
            "condition_number": "Condition number",
            "focal_terms": "Focal terms",
        }
    )
    _render_table(association_summary, "methodology-association-summary")
    _render_table(
        bundle.adjusted_associations.rename(
            columns={
                "model": "Model",
                "term_label": "Term",
                "coefficient": "Koefisien",
                "std_error_hc3": "SE HC3",
                "ci_95_low": "CI 95% low",
                "ci_95_high": "CI 95% high",
                "p_value": "p-value",
            }
        ).drop(columns=["term"]),
        "methodology-association-estimates",
    )
    render_csv_download(
        bundle.adjusted_associations,
        label="Unduh estimasi asosiasi",
        filename="healthops_estimasi_asosiasi.csv",
        key="download-methodology-associations",
        active_filters="Tidak berlaku; model menggunakan full sample notebook",
        benchmark_definition="Model gabungan dan model focal-term dengan robust SE HC3",
        data_version=bundle.data_version,
    )

    st.subheader("Performa model", anchor=False)
    maturity_models = pd.DataFrame(bundle.model_metrics["maturity_model"])
    operational_models = pd.DataFrame(bundle.model_metrics["operational_model"])
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("**Expected digital maturity**")
        _render_table(maturity_models, "methodology-maturity-models")
        st.caption(
            "Expected maturity pada dashboard adalah prediksi out-of-fold; random seed "
            f"konfigurasi = {config['random_state']}."
        )
    with right:
        st.markdown("**Prediksi waktu respons rujukan**")
        _render_table(operational_models, "methodology-operational-models")
        st.caption("Metrik operasional adalah ringkasan cross-validation notebook.")

    governance = bundle.model_metrics["model_governance"]
    st.error(
        f"Validation gate tidak lolos: scenario eligible = "
        f"{governance['scenario_model_eligible']}; explainability eligible = "
        f"{governance['explainability_model_eligible']}. "
        "Prediksi, simulasi, dan feature attribution individual tidak ditampilkan.",
        icon=":material/model_training:",
    )

with quality_tab:
    render_chart(
        build_missingness_chart(quality),
        title="Missingness sumber terbatas pada tiga variabel",
        subtitle=(
            f"Audit sebelum cleaning/imputasi · {source_missing} dari {source_cells} sel sumber"
        ),
        insight=(
            "Delapan nilai hilang masing-masing terdapat pada staf IT, telemedicine, dan "
            "anggaran IT. Flag missing dipertahankan pada artefak scored."
        ),
        key="methodology-missingness",
    )
    quality_table = quality.rename(
        columns={
            "variabel": "Variabel",
            "dtype": "Tipe",
            "missing_count": "Missing",
            "missing_pct": "Missing (%)",
            "unique_count": "Nilai unik",
        }
    ).sort_values(["Missing", "Variabel"], ascending=[False, True])
    _render_table(quality_table, "methodology-quality-table")
    render_csv_download(
        quality,
        label="Unduh audit kualitas data",
        filename="healthops_audit_kualitas_data.csv",
        key="download-methodology-quality",
        active_filters="Tidak berlaku; audit mencakup data sumber lengkap",
        benchmark_definition="Audit source-level sebelum cleaning dan imputasi",
        data_version=bundle.data_version,
    )

    st.subheader("Validasi artefak runtime", anchor=False)
    validation = pd.DataFrame(
        [
            ("ID rumah sakit unik", len(hospitals), duplicate_ids, "Lolos"),
            ("Cakupan priority artifact", len(bundle.priority), 0, "Lolos"),
            ("Cakupan peer artifact", len(bundle.peers), 0, "Lolos"),
            ("Cakupan root-cause artifact", len(bundle.root_causes), 0, "Lolos"),
            (
                "Bobot prioritas berjumlah 1,0",
                3,
                abs(sum(config["priority_weights"].values()) - 1.0),
                "Lolos",
            ),
        ],
        columns=["Pemeriksaan", "Cakupan", "Pelanggaran", "Status"],
    )
    _render_table(validation, "methodology-runtime-validation")
    st.info(
        "Audit missingness merekam kondisi data sumber sebelum imputasi. Tiga kolom outcome "
        "mentah pada artefak scored memiliki satu nilai kosong setelah normalisasi anomali; "
        "kolom scoring terpisah digunakan oleh notebook agar skor tetap lengkap.",
        icon=":material/data_alert:",
    )

with limit_tab:
    st.subheader("Batas interpretasi", anchor=False)
    st.markdown(
        """
- Data bersifat **cross-sectional**; hubungan tidak dapat diinterpretasikan sebagai kausal.
- Sampel 276 rumah sakit tidak diklaim sebagai estimasi nasional atau sensus fasilitas.
- Rentang BOR dan threshold lainnya adalah **asumsi analitik/operasional** dari konfigurasi.
- LOS tidak disesuaikan terhadap case mix; BOR memerlukan konteks kapasitas dan kelas.
- Status RME dan SatuSehat bersifat biner dan tidak mengukur kualitas implementasi atau penggunaan.
- Expected maturity adalah estimasi model, bukan target resmi atau counterfactual.
- Peer kelas memperbaiki keterbandingan, tetapi tidak menghilangkan seluruh confounding.
- Skor prioritas membantu triase dan harus diikuti asesmen lapangan sebelum tindakan.
"""
    )

    st.subheader("Versi dan reproduktibilitas", anchor=False)
    version_table = pd.DataFrame(
        [
            ("Data version", bundle.data_version),
            ("Random seed analitik", str(config["random_state"])),
            ("Format artefak", "CSV dan JSON, immutable dalam repository"),
            ("Dependency lock", "uv.lock"),
            ("Validasi runtime", "schema, primary key, foreign key, row count, weight sum"),
        ],
        columns=["Item", "Nilai"],
    )
    _render_table(version_table, "methodology-versioning")
    with st.expander("Konfigurasi analitik lengkap", icon=":material/settings:"):
        st.code(json.dumps(config, indent=2, ensure_ascii=False), language="json")

    st.subheader("Artefak runtime", anchor=False)
    artifacts = pd.DataFrame(
        {
            "Artefak": [
                "hospital_features_scored.csv",
                "hospital_priority.csv",
                "peer_benchmarks.csv",
                "root_cause_scores.csv",
                "intervention_recommendations.csv",
                "executive_findings.csv",
                "outcome_association.csv",
                "adjusted_association_hc3.csv",
                "adjusted_model_summary.csv",
                "data_quality_audit.csv",
                "analysis_config.json",
                "model_metrics.json",
            ]
        }
    )
    _render_table(artifacts, "methodology-artifacts")
