# Technology Stack Specification

## 1. Tujuan Dokumen

Dokumen ini menetapkan stack teknologi final untuk dashboard SYNAPSE Smart Hospital.

Dokumen ini bukan daftar alternatif teknologi. Seluruh keputusan utama sudah ditetapkan berdasarkan karakteristik proyek:

* dataset terdiri dari 276 rumah sakit;
* dataset utama memiliki 20 variabel;
* data bersifat cross-sectional;
* tidak terdapat data transaksi atau time series;
* tidak terdapat data pasien individual;
* seluruh analisis berat sudah dijalankan pada notebook;
* notebook sudah menghasilkan artefak siap konsumsi untuk dashboard;
* dashboard digunakan untuk kompetisi dan demonstrasi analitik;
* aplikasi dibangun dengan Streamlit;
* dashboard tidak memerlukan backend, database, API, atau model serving.

Arsitektur final:

```text
Notebook analitik
        ↓
Artefak CSV dan JSON terkomputasi
        ↓
Streamlit data loader
        ↓
Filter dan agregasi ringan
        ↓
Komponen KPI, chart, tabel, dan hospital drill-down
```

Dashboard harus berfungsi sebagai presentation dan decision-support layer.

Dashboard tidak boleh menjadi pipeline analitik kedua.

---

# 2. Keputusan Stack Final

| Layer                     | Teknologi Final           | Fungsi                                  |
| ------------------------- | ------------------------- | --------------------------------------- |
| Bahasa                    | Python                    | Seluruh aplikasi                        |
| Dashboard framework       | Streamlit                 | UI, navigasi, filter, state, dan export |
| Dataframe processing      | pandas                    | Loading, filtering, aggregation         |
| Numerical utilities       | NumPy                     | Safe calculation dan formatting numerik |
| Interactive visualization | Plotly                    | Seluruh chart interaktif                |
| Runtime data storage      | CSV dan JSON              | Membaca artefak notebook                |
| Application state         | `st.session_state`        | Filter dan rumah sakit terpilih         |
| Caching                   | `st.cache_data`           | Cache file dan agregasi                 |
| Table rendering           | Native `st.dataframe`     | Ranking dan detail table                |
| Testing                   | pytest                    | Data contract dan utility tests         |
| Code quality              | Ruff                      | Formatting dan linting                  |
| Dependency management     | uv                        | Environment, dependency, dan lockfile   |
| Deployment                | Streamlit Community Cloud | Deployment final kompetisi              |
| Version control           | Git dan GitHub            | Kolaborasi dan deployment               |

---

# 3. Teknologi yang Tidak Digunakan

Jangan menambahkan teknologi berikut:

* PostgreSQL;
* SQLite;
* DuckDB;
* Redis;
* FastAPI;
* Flask;
* Django;
* React;
* Next.js;
* Node.js;
* Docker;
* Kubernetes;
* Airflow;
* Spark;
* Polars;
* PyArrow;
* Parquet;
* Pandera;
* Pydantic;
* AgGrid;
* statsmodels pada runtime;
* scikit-learn pada runtime;
* SciPy pada runtime;
* SHAP pada runtime;
* joblib model loading pada runtime;
* authentication system;
* external API;
* geospatial server;
* map tile provider.

Alasannya sederhana:

1. Dataset hanya berisi 276 baris.
2. Seluruh data dapat dimuat langsung ke memori.
3. Analisis telah diselesaikan dan diekspor oleh notebook.
4. Dashboard tidak membutuhkan write operation.
5. Tidak terdapat pengguna dengan role berbeda.
6. Tidak terdapat data real-time.
7. Tidak terdapat query kompleks yang membutuhkan database.
8. Tidak terdapat koordinat geografis.
9. Penambahan teknologi tersebut meningkatkan kompleksitas tanpa menambah nilai analitik.

---

# 4. Dataset Source of Truth

## 4.1 Raw Dataset

File raw:

```text
dataset_smart_hospital_indonesia.csv
```

atau nama file sumber aktual yang digunakan notebook.

Dataset memiliki 276 baris dan 20 kolom.

Kolom raw resmi:

```python
RAW_COLUMNS = [
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
    "kunjungan_telemedicine_per_bulan",
    "jumlah_perangkat_iot",
    "jumlah_staf_it",
    "anggaran_it_tahunan_juta_rupiah",
    "rata_rata_waktu_respons_rujukan_menit",
]
```

Dashboard tidak perlu membaca raw dataset pada runtime normal.

Raw dataset hanya digunakan oleh notebook analitik.

---

## 4.2 Primary Dashboard Dataset

File utama dashboard:

```text
synapse_artifacts/hospital_features_scored.csv
```

File ini menjadi source of truth untuk:

