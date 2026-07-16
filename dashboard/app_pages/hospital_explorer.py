"""Hospital explorer page."""

from __future__ import annotations

import streamlit as st

from dashboard.components.charts import render_chart
from dashboard.components.charts_hospital import (
    build_burden_decomposition,
    build_peer_benchmark_profile,
    build_priority_decomposition,
)
from dashboard.components.common import (
    KpiCard,
    render_filter_context,
    render_kpi_row,
    render_method_note,
    render_page_header,
)
from dashboard.components.tables import render_paginated_table
from dashboard.context import get_page_context
from dashboard.state import set_selected_hospital
from dashboard.utils.export import render_csv_download
from dashboard.utils.formatting import (
    format_minutes,
    format_score,
    format_signed,
)

context = get_page_context()
bundle = context.bundle
portfolio = bundle.hospitals

render_page_header(
    "Eksplorasi rumah sakit",
    "Bagaimana posisi rumah sakit ini dibandingkan dengan rumah sakit sekelas?",
    bundle.data_version,
)
render_filter_context(context.filter_summary, len(context.hospitals), len(portfolio))

ordered = portfolio.sort_values(["nama_rumah_sakit", "id_rumah_sakit"])
name_by_id = ordered.set_index("id_rumah_sakit")["nama_rumah_sakit"].to_dict()
default_id = st.session_state.get("selected_hospital_id") or str(
    bundle.priority.iloc[0]["id_rumah_sakit"]
)
options = ordered["id_rumah_sakit"].tolist()
default_index = options.index(default_id) if default_id in options else 0
selected_id = st.selectbox(
    "Pilih rumah sakit",
    options,
    index=default_index,
    format_func=lambda hospital_id: f"{hospital_id} · {name_by_id[hospital_id]}",
    key="explorer_hospital",
)
selected = portfolio.loc[portfolio["id_rumah_sakit"].eq(selected_id)].iloc[0]
set_selected_hospital(str(selected_id), str(selected["nama_rumah_sakit"]))

with st.container(border=True, key="hospital-profile-header"):
    st.subheader(f"{selected['nama_rumah_sakit']} · {selected['id_rumah_sakit']}", anchor=False)
    st.markdown(
        f":blue-badge[Kelas {selected['kelas_rumah_sakit']}] "
        f":gray-badge[{selected['kepemilikan']}] "
        f":violet-badge[{selected['provinsi']}] "
        f":red-badge[{selected['intervention_tier']}]"
    )
    st.caption(
        f"{selected['kota_kabupaten']} · {int(selected['jumlah_tempat_tidur'])} tempat tidur · "
        f"{int(selected['jumlah_jenis_layanan'])} jenis layanan · "
        f"RME: {selected['status_implementasi_rme']} · "
        f"SatuSehat: {selected['status_terhubung_satusehat']}"
    )

peer_group = portfolio.loc[portfolio["kelas_rumah_sakit"].eq(selected["kelas_rumah_sakit"])].copy()
peer_median_maturity = peer_group["skor_kematangan_digital"].median()
peer_median_referral = peer_group["rata_rata_waktu_respons_rujukan_menit"].median()
referral_delta = selected["rata_rata_waktu_respons_rujukan_menit"] - peer_median_referral

render_kpi_row(
    [
        KpiCard(
            "Kematangan Digital",
            format_score(selected["skor_kematangan_digital"]),
            f"{format_signed(selected['skor_kematangan_digital'] - peer_median_maturity)} vs kelas",
            "STABIL"
            if selected["skor_kematangan_digital"] >= peer_median_maturity
            else "PERLU PERHATIAN",
            f"Peer: {len(peer_group)} rumah sakit Kelas {selected['kelas_rumah_sakit']}",
        ),
        KpiCard(
            "Kesenjangan Konversi Digital",
            format_signed(selected["digital_conversion_gap"]),
            str(selected["investment_conversion_segment"]),
            "PERLU PERHATIAN" if selected["digital_conversion_gap"] < 0 else "STABIL",
            "Aktual − ekspektasi OOF",
        ),
        KpiCard(
            "Waktu Respons Rujukan",
            format_minutes(selected["rata_rata_waktu_respons_rujukan_menit"]),
            f"{format_signed(referral_delta, suffix=' menit')} vs kelas",
            "STABIL"
            if selected["rata_rata_waktu_respons_rujukan_menit"] <= peer_median_referral
            else "PERLU PERHATIAN",
            f"Median kelas: {format_minutes(peer_median_referral)}",
        ),
        KpiCard(
            "Beban Operasional",
            format_score(selected["operational_burden_score"], 3),
            "Persentil gabungan dalam kelas",
            "PRIORITAS" if selected["operational_burden_score"] >= 0.75 else "STABIL",
            "Respons, BOR, LOS, dan beban kerja",
        ),
        KpiCard(
            "Skor Prioritas",
            format_score(selected["intervention_priority_score"], 3),
            f"Peringkat {int(selected['priority_rank'])} dari {len(portfolio)}",
            "PRIORITAS" if selected["intervention_tier"].startswith("Tier 1") else "STABIL",
            str(selected["intervention_tier"]),
        ),
    ],
    key="kpi-row-hospital",
)

render_chart(
    build_peer_benchmark_profile(selected, peer_group, portfolio),
    title="Profil rumah sakit terhadap distribusi kelasnya",
    subtitle=(
        f"Peer tetap = seluruh rumah sakit Kelas {selected['kelas_rumah_sakit']} · "
        "garis tebal = IQR kelas"
    ),
    insight=(
        "Persentil hanya menyetarakan posisi visual antar-unit. Hover menampilkan nilai aktual, "
        "IQR kelas, median kelas, dan median nasional."
    ),
    key="hospital-peer-profile",
)

