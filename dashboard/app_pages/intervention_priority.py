"""Intervention priority page."""

from __future__ import annotations

import streamlit as st

from dashboard.components.charts import render_chart
from dashboard.components.charts_priority import (
    build_priority_matrix,
    build_priority_ranking,
    build_root_cause_pareto,
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
from dashboard.utils.formatting import format_decimal, format_percentage, format_score

context = get_page_context()
bundle = context.bundle
hospitals = context.hospitals
portfolio = bundle.hospitals

render_page_header(
    "Prioritas intervensi",
    "Rumah sakit mana yang perlu dinilai lebih dahulu, mengapa, dan dengan intervensi apa?",
    bundle.data_version,
)
render_filter_context(context.filter_summary, len(hospitals), len(portfolio))

if hospitals.empty:
    render_empty_state()
    st.stop()

priority_mask = hospitals["intervention_tier"].ne("Tier 3 — Monitoring")
priority_hospitals = hospitals.loc[priority_mask].copy()
priority_count = len(priority_hospitals)
priority_share = priority_count / len(hospitals) * 100
median_priority = hospitals["intervention_priority_score"].median()
if priority_hospitals.empty:
    dominant_bottleneck = "Tidak tersedia"
    highest_cohort = "Tidak tersedia"
else:
    dominant_bottleneck = priority_hospitals["root_cause_primary"].mode().iloc[0]
    class_summary = priority_hospitals["kelas_rumah_sakit"].value_counts()
    highest_cohort = f"Kelas {class_summary.index[0]} · {class_summary.iloc[0]} RS"

render_kpi_row(
    [
        KpiCard(
            "Rumah Sakit Prioritas",
            format_decimal(priority_count, 0),
            "Tier 1 dan Tier 2",
            "PRIORITAS" if priority_count else "STABIL",
            f"{priority_count} dari {len(hospitals)}",
        ),
        KpiCard(
            "Portofolio Terflag",
            format_percentage(priority_share),
            "Prioritas asesmen",
            "PERLU PERHATIAN" if priority_share else "STABIL",
            f"n={len(hospitals)}",
        ),
        KpiCard(
            "Median Skor Prioritas",
            format_score(median_priority, 3),
            "Indeks 0–1",
            "STABIL",
            f"n={len(hospitals)}",
        ),
        KpiCard(
            "Hambatan Dominan",
            dominant_bottleneck,
            "Di antara Tier 1–2",
            "PERLU PERHATIAN" if priority_count else "DATA TERBATAS",
            f"n={priority_count}",
        ),
        KpiCard(
            "Cohort Prioritas Terbesar",
            highest_cohort,
            "Menurut kelas rumah sakit",
            "PRIORITAS" if priority_count else "DATA TERBATAS",
            f"n={priority_count}",
        ),
    ],
    key="kpi-row-priority",
)

selected_hospital_id = st.session_state.get("selected_hospital_id")
render_chart(
    build_priority_matrix(hospitals, selected_hospital_id=selected_hospital_id),
    title="Tiga dimensi menentukan urutan asesmen intervensi",
    subtitle="Ukuran titik = underperformance investasi · klik titik untuk memilih rumah sakit",
    insight=(
        f"{int(hospitals['double_inefficiency'].sum())} rumah sakit memenuhi skrining "
        "inefisiensi ganda pada cohort aktif."
    ),
    key="priority-matrix",
    selectable=True,
)

left, right = st.columns([1, 1.1], gap="large")
with left:
    pareto_source = priority_hospitals if not priority_hospitals.empty else hospitals
    render_chart(
        build_root_cause_pareto(pareto_source),
        title="Bottleneck utama memusatkan kebutuhan asesmen",
        subtitle=f"Primary bottleneck pada {'Tier 1–2' if priority_count else 'cohort aktif'}",
        insight=(
            "Primary bottleneck merangkum satu penyebab; detail multi-label tetap tersedia "
            "di tabel."
        ),
        key="priority-root-cause-pareto",
    )
with right:
    render_chart(
        build_priority_ranking(hospitals),
        title="Rumah sakit dengan urutan asesmen tertinggi",
        subtitle="15 peringkat teratas pada filter aktif",
        insight=(
            "Ranking mengatur urutan asesmen dan tidak menyatakan kebutuhan intervensi absolut."
        ),
        key="priority-ranking",
        selectable=True,
    )

st.subheader("Daftar tindakan terprioritas", anchor=False)
controls = st.container(horizontal=True, vertical_alignment="bottom")
with controls:
    search = st.text_input(
        "Cari rumah sakit",
        placeholder="Nama, ID, atau provinsi",
        key="table_search_priority",
    )
    tier_filter = st.multiselect(
        "Tier",
        sorted(hospitals["intervention_tier"].dropna().unique()),
        key="priority_table_tier",
    )
    bottleneck_filter = st.multiselect(
        "Hambatan dominan",
        sorted(hospitals["root_cause_primary"].dropna().unique()),
        key="priority_table_bottleneck",
    )

action_table = hospitals.sort_values("priority_rank")
if search:
    query = search.casefold()
    action_table = action_table.loc[
        action_table[["id_rumah_sakit", "nama_rumah_sakit", "provinsi"]]
        .astype(str)
        .apply(lambda column: column.str.casefold().str.contains(query, regex=False))
        .any(axis=1)
    ]
if tier_filter:
    action_table = action_table.loc[action_table["intervention_tier"].isin(tier_filter)]
if bottleneck_filter:
    action_table = action_table.loc[action_table["root_cause_primary"].isin(bottleneck_filter)]

render_paginated_table(
    action_table,
    key="priority-action",
    column_order=[
        "priority_rank",
        "id_rumah_sakit",
        "nama_rumah_sakit",
        "provinsi",
        "kelas_rumah_sakit",
        "intervention_priority_score",
        "intervention_tier",
        "digital_deficit_score",
        "operational_burden_score",
        "investment_underperformance_score",
        "root_cause_primary",
        "root_cause_secondary",
        "recommended_intervention",
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
        "intervention_tier": "Tier",
        "digital_deficit_score": st.column_config.ProgressColumn(
            "Defisit digital", min_value=0, max_value=1, format="%.2f"
        ),
        "operational_burden_score": st.column_config.ProgressColumn(
            "Beban operasional", min_value=0, max_value=1, format="%.2f"
        ),
        "investment_underperformance_score": st.column_config.ProgressColumn(
            "Underperformance investasi", min_value=0, max_value=1, format="%.2f"
        ),
        "root_cause_primary": "Hambatan utama",
        "root_cause_secondary": "Hambatan sekunder",
        "recommended_intervention": "Intervensi",
    },
)

st.subheader("Rencana tindakan per cohort", anchor=False)
st.caption(
    "Artefak rekomendasi notebook untuk seluruh portofolio; tidak berubah oleh filter halaman."
)
st.dataframe(
    bundle.recommendations,
    hide_index=True,
    width="stretch",
    column_order=[
        "root_cause_primary",
        "jumlah_rumah_sakit",
        "recommended_intervention",
        "owner",
        "timeline",
        "kpi",
        "risiko_utama",
    ],
    column_config={
        "root_cause_primary": "Hambatan dominan",
        "jumlah_rumah_sakit": st.column_config.NumberColumn("Jumlah RS", format="%d"),
        "recommended_intervention": "Intervensi",
        "owner": "Penanggung jawab",
        "timeline": "Timeline",
        "kpi": "KPI monitoring",
        "risiko_utama": "Risiko implementasi",
    },
)

selected_id = st.session_state.get("selected_hospital_id")
if selected_id:
    selected = portfolio.loc[portfolio["id_rumah_sakit"].eq(selected_id)]
    if not selected.empty:
        row = selected.iloc[0]
        with st.container(border=True):
            st.subheader(f"{row['id_rumah_sakit']} · {row['nama_rumah_sakit']}", anchor=False)
            st.markdown(f":red-badge[{row['intervention_tier']}] **{row['root_cause_primary']}**")
            st.write(row["recommended_intervention"])
            if st.button(
                "Buka profil lengkap",
                icon=":material/open_in_new:",
                type="primary",
            ):
                st.switch_page("app_pages/hospital_explorer.py")

weights = bundle.analysis_config["priority_weights"]
render_method_note(
    "Formula dan batas interpretasi",
    (
        f"Skor Prioritas = {weights['digital_deficit']:.0%} Defisit Digital + "
        f"{weights['operational_burden']:.0%} Beban Operasional + "
        f"{weights['investment_underperformance']:.0%} Underperformance Investasi. "
        "Seluruh komponen berasal dari notebook. Skor ini hanya mengurutkan asesmen dan bukan "
        "probabilitas risiko klinis. Root cause bersifat multi-label; primary bottleneck adalah "
        "ringkasan untuk tampilan portofolio."
    ),
)