* seluruh informasi rumah sakit;
* raw operational metrics;
* raw digital metrics;
* normalized resource metrics;
* digital conversion metrics;
* operational burden metrics;
* double-inefficiency status;
* priority score;
* priority rank;
* root-cause fields;
* segmentation fields.

Semua halaman dashboard membaca file ini melalui satu shared loader.

Jangan membuat ulang feature engineering dari raw CSV di dalam Streamlit.

---

# 5. Artefak Notebook yang Digunakan

## 5.1 Required Runtime Files

Dashboard menggunakan file berikut:

```text
synapse_artifacts/
├── hospital_features_scored.csv
├── hospital_priority.csv
├── peer_benchmarks.csv
├── root_cause_scores.csv
├── intervention_recommendations.csv
├── executive_findings.csv
├── outcome_association.csv
├── data_quality_audit.csv
├── analysis_config.json
└── model_metrics.json
```

---

## 5.2 Peran Setiap Artefak

### `hospital_features_scored.csv`

Digunakan oleh:

* Ringkasan Eksekutif;
* Kesiapan Digital dan Investasi;
* Dampak Operasional;
* Priority Matrix;
* Hospital Explorer;
* seluruh global filter.

File ini adalah tabel utama pada level rumah sakit.

---

### `hospital_priority.csv`

Digunakan oleh:

* priority watchlist;
* priority ranking;
* prioritized action table;
* priority tier summary;
* selected hospital priority context.

Dashboard tidak menghitung ulang ranking prioritas.

---

### `peer_benchmarks.csv`

Digunakan oleh:

* Hospital Explorer;
* actual versus peer comparison;
* bullet comparison;
* peer median;
* gap versus peer.

Peer benchmark tidak dihitung ulang berdasarkan filter dashboard.

Peer definition harus mengikuti definisi yang digunakan notebook.

---

### `root_cause_scores.csv`

Digunakan oleh:

* root-cause Pareto;
* primary bottleneck;
* secondary bottleneck;
* root-cause score decomposition;
* multi-label bottleneck display.

Dashboard harus mempertahankan sifat multi-label root cause.

`root_cause_primary` digunakan untuk ringkasan.

`root_cause_secondary` dan `root_cause_multilabel` digunakan untuk drill-down.

---

### `intervention_recommendations.csv`

Digunakan oleh:

* cohort action plan;
* recommended intervention;
* responsible owner;
* implementation timeline;
* monitoring KPI;
* implementation risk.

Dashboard tidak membuat rekomendasi baru menggunakan rules terpisah.

Gunakan hasil final notebook.

---

### `executive_findings.csv`

Digunakan oleh:

* dynamic findings pada executive summary;
* evidence summary;
* decision statement.

Temuan harus dibaca dari artefak ini, bukan ditulis ulang secara hardcoded pada page file.

---

### `outcome_association.csv`

Digunakan oleh:

* adjusted association coefficient plot;
* estimate;
* confidence interval;
* p-value;
* model label;
* sample size.

Dashboard tidak menjalankan regresi.

---

### `data_quality_audit.csv`

Digunakan oleh:

* halaman Metodologi dan Kualitas Data;
* missing-value table;
* anomaly summary;
* data-quality callout.

---

### `analysis_config.json`

Digunakan untuk menampilkan:

* rentang referensi BOR;
* quantile inefisiensi ganda;
* priority weights;
* root-cause threshold;
* model governance threshold;
* random state.

Dashboard tidak memiliki salinan configuration value yang berbeda.

---

### `model_metrics.json`

Digunakan untuk menampilkan:

* model performance;
* validation gate;
* model status;
* explanatory limitation.

Dashboard tidak membaca model `.joblib`.

---

## 5.3 Artefak yang Tidak Dimuat Dashboard

File berikut tetap disimpan sebagai bukti analitik, tetapi tidak perlu dimuat pada setiap runtime:

```text
hospital_clean.csv
maturity_model_metrics.csv
operational_model_metrics.csv
model_global_importance.csv
scenario_results.csv
threshold_sensitivity.csv
priority_rank_stability.csv
priority_rank_spearman.csv
priority_topk_stability.csv
outlier_sensitivity.csv
imputation_sensitivity.csv
geographic_overrepresentation.csv
```

File tersebut hanya dibaca pada halaman Metodologi apabila visual atau tabel terkait benar-benar digunakan.

---

## 5.4 Model Files

Notebook menghasilkan:

```text
models/digital_maturity_model.joblib
models/referral_response_model.joblib
```

Dashboard tidak memuat kedua file tersebut.

Model hanya merupakan artefak reproducibility.

Semua prediction dan model output yang dibutuhkan dashboard sudah tersedia dalam CSV atau JSON.