left, right = st.columns(2, gap="large")
with left:
    render_chart(
        build_burden_decomposition(selected),
        title="Komponen pembentuk beban operasional",
        subtitle="Semakin tinggi persentil, semakin berat posisi relatif dalam kelas",
        insight=(
            f"Beban operasional gabungan rumah sakit ini adalah "
            f"{selected['operational_burden_score']:.3f}."
        ),
        key="hospital-burden-decomposition",
    )
with right:
    render_chart(
        build_priority_decomposition(selected, bundle.analysis_config["priority_weights"]),
        title="Kontribusi pembentuk Skor Prioritas",
        subtitle="Skor komponen dikalikan bobot konfigurasi notebook",
        insight=(
            f"Total kontribusi menghasilkan Skor Prioritas "
            f"{selected['intervention_priority_score']:.3f}."
        ),
        key="hospital-priority-decomposition",
    )

root_detail = bundle.root_causes.loc[bundle.root_causes["id_rumah_sakit"].eq(selected_id)].iloc[0]
recommendation = bundle.recommendations.loc[
    bundle.recommendations["root_cause_primary"].eq(selected["root_cause_primary"])
]

with st.container(border=True):
    st.subheader("Hambatan dan rekomendasi", anchor=False)
    st.markdown(f"**Hambatan utama:** {selected['root_cause_primary']}")
    st.caption(
        f"Multi-label: {root_detail['root_cause_multilabel']} · "
        f"kekuatan {root_detail['root_cause_strength']:.2f}"
    )
    st.markdown(f"**Tindakan:** {selected['recommended_intervention']}")
    if not recommendation.empty:
        rec = recommendation.iloc[0]
        st.markdown(
            f"**Penanggung jawab:** {rec['owner']}  \n"
            f"**Timeline:** {rec['timeline']}  \n"
            f"**KPI monitoring:** {rec['kpi']}  \n"
            f"**Risiko implementasi:** {rec['risiko_utama']}"
        )

st.subheader("Rumah sakit pembanding", anchor=False)
st.caption(
    f"Peer table mengikuti definisi notebook: seluruh Kelas {selected['kelas_rumah_sakit']}, "
    "bukan subset filter aktif."
)
peer_table = peer_group.sort_values("intervention_priority_score", ascending=False)
render_paginated_table(
    peer_table,
    key="hospital-peers",
    column_order=[
        "id_rumah_sakit",
        "nama_rumah_sakit",
        "provinsi",
        "skor_kematangan_digital",
        "expected_digital_maturity_oof",
        "digital_conversion_gap",
        "staf_it_per_100_bed",
        "tingkat_keterisian_tempat_tidur_persen",
        "rata_rata_lama_rawat_hari",
        "rata_rata_waktu_respons_rujukan_menit",
        "operational_burden_score",
        "intervention_priority_score",
    ],
    column_config={
        "id_rumah_sakit": st.column_config.TextColumn("ID", pinned=True),
        "nama_rumah_sakit": st.column_config.TextColumn("Rumah sakit", pinned=True),
        "provinsi": "Provinsi",
        "skor_kematangan_digital": st.column_config.NumberColumn("Kematangan", format="%.1f"),
        "expected_digital_maturity_oof": st.column_config.NumberColumn("Ekspektasi", format="%.1f"),
        "digital_conversion_gap": st.column_config.NumberColumn("Gap", format="%+.1f"),
        "staf_it_per_100_bed": st.column_config.NumberColumn("Staf IT/100 bed", format="%.2f"),
        "tingkat_keterisian_tempat_tidur_persen": st.column_config.NumberColumn(
            "BOR", format="%.1f%%"
        ),
        "rata_rata_lama_rawat_hari": st.column_config.NumberColumn("LOS", format="%.1f"),
        "rata_rata_waktu_respons_rujukan_menit": st.column_config.NumberColumn(
            "Respons", format="%.1f"
        ),
        "operational_burden_score": st.column_config.ProgressColumn(
            "Beban", min_value=0, max_value=1, format="%.2f"
        ),
        "intervention_priority_score": st.column_config.ProgressColumn(
            "Prioritas", min_value=0, max_value=1, format="%.3f"
        ),
    },
)
render_csv_download(
    peer_table,
    label="Unduh cohort pembanding",
    filename=f"healthops_peer_{selected_id}.csv",
    key="download-hospital-peers",
    active_filters=f"Rumah sakit terpilih={selected_id}; filter global tidak diterapkan pada peer",
    benchmark_definition=(
        f"Seluruh rumah sakit Kelas {selected['kelas_rumah_sakit']} (n={len(peer_group)})"
    ),
    data_version=bundle.data_version,
)

render_method_note(
    "Definisi peer dan batas interpretasi",
    """
Peer ditetapkan oleh notebook sebagai seluruh rumah sakit dengan kelas yang sama dan tidak berubah
oleh filter dashboard. Q1, median, Q3, dan persentil dihitung secara deskriptif dari cohort kelas
penuh; median diverifikasi terhadap artefak `peer_benchmarks.csv`. Nilai peer adalah pembanding,
bukan target resmi. Data bersifat cross-sectional dan tidak mendukung kesimpulan sebab-akibat.
""",
)