---

# 6. Runtime Architecture

## 6.1 Runtime Flow

```text
Streamlit start
    ↓
Validate required artifact files
    ↓
Load CSV and JSON files once
    ↓
Cache loaded data
    ↓
Initialize session state
    ↓
Apply global filters
    ↓
Calculate lightweight summaries
    ↓
Render pages
```

Tidak terdapat:

* model fitting;
* cross-validation;
* imputation pipeline;
* feature engineering pipeline;
* SHAP calculation;
* statistical testing;
* bootstrap;
* scenario simulation.

---

## 6.2 Runtime Responsibilities

Runtime hanya bertanggung jawab terhadap:

* filtering;
* groupby;
* median;
* count;
* percentage;
* sorting;
* row selection;
* chart construction;
* table construction;
* formatting;
* CSV export;
* navigation;
* session state.

---

# 7. Application Framework

## 7.1 Streamlit

Streamlit merupakan satu-satunya application framework.

Gunakan Streamlit untuk:

* multipage navigation;
* sidebar;
* global filters;
* KPI cards;
* tabs;
* expanders;
* chart rendering;
* table rendering;
* download button;
* selected hospital state;
* active filter summary;
* methodology content.

---

## 7.2 Navigation

Gunakan satu entry point:

```text
dashboard/app.py
```

Gunakan navigation configuration terpusat.

Halaman:

```text
01 Ringkasan Eksekutif
02 Kesiapan Digital & Investasi
03 Dampak terhadap Operasional
04 Prioritas Intervensi
05 Eksplorasi Rumah Sakit
06 Metodologi & Kualitas Data
```

Jangan menggunakan sistem navigasi ganda.

---

## 7.3 Page Configuration

Konfigurasi dilakukan satu kali:

```python
import streamlit as st

st.set_page_config(
    page_title="SYNAPSE HealthOps",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

---

# 8. Session State

Gunakan `st.session_state` hanya untuk state antarmuka.

```python
SESSION_DEFAULTS = {
    "selected_hospital_id": None,
    "selected_hospital_name": None,
    "filter_provinsi": [],
    "filter_kelas": [],
    "filter_kepemilikan": [],
    "filter_rme": [],
    "filter_satusehat": [],
    "priority_only": False,
}
```

Tidak perlu menyimpan:

* seluruh DataFrame;
* hasil model;
* model object;
* chart object;
* export bytes permanen;
* cache manual.

DataFrame tersedia melalui cached loader.

---

# 9. Data Loading

## 9.1 Shared Loader

Semua file dibaca dari satu module:

```text
dashboard/data_loader.py
```

Contoh interface:

```python
from pathlib import Path

import pandas as pd
import streamlit as st


ARTIFACT_DIR = Path("synapse_artifacts")


@st.cache_data(show_spinner=False)
def load_hospital_features() -> pd.DataFrame:
    return pd.read_csv(
        ARTIFACT_DIR / "hospital_features_scored.csv"
    )


@st.cache_data(show_spinner=False)
def load_priority_table() -> pd.DataFrame:
    return pd.read_csv(
        ARTIFACT_DIR / "hospital_priority.csv"
    )


@st.cache_data(show_spinner=False)
def load_peer_benchmarks() -> pd.DataFrame:
    return pd.read_csv(
        ARTIFACT_DIR / "peer_benchmarks.csv"
    )
```

Jangan membaca file yang sama secara langsung dari setiap halaman.

---

## 9.2 JSON Loading

```python
import json


@st.cache_data(show_spinner=False)
def load_json_artifact(filename: str) -> dict:
    with (ARTIFACT_DIR / filename).open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)
```

---

## 9.3 Data Contract Validation

Tidak perlu Pandera.

Gunakan validasi eksplisit sederhana.

```python
REQUIRED_HOSPITAL_COLUMNS = {
    "id_rumah_sakit",
    "nama_rumah_sakit",
    "provinsi",
    "kota_kabupaten",
    "kelas_rumah_sakit",
    "kepemilikan",
    "skor_kematangan_digital",
    "tingkat_keterisian_tempat_tidur_persen",
    "rata_rata_lama_rawat_hari",
    "rata_rata_waktu_respons_rujukan_menit",
}
```

```python
def validate_columns(
    dataframe: pd.DataFrame,
    required_columns: set[str],
    artifact_name: str,
) -> None:
    missing_columns = required_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"{artifact_name} tidak memiliki kolom wajib: "
            f"{sorted(missing_columns)}"
        )
```

Validasi minimum:

* file tersedia;
* required columns tersedia;
* `id_rumah_sakit` unik;
* tabel tidak kosong;
* jumlah rumah sakit sesuai ekspektasi;
* join key tidak memiliki duplikasi tidak terduga.

---

# 10. Data Processing

## 10.1 pandas

Gunakan pandas untuk seluruh data operation.

Operasi utama:

```python
filtered_df = hospital_df.loc[mask].copy()

median_maturity = filtered_df[
    "skor_kematangan_digital"
].median()

satusehat_rate = filtered_df[
    "status_terhubung_satusehat"
].eq("Terhubung").mean()

priority_count = filtered_df[
    "double_inefficiency"
].sum()
```

Dataset kecil sehingga tidak memerlukan optimasi engine tambahan.

---

## 10.2 NumPy

Gunakan NumPy hanya untuk:

* `np.where`;
* missing-value handling;
* safe numeric operations;
* clipping jika dibutuhkan untuk visual;
* finite-value validation.

Jangan menggunakan NumPy untuk membangun ulang model statistik.

---

## 10.3 No Runtime Feature Engineering

Metric berikut berasal dari `hospital_features_scored.csv`:

* anggaran IT per tempat tidur;
* staf IT per 100 tempat tidur;
* IoT per 100 tempat tidur;
* kunjungan per tempat tidur;
* kunjungan per tenaga kerja;
* telemedicine intensity;
* investment intensity;
* expected maturity;
* conversion gap;
* digital deficit;
* operational burden;
* investment underperformance;
* priority score;
* double-inefficiency flag;
* root-cause scores.

Jangan menghitung ulang metric tersebut pada dashboard.

---

# 11. Visualization

## 11.1 Plotly Only

Seluruh chart interaktif menggunakan Plotly.

```python
import plotly.express as px
import plotly.graph_objects as go
```

Jangan menggunakan:

* Matplotlib;
* Seaborn;
* Altair;
* Bokeh;
* PyDeck;
* Folium.

Matplotlib tetap berada pada notebook untuk analisis dan static figures.

---

## 11.2 Chart Builder Pattern

Chart logic berada pada:

```text
dashboard/components/charts/
```

Contoh:

```python
def build_priority_matrix(
    dataframe: pd.DataFrame,
    selected_hospital_id: str | None,
) -> go.Figure:
    ...
```

Page file tidak boleh berisi konfigurasi Plotly panjang.

---

## 11.3 Required Charts

Implementasikan:

* digital maturity versus operational burden quadrant;
* maturity distribution by class;
* maturity distribution by ownership;
* actual versus expected maturity;
* investment conversion matrix;
* coefficient plot;
* maturity versus referral response;
* operational profile heatmap;
* root-cause Pareto;
* priority ranking;
* hospital benchmark bullet rows;
* priority score decomposition.

---

## 11.4 No Geographic Map

Dataset memiliki:

* provinsi;
* kota atau kabupaten.

Dataset tidak memiliki:

* latitude;
* longitude;
* geometry;
* administrative shapefile.

Jangan menambahkan map dependency.

Gunakan:

* province ranking;
* province heatmap;
* province summary table;
* horizontal dot plot.

Geographic insight tidak harus diwujudkan sebagai peta.

---

## 11.5 Shared Plotly Theme

Gunakan satu helper:

```python
def apply_chart_theme(
    figure: go.Figure,
) -> go.Figure:
    figure.update_layout(
        template="plotly_white",
        margin={
            "l": 24,
            "r": 24,
            "t": 56,
            "b": 24,
        },
        font={
            "family": "Inter, Arial, sans-serif",
            "size": 13,
        },
        hoverlabel={
            "font_size": 12,
        },
        legend={
            "title": None,
        },
    )

    return figure
```

Color tokens harus mengikuti `SYNAPSE_HealthOps_Design_System.md`.

Jangan mendefinisikan warna berbeda pada setiap halaman.

---

# 12. Tables

## 12.1 Native Streamlit Dataframe

Gunakan:

```python
st.dataframe()
```

untuk seluruh tabel.

Tidak menggunakan AgGrid.

Native table sudah mencukupi untuk:

* 276 rumah sakit;
* sorting;
* scrolling;
* column formatting;
* compact ranking;
* selectable rows sesuai kemampuan Streamlit yang digunakan.

---

## 12.2 Main Tables

Tabel utama:

* top priority watchlist;
* hospital priority ranking;
* investment underperformance table;
* root-cause table;
* recommendation table;
* peer comparison table;
* data-quality table.

Batasi jumlah kolom default.

Detail tambahan ditampilkan melalui:

* expander;
* selected-hospital panel;
* CSV export.

---

# 13. Styling

## 13.1 Streamlit Theme

Gunakan:

```text
.streamlit/config.toml
```

Theme mengikuti design system final.

Contoh struktur:

```toml
[theme]
base = "light"
primaryColor = "#2563EB"
backgroundColor = "#F8FAFC"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#0F172A"
font = "sans serif"
```

Nilai warna harus disamakan dengan design-system file yang telah dibuat.

---

## 13.2 Custom CSS

Custom CSS hanya digunakan untuk:

* KPI cards;
* status badges;
* active-filter chips;
* page spacing;
* selected hospital header;
* recommendation card;
* methodology callout.

Simpan pada:

```text
dashboard/styles/main.css
```

Jangan menggunakan JavaScript injection.

Jangan menggunakan custom Streamlit component.

---

# 14. Project Structure

```text
ssdc/
├── dashboard/
│   ├── app.py
│   ├── data_loader.py
│   ├── state.py
│   ├── filters.py
│   ├── pages/
│   │   ├── executive_summary.py
│   │   ├── digital_investment.py
│   │   ├── operational_impact.py
│   │   ├── intervention_priority.py
│   │   ├── hospital_explorer.py
│   │   └── methodology.py
│   ├── components/
│   │   ├── kpi_card.py
│   │   ├── active_filters.py
│   │   ├── status_badge.py
│   │   ├── recommendation_card.py
│   │   ├── hospital_header.py
│   │   ├── tables.py
│   │   └── charts/
│   │       ├── executive.py
│   │       ├── digital.py
│   │       ├── operational.py
│   │       ├── priority.py
│   │       └── hospital.py
│   ├── utils/
│   │   ├── formatting.py
│   │   ├── validation.py
│   │   ├── export.py
│   │   └── terminology.py
│   └── styles/
│       └── main.css
├── synapse_artifacts/
│   ├── hospital_features_scored.csv
│   ├── hospital_priority.csv
│   ├── peer_benchmarks.csv
│   ├── root_cause_scores.csv
│   ├── intervention_recommendations.csv
│   ├── executive_findings.csv
│   ├── outcome_association.csv
│   ├── data_quality_audit.csv
│   ├── analysis_config.json
│   └── model_metrics.json
├── notebooks/
│   └── SYNAPSE_2026_Smart_Hospital_Analysis.ipynb
├── tests/
│   ├── test_data_contract.py
│   ├── test_data_loader.py
│   ├── test_filters.py
│   ├── test_formatting.py
│   └── test_joins.py
├── .streamlit/
│   └── config.toml
├── pyproject.toml
├── uv.lock
├── dashboard_structure.md
├── techstack.md
└── README.md
```

Gunakan struktur repository aktual sebagai dasar.

Jangan memindahkan folder milik data engineer apabila path yang ada sudah menjadi kontrak antaranggota tim.

Dashboard harus mengonsumsi artefak dari folder output yang telah disepakati.

---

# 15. Dependency Specification

## 15.1 Runtime Dependencies

Dependency runtime dideklarasikan pada `pyproject.toml`:

```toml
[project]
name = "synapse-smart-hospital"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "streamlit",
    "pandas",
    "numpy",
    "plotly",
]

[tool.uv]
package = false
default-groups = []
```

Tidak ada dependency machine learning pada runtime.

---

## 15.2 Development Dependencies

Dependency development ditempatkan pada group `dev`:

```toml
[dependency-groups]
dev = [
    "pytest",
    "ruff",
]
```

Tambahkan dependency melalui uv agar `pyproject.toml` dan `uv.lock` diperbarui bersama:

```bash
uv add streamlit pandas numpy plotly
uv add --group dev pytest ruff
uv add --group analysis matplotlib scipy scikit-learn joblib jupyter
```

Jika notebook dijalankan pada project yang sama, dependency notebook disimpan pada group `analysis`:

```toml
[dependency-groups]
dev = [
    "pytest",
    "ruff",
]
analysis = [
    "matplotlib",
    "scipy",
    "scikit-learn",
    "joblib",
    "jupyter",
]
```

Pisahkan dependency dashboard dan dependency analisis.

`pandas` dan `numpy` tidak perlu diulang pada group `analysis` karena sudah menjadi dependency runtime project.

Streamlit deployment hanya menggunakan dependency runtime project.

---

## 15.3 Dependency Management

Gunakan:

```text
uv
pyproject.toml
uv.lock
```

`pyproject.toml` menjadi source of truth deklarasi dependency.

`uv.lock` wajib di-commit untuk memastikan hasil instalasi reproducible pada local development, CI, dan deployment.

Gunakan workflow berikut:

```bash
uv lock
uv sync --frozen
uv run streamlit run dashboard/app.py
uv run --group dev pytest
uv run --group dev ruff check .
uv run --group dev ruff format --check .
```

Untuk menjalankan notebook:

```bash
uv run --group analysis jupyter lab
```

Jangan menambahkan atau mempertahankan:

* `requirements.txt`;
* `requirements-analysis.txt`;
* Poetry;
* Conda;
* Pipenv;
* lockfile dependency selain `uv.lock`;
* instalasi dependency langsung menggunakan `pip`.

Gunakan group hanya untuk memisahkan dependency `dev` dan `analysis` dari dependency runtime.

Tetapkan version constraint setelah aplikasi stabil, lalu perbarui dan verifikasi `uv.lock` sebelum deployment final.

---

# 16. Offline Analysis Boundary

## 16.1 Notebook Responsibilities

Notebook bertanggung jawab terhadap:

* data cleaning;
* anomaly audit;
* feature engineering;
* statistical testing;
* group comparison;
* effect size;
* OOF prediction;
* expected maturity;
* adjusted operational model;
* model validation;
* model explainability;
* double-inefficiency definition;
* sensitivity analysis;
* root-cause scoring;
* recommendation mapping;
* export artefak.

---

## 16.2 Dashboard Responsibilities

Dashboard bertanggung jawab terhadap:

* presenting results;
* filtering;
* comparing cohorts;
* exploring hospitals;
* displaying methodology;
* exporting filtered rows.

Batas ini harus dipertahankan.

---

# 17. Caching

## 17.1 Required Caching

Gunakan `st.cache_data` pada semua data loader.

```python
@st.cache_data(show_spinner=False)
def load_csv_artifact(
    filename: str,
) -> pd.DataFrame:
    return pd.read_csv(
        ARTIFACT_DIR / filename
    )
```

Dataset sangat kecil sehingga tidak perlu:

* cache backend;
* Redis;
* manual serialization;
* incremental cache;
* resource cache.

---

## 17.2 Cache Scope

Cache:

* source CSV;
* source JSON;
* merged hospital detail table;
* export preparation jika diperlukan.

Jangan cache setiap chart.

Chart dibangun dari filtered DataFrame yang kecil.

---

# 18. Join Strategy

Gunakan:

```text
id_rumah_sakit
```

sebagai primary key untuk seluruh join level rumah sakit.

Contoh:

```python
hospital_detail = (
    hospital_features
    .merge(
        priority_table,
        on="id_rumah_sakit",
        how="left",
        validate="one_to_one",
        suffixes=("", "_priority"),
    )
    .merge(
        peer_benchmarks,
        on="id_rumah_sakit",
        how="left",
        validate="one_to_one",
        suffixes=("", "_peer"),
    )
)
```

Gunakan `validate="one_to_one"` untuk mendeteksi duplicate key.

Jangan join menggunakan:

* nama rumah sakit;
* kombinasi provinsi dan nama;
* row index.

---

# 19. Filtering Strategy

Filter global:

* `provinsi`;
* `kelas_rumah_sakit`;
* `kepemilikan`;
* `status_implementasi_rme`;
* `status_terhubung_satusehat`.

Selected hospital:

* `id_rumah_sakit`.

Filter diterapkan pada primary hospital table.

Tabel rekomendasi cohort tidak harus berubah jika artefaknya bersifat global. Jika ditampilkan bersama filter, labeli dengan jelas apakah rekomendasi tersebut:

* seluruh portofolio;
* atau subset aktif.

Tidak ada filter:

* tanggal;
* bulan;
* tahun;
* historical period;
* model version;
* scenario version.

---

# 20. Export

Dashboard hanya menyediakan CSV export.

Gunakan:

```python
csv_data = dataframe.to_csv(
    index=False,
).encode("utf-8-sig")
```

Export:

* filtered hospital portfolio;
* priority table;
* selected peer comparison;
* recommendation table.

Tidak perlu:

* Excel export;
* PDF generation;
* image export;
* scheduled report;
* email delivery.

---

# 21. Testing

## 21.1 Required Tests

Test hanya difokuskan pada failure yang dapat merusak dashboard.

### Data Contract Test

Pastikan:

* seluruh artefak wajib tersedia;
* primary dataset tidak kosong;
* seluruh kolom wajib tersedia;
* `id_rumah_sakit` unik;
* jumlah rumah sakit adalah 276.

---

### Join Test

Pastikan:

* join tidak menggandakan rumah sakit;
* seluruh rumah sakit prioritas ditemukan pada primary dataset;
* seluruh peer benchmark memiliki hospital ID valid;
* root-cause table tidak memiliki orphan record.

---

### Filter Test

Pastikan:

* filter satu kategori bekerja;
* kombinasi filter bekerja;
* filter kosong mengembalikan seluruh dataset;
* kombinasi tanpa hasil menghasilkan DataFrame kosong, bukan error.

---

### Formatting Test

Pastikan:

* percentage;
* Indonesian currency;
* decimal;
* minute;
* count;
* missing value

ditampilkan konsisten.

---

## 21.2 Tests yang Tidak Diperlukan

Tidak perlu menguji:

* model accuracy;
* cross-validation;
* statistical coefficient;
* SHAP;
* threshold sensitivity;
* root-cause formula;
* priority score formula.

Logic tersebut merupakan tanggung jawab notebook dan telah menghasilkan artefak final.

---

# 22. Code Quality

Gunakan Ruff untuk:

* linting;
* import sorting;
* formatting.

Konfigurasi sederhana:

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = [
    "E",
    "F",
    "I",
    "B",
]

[tool.ruff.format]
quote-style = "double"
```

Tidak perlu mypy.

Type hints tetap digunakan pada shared functions:

```python
def filter_hospitals(
    dataframe: pd.DataFrame,
    filters: dict[str, list[str]],
) -> pd.DataFrame:
    ...
```

---

# 23. Deployment

## 23.1 Final Deployment Target

Gunakan Streamlit Community Cloud.

Deployment source:

```text
GitHub repository
```

Entry point:

```text
dashboard/app.py
```

Dependency file:

```text
uv.lock
```

Deklarasi dependency:

```text
pyproject.toml
```

Streamlit Community Cloud mendeteksi `uv.lock` dan menggunakan uv untuk instalasi dependency.

---

## 23.2 Deployment Requirements

Repository deployment harus memiliki:

* application code;
* required CSV artifacts;
* required JSON artifacts;
* `.streamlit/config.toml`;
* `pyproject.toml`;
* `uv.lock`;
* relative path yang konsisten.

Tidak perlu Docker.

---

## 23.3 File Size

Artefak harus cukup kecil untuk disimpan langsung di repository kompetisi.

Jangan menggunakan:

* external object storage;
* Google Drive download;
* API download;
* database connection;
* runtime notebook execution.

---

# 24. Performance

Dengan 276 baris, target performa:

| Operation                     |           Target |
| ----------------------------- | ---------------: |
| Initial load                  | Di bawah 3 detik |
| Page navigation setelah cache | Di bawah 1 detik |
| Filter update                 |  Di bawah 500 ms |
| Table rendering               | Di bawah 1 detik |
| CSV export                    | Di bawah 1 detik |

Jika dashboard lambat, penyebab kemungkinan berasal dari:

* jumlah chart terlalu banyak;
* custom HTML berlebihan;
* file dibaca berulang;
* merge dilakukan berulang;
* Plotly figure terlalu kompleks;
* page menjalankan logic analitik yang seharusnya offline.

Bukan karena ukuran dataset.

---

# 25. Error Handling

## 25.1 Missing Artifact

```python
if not artifact_path.exists():
    st.error(
        f"Artefak {artifact_path.name} tidak ditemukan. "
        "Jalankan notebook analitik dan export seluruh artefak."
    )
    st.stop()
```

---

## 25.2 Invalid Contract

```python
try:
    validate_columns(
        dataframe,
        REQUIRED_HOSPITAL_COLUMNS,
        "hospital_features_scored.csv",
    )
except ValueError as error:
    st.error(str(error))
    st.stop()
```

---

## 25.3 Empty Filter

```text
Tidak ada rumah sakit yang sesuai dengan kombinasi filter aktif.
Reset atau ubah filter untuk melanjutkan.
```

---

## 25.4 Missing Hospital Detail

```text
Data detail rumah sakit tidak tersedia pada artefak peer benchmark.
```

Jangan membuat nilai fallback atau nilai sintetis.

---

# 26. Security Scope

Dataset berada pada level rumah sakit.

Tidak terdapat:

* patient record;
* medical record;
* personal identifier;
* health data individual;
* login credential;
* API secret.

Karena itu:

* tidak diperlukan authentication;
* tidak diperlukan encryption layer khusus;
* tidak diperlukan role-based access control;
* tidak diperlukan audit login.

Tetap jangan menambahkan data pasien atau informasi personal ke repository.

---

# 27. Naming Convention

## Python Internal Names

Gunakan nama kolom asli Bahasa Indonesia.

Jangan melakukan rename seluruh dataset ke Bahasa Inggris.

Contoh:

```python
digital_maturity = dataframe[
    "skor_kematangan_digital"
]
```

Lebih baik daripada membuat duplicate alias:

```python
dataframe["digital_maturity_score"]
```

Display label tetap menggunakan istilah UI yang telah ditentukan pada dashboard structure.

---

## Display Labels

Gunakan mapping terpusat:

```python
DISPLAY_LABELS = {
    "skor_kematangan_digital": "Kematangan Digital",
    "tingkat_keterisian_tempat_tidur_persen": "BOR",
    "rata_rata_lama_rawat_hari": "Rata-rata LOS",
    "rata_rata_waktu_respons_rujukan_menit": (
        "Waktu Respons Rujukan"
    ),
    "anggaran_it_tahunan_juta_rupiah": (
        "Anggaran IT Tahunan"
    ),
}
```

Jangan menulis mapping berbeda pada setiap page.

---

# 28. Codex Implementation Rules

Codex harus:

1. membaca notebook final;
2. membaca daftar artefak pada `synapse_artifacts`;
3. membaca `dashboard_structure.md`;
4. membaca design system;
5. memeriksa nama kolom aktual pada setiap artefak;
6. membuat data contract berdasarkan kolom aktual;
7. menggunakan `hospital_features_scored.csv` sebagai dataset utama;
8. menggunakan `id_rumah_sakit` sebagai join key;
9. menggunakan artefak precomputed;
10. menjaga page file tetap ringan;
11. menggunakan Plotly untuk seluruh chart;
12. menggunakan native Streamlit table;
13. menggunakan shared formatting dan chart theme;
14. menggunakan relative path;
15. menambahkan test untuk data contract dan join.

Codex tidak boleh:

1. melatih model;
2. membaca file `.joblib` pada runtime;
3. menghitung ulang priority score;
4. menghitung ulang root-cause score;
5. menghitung ulang expected maturity;
6. menjalankan statistical test;
7. menjalankan SHAP;
8. menambahkan database;
9. menambahkan API;
10. menambahkan Docker;
11. menambahkan Parquet;
12. menambahkan Pandera;
13. menambahkan AgGrid;
14. menambahkan map dependency;
15. menambahkan filter waktu;
16. membuat synthetic historical data;
17. membuat fallback benchmark baru;
18. mengarang kolom yang tidak tersedia;
19. membuat recommendation logic kedua;
20. mengganti istilah secara tidak konsisten.

---

# 29. Implementation Sequence

## Phase 1: Data Contract

1. Inspect seluruh artefak.
2. Catat kolom masing-masing file.
3. Validasi primary key.
4. Implementasikan shared loader.
5. Implementasikan join validation.

## Phase 2: Foundation

1. Streamlit entry point.
2. Navigation.
3. Session state.
4. Global filters.
5. Number formatting.
6. Shared Plotly theme.
7. CSS tokens.

## Phase 3: Core Dashboard

1. Ringkasan Eksekutif.
2. Kesiapan Digital dan Investasi.
3. Prioritas Intervensi.
4. Hospital Explorer.

## Phase 4: Analytical Support

1. Dampak Operasional.
2. Coefficient plot.
3. Methodology page.
4. Data-quality page sections.

## Phase 5: Finalization

1. CSV export.
2. Error state.
3. Empty state.
4. Responsive layout.
5. Data contract tests.
6. Join tests.
7. Streamlit Cloud deployment.

---

# 30. Definition of Done

Technology stack dianggap berhasil diterapkan jika:

* aplikasi dijalankan dengan `uv run streamlit run dashboard/app.py`;
* environment disinkronkan dari `uv.lock` menggunakan `uv sync --frozen`;
* hanya dependency dashboard yang diinstal;
* seluruh artefak dibaca dari `synapse_artifacts`;
* raw CSV tidak diproses ulang pada runtime;
* model tidak dimuat;
* model tidak dilatih;
* seluruh halaman menggunakan source of truth yang sama;
* seluruh join menggunakan `id_rumah_sakit`;
* jumlah rumah sakit tidak berubah setelah join;
* seluruh chart menggunakan Plotly;
* seluruh tabel menggunakan native Streamlit;
* seluruh filter menggunakan shared component;
* selected hospital bertahan antarhalaman;
* priority score sama dengan output notebook;
* bottleneck sama dengan output notebook;
* rekomendasi sama dengan output notebook;
* dashboard dapat di-deploy pada Streamlit Community Cloud;
* initial load berada di bawah target;
* tidak terdapat dependency yang tidak digunakan.

---

# 31. Final Stack Summary

```text
Application:
Streamlit

Language:
Python

Runtime data:
Precomputed CSV and JSON artifacts

Primary dataset:
synapse_artifacts/hospital_features_scored.csv

Processing:
pandas and NumPy

Visualization:
Plotly

Tables:
Native Streamlit dataframe

State:
Streamlit session state

Caching:
Streamlit cache data

Testing:
pytest

Formatting and linting:
Ruff

Dependency management:
uv with pyproject.toml and uv.lock

Deployment:
Streamlit Community Cloud

Database:
None

Backend API:
None

Runtime machine learning:
None

Runtime statistical modeling:
None

Container:
None

Architecture:
Static analytical artifacts consumed by a modular Streamlit dashboard
```
