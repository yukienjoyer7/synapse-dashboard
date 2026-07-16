# Dashboard Structure Specification

## 1. Tujuan Dokumen

Dokumen ini mendefinisikan struktur informasi, hierarki KPI, komponen visual, interaksi, dan persyaratan implementasi dashboard analitik rumah sakit.

Dashboard harus membantu pengguna menjawab empat pertanyaan utama:

1. Bagaimana kondisi umum kesiapan digital dan performa operasional rumah sakit?
2. Apakah investasi sumber daya IT berhasil dikonversi menjadi kematangan digital?
3. Apakah kematangan digital berkaitan dengan performa operasional yang lebih baik?
4. Rumah sakit mana yang harus diprioritaskan untuk intervensi, mengapa, dan intervensi apa yang relevan?

Dashboard bukan hanya alat eksplorasi data. Dashboard harus berfungsi sebagai sistem pendukung keputusan untuk:

* melihat kondisi portofolio rumah sakit;
* mendeteksi kesenjangan digital;
* mengidentifikasi inefisiensi operasional;
* menemukan kegagalan konversi investasi;
* menentukan prioritas intervensi;
* membandingkan rumah sakit dengan kelompok peer yang relevan.

---

# 2. Prinsip Utama Dashboard

## 2.1 Progressive Disclosure

Informasi ditampilkan secara bertahap:

1. Portfolio signal
2. Cohort comparison
3. Root cause
4. Hospital-level evidence
5. Recommended action

Jangan menampilkan seluruh analisis dalam satu halaman.

Setiap halaman harus memiliki satu pertanyaan manajemen utama.

---

## 2.2 Decision-Oriented Design

Setiap visual harus mendukung salah satu fungsi berikut:

* mendeteksi masalah;
* membandingkan kelompok;
* mengidentifikasi anomali;
* menjelaskan penyebab;
* menentukan prioritas;
* mendukung rekomendasi.

Visual yang hanya bersifat dekoratif atau mengulang KPI tidak perlu digunakan.

---

## 2.3 Peer-Aware Comparison

Perbandingan default tidak boleh hanya menggunakan median nasional.

Urutan benchmark yang disarankan:

1. rumah sakit dengan kelas yang sama;
2. rumah sakit dengan kelas dan kepemilikan yang sama;
3. seluruh portofolio nasional.

Peer comparison hanya digunakan jika ukuran sampel memenuhi batas minimum.

Jika peer group terlalu kecil, fallback ke benchmark yang lebih luas.

Contoh:

```python
MIN_PEER_SIZE = 10
```

---

## 2.4 Descriptive, Not Causal

Dataset bersifat observasional dan cross-sectional.

Gunakan bahasa:

* berkaitan dengan;
* diasosiasikan dengan;
* menunjukkan hubungan;
* memiliki kecenderungan;
* berada di bawah ekspektasi model.

Hindari bahasa:

* menyebabkan;
* membuktikan bahwa;
* meningkatkan secara langsung;
* menghasilkan dampak kausal.

---

## 2.5 Transparent Scoring

Semua skor turunan harus memiliki:

* definisi;
* formula;
* komponen;
* bobot;
* arah interpretasi;
* rentang nilai;
* threshold;
* keterbatasan.

Priority score tidak boleh ditampilkan sebagai probabilitas risiko klinis.

Gunakan label:

> Skor prioritas deskriptif untuk membantu pengurutan intervensi.

---

# 3. Target Pengguna

## 3.1 Pengguna Utama

* manajemen konsorsium rumah sakit;
* pengelola transformasi digital;
* pengambil keputusan investasi IT;
* manajemen operasional;
* tim evaluasi performa;
* regulator atau pemilik jaringan rumah sakit.

## 3.2 Kebutuhan Pengguna

Pengguna harus dapat:

* melihat kondisi seluruh rumah sakit;
* memfilter kelompok rumah sakit;
* menemukan kelompok dengan performa rendah;
* memilih rumah sakit tertentu;
* membandingkan dengan peer;
* memahami faktor utama penyebab masalah;
* melihat rekomendasi intervensi;
* mengunduh data hasil filter.

---

# 4. Struktur Navigasi

Dashboard menggunakan enam halaman utama.

```text
01 Ringkasan Eksekutif
02 Kesiapan Digital & Investasi
03 Dampak terhadap Operasional
04 Prioritas Intervensi
05 Eksplorasi Rumah Sakit
06 Metodologi & Kualitas Data
```

Urutan halaman mengikuti alur keputusan:

```text
Kondisi portofolio
    ↓
Kesenjangan digital dan investasi
    ↓
Hubungan dengan performa operasional
    ↓
Penentuan rumah sakit prioritas
    ↓
Investigasi rumah sakit individual
    ↓
Validasi metodologi
```

---

# 5. Global Layout

## 5.1 Sidebar

Sidebar digunakan untuk:

* navigasi halaman;
* filter global;
* pencarian rumah sakit;
* pengaturan benchmark;
* tombol reset filter;
* informasi versi data.

Urutan sidebar:

```text
Navigation
Global Filters
Hospital Search
Benchmark Settings
Reset Filters
Data Version
```

---

## 5.2 Main Content

Struktur umum setiap halaman:

```text
Page Title
Page Description
Active Filter Summary
KPI Cards
Primary Visualization
Supporting Visualizations
Insight or Interpretation Panel
Detailed Table
Methodology Expander
```

Tidak semua halaman harus memiliki seluruh komponen, tetapi struktur visual harus konsisten.

---

## 5.3 Active Filter Summary

Tampilkan filter aktif di bagian atas halaman.

Contoh:

```text
Filter aktif:
Jawa Timur | Kelas B dan C | Publik | SATUSEHAT: Terhubung
```

Jika tidak ada filter:

```text
Menampilkan seluruh portofolio rumah sakit
```

Gunakan chips, pills, atau compact text summary.

---

# 6. Global Filters

## 6.1 Filter Utama

Filter berikut harus tersedia di seluruh halaman:

* provinsi;
* kelas rumah sakit;
* kepemilikan;
* status implementasi RME;
* status koneksi SATUSEHAT;
* pencarian nama atau ID rumah sakit;
* benchmark comparison.

---

## 6.2 Filter Benchmark

Opsi benchmark:

```text
Peer Default
Kelas Rumah Sakit
Kelas + Kepemilikan
Nasional
```

Default:

```text
Peer Default
```

Logika `Peer Default`:

1. gunakan kelas dan kepemilikan jika ukuran peer cukup;
2. gunakan kelas jika peer terlalu kecil;
3. gunakan nasional jika kelas terlalu kecil.

---

## 6.3 Tidak Ada Filter Waktu

Jangan menampilkan filter:

* bulan;
* kuartal;
* tahun;
* previous period;
* year-over-year.

Dataset tidak memiliki dimensi waktu longitudinal yang valid.

Jangan membuat persentase perubahan terhadap periode sebelumnya.

---

## 6.4 Reset Filter

Sediakan tombol:

```text
Reset Semua Filter
```

Tombol harus:

* menghapus seluruh filter;
* menghapus rumah sakit terpilih;
* mengembalikan benchmark ke default;
* mengembalikan halaman ke state awal.

---

# 7. Shared Application State

Gunakan `st.session_state` untuk menyimpan:

```python
st.session_state.selected_hospital_id
st.session_state.selected_hospital_name
st.session_state.active_province
st.session_state.active_hospital_class
st.session_state.active_ownership
st.session_state.active_rme_status
st.session_state.active_satusehat_status
st.session_state.active_benchmark
st.session_state.priority_only
```

Ketika pengguna memilih rumah sakit pada chart atau table:

1. simpan ID rumah sakit;
2. update state;
3. tampilkan ringkasan rumah sakit;
4. sediakan tombol menuju halaman Eksplorasi Rumah Sakit.

---

# 8. Hierarki KPI

KPI dibagi menjadi tiga tingkat:

1. Executive KPI
2. Diagnostic KPI
3. Evidence KPI

---

## 8.1 Executive KPI

Executive KPI tampil pada halaman Ringkasan Eksekutif.

### KPI 1: Median Kematangan Digital

**Field utama**

```text
skor_kematangan_digital
```

**Formula**

```python
median_digital_maturity = filtered_df[
    "skor_kematangan_digital"
].median()
```

**Unit**

```text
Skor
```

**Interpretasi**

Semakin tinggi nilai, semakin matang kemampuan digital rumah sakit.

**Comparison**

Bandingkan dengan:

* median peer;
* median nasional;
* keseluruhan dataset jika tidak ada filter.

---

### KPI 2: Cakupan SATUSEHAT

**Formula**

```python
satusehat_coverage = (
    filtered_df["status_satusehat"].eq("Terhubung").mean() * 100
)
```

**Unit**

```text
Persen rumah sakit
```

**Denominator**

Jumlah rumah sakit setelah filter.

---

### KPI 3: Median Waktu Respons Rujukan

**Formula**

```python
median_referral_response = filtered_df[
    "waktu_respons_rujukan_menit"
].median()
```

**Unit**

```text
Menit
```

**Arah KPI**

Semakin rendah semakin baik.

---

### KPI 4: Rumah Sakit di Luar Rentang BOR

BOR harus dievaluasi menggunakan salah satu dari dua pendekatan:

#### Pendekatan A: Threshold Bisnis

```python
BOR_LOWER_BOUND = configurable_value
BOR_UPPER_BOUND = configurable_value
```

#### Pendekatan B: Peer-Adjusted Deviation

```python
bor_deviation = abs(
    hospital_bor - peer_median_bor
)
```

Pendekatan peer-adjusted lebih disarankan jika threshold universal tidak disediakan oleh domain expert.

**Formula KPI**

```python
outside_bor_share = (
    filtered_df["bor_status"].eq("Di Luar Rentang").mean() * 100
)
```

---

### KPI 5: Kegagalan Konversi Investasi

Kondisi rumah sakit memiliki sumber daya IT tinggi, tetapi kematangan digital berada di bawah ekspektasi.

**Input**

* anggaran IT per tempat tidur;
* staf IT per 100 tempat tidur;
* perangkat IoT per 100 tempat tidur;
* digital maturity actual;
* digital maturity expected.

**Formula gap**

```python
digital_conversion_gap = (
    actual_digital_maturity
    - expected_digital_maturity
)
```

**Flag**

```python
investment_conversion_failure = (
    investment_intensity >= investment_threshold
) & (
    digital_conversion_gap < conversion_gap_threshold
)
```

Threshold harus disimpan di konfigurasi.

---

### KPI 6: Inefisiensi Ganda

Rumah sakit memiliki:

* defisit digital tinggi;
* beban operasional tinggi.

**Flag**

```python
double_inefficiency = (
    digital_deficit_percentile >= DIGITAL_DEFICIT_THRESHOLD
) & (
    operational_burden_percentile >= OPERATIONAL_BURDEN_THRESHOLD
)
```

Contoh default:

```python
DIGITAL_DEFICIT_THRESHOLD = 0.75
OPERATIONAL_BURDEN_THRESHOLD = 0.75
```

Threshold tidak boleh di-hardcode di banyak file.

Simpan pada satu file konfigurasi.

---

# 9. Diagnostic KPI

## 9.1 Digital and Investment KPI

* tingkat implementasi RME;
* cakupan SATUSEHAT;
* median digital maturity;
* telemedicine utilization;
* anggaran IT per tempat tidur;
* staf IT per 100 tempat tidur;
* perangkat IoT per 100 tempat tidur;
* investment intensity score;
* actual digital maturity;
* expected digital maturity;
* digital conversion gap;
* conversion segment.

---

## 9.2 Operational KPI

* BOR;
* BOR deviation;
* LOS;
* referral response time;
* monthly patient visits;
* patient visits per bed;
* patient visits per employee;
* telemedicine share;
* operational burden score;
* operational burden percentile.

---

## 9.3 Prioritization KPI

* digital deficit score;
* digital deficit percentile;
* operational burden score;
* operational burden percentile;
* investment underperformance score;
* priority score;
* priority rank;
* dominant bottleneck;
* double-inefficiency flag;
* intervention category.

---

# 10. KPI Card Specification

Setiap kartu KPI harus memiliki:

1. nama KPI;
2. nilai utama;
3. unit;
4. comparison;
5. status;
6. denominator;
7. tooltip definisi.

Contoh:

```text
Median Respons Rujukan
31,4 menit
4,8 menit lebih lambat dari median peer
PERLU PERHATIAN
68 rumah sakit terfilter
```

Jangan hanya menampilkan:

```text
31.4
↓ 13%
```

Delta harus selalu memiliki referensi pembanding yang jelas.

---

## 10.1 Status Label

Gunakan label status:

```text
BAIK
STABIL
PERLU PERHATIAN
PRIORITAS
DATA TERBATAS
```

Hindari penggunaan warna tanpa teks.

---

## 10.2 KPI Tooltip

Tooltip harus menjelaskan:

* definisi;
* formula singkat;
* arah interpretasi;
* denominator;
* benchmark;
* limitation jika ada.

---

# 11. Page 1: Ringkasan Eksekutif

## 11.1 Tujuan

Memberikan ringkasan kondisi seluruh portofolio dan menunjukkan lokasi utama yang membutuhkan perhatian.

## 11.2 Pertanyaan Utama

> Di bagian mana konsorsium harus memusatkan perhatian?

---

## 11.3 Layout

```text
Page Header
Active Filter Summary
6 Executive KPI Cards
Priority Quadrant
Portfolio Heatmap
Top Priority Watchlist
Dynamic Findings
```

---

## 11.4 KPI Cards

Tampilkan maksimal enam kartu:

1. Median Kematangan Digital
2. Cakupan SATUSEHAT
3. Median Respons Rujukan
4. Rumah Sakit di Luar Rentang BOR
5. Kegagalan Konversi Investasi
6. Inefisiensi Ganda

Gunakan layout:

```python
cols = st.columns(6)
```

Pada viewport sempit, izinkan menjadi dua baris.

---

## 11.5 Primary Visualization

### Digital Maturity vs Operational Burden Quadrant

**X-axis**

```text
Digital maturity
```

atau:

```text
Digital deficit percentile
```

Pilih satu definisi secara konsisten.

Rekomendasi:

```text
X-axis = Digital maturity
Y-axis = Operational burden percentile
```

**Bubble size**

```text
Jumlah tempat tidur
```

atau:

```text
Jumlah kunjungan pasien bulanan
```

Default:

```text
Jumlah tempat tidur
```

**Color**

Status prioritas:

```text
Normal
Watch
Priority
```

**Tooltip**

* nama rumah sakit;
* provinsi;
* kelas;
* ownership;
* digital maturity;
* expected digital maturity;
* operational burden;
* referral response;
* BOR;
* priority score.

**Quadrant labels**

```text
Siap dan Efisien
Siap namun Tertekan
Terbatas namun Stabil
Prioritas Intervensi
```

**Reference lines**

* median digital maturity;
* threshold operational burden;
* atau median masing-masing sumbu.

Threshold harus dijelaskan di tooltip atau methodology expander.

---

## 11.6 Portfolio Heatmap

Tujuan:

Menunjukkan distribusi masalah berdasarkan provinsi, kelas, atau ownership.

Pilihan default:

```text
Rows: Provinsi
Columns: KPI category
Values: Standardized deviation atau share rumah sakit bermasalah
```

Kolom:

* digital maturity deficit;
* SATUSEHAT gap;
* referral response burden;
* BOR deviation;
* double inefficiency share.

Alternatif jika provinsi terlalu banyak:

* horizontal ranked heatmap;
* hanya tampilkan top 15;
* sediakan scroll;
* sediakan sort berdasarkan priority score.

---

## 11.7 Top Priority Watchlist

Tampilkan 10 rumah sakit prioritas.

Kolom:

```text
Rank
Hospital
Province
Class
Priority Score
Digital Deficit
Operational Burden
Dominant Bottleneck
```

Interaksi:

* klik row memilih rumah sakit;
* tombol `Lihat Detail`;
* tombol `Buka Prioritas Intervensi`.

---

## 11.8 Dynamic Findings

Tampilkan tiga insight berbasis data terfilter:

### Finding 1: Portfolio Signal

Contoh:

```text
Kelompok rumah sakit kelas C memiliki median kematangan digital terendah pada filter aktif.
```

### Finding 2: Operational Risk

Contoh:

```text
Rumah sakit dengan defisit digital tertinggi memiliki waktu respons rujukan lebih lambat dibandingkan peer median.
```

### Finding 3: Recommended Focus

Contoh:

```text
Prioritas utama berada pada rumah sakit dengan staf IT rendah dan beban kunjungan tinggi.
```

Insight harus dihasilkan dari rules yang deterministic.

Jangan menggunakan LLM pada runtime untuk menghasilkan insight.

---

## 11.9 Empty State

Jika filter menghasilkan data kosong:

```text
Tidak ada rumah sakit yang sesuai dengan kombinasi filter ini.
Ubah atau reset filter untuk melanjutkan.
```

---

# 12. Page 2: Kesiapan Digital & Investasi

## 12.1 Tujuan

Mengevaluasi kesiapan digital dan kemampuan rumah sakit dalam mengonversi investasi IT menjadi kematangan digital.

## 12.2 Pertanyaan Utama

> Apakah sumber daya IT berhasil dikonversi menjadi kemampuan digital?

---

## 12.3 Layout

```text
Page Header
Active Filter Summary
5 Diagnostic KPI Cards
Digital Maturity Distribution
Actual vs Expected Maturity
Investment Conversion Matrix
Investment Component Analysis
Action Table
```

---

## 12.4 KPI Cards

1. Median Digital Maturity
2. RME Adoption Rate
3. SATUSEHAT Coverage
4. Investment Conversion Failure Rate
5. Median IT Staff per 100 Beds

---

## 12.5 Digital Maturity by Hospital Class

Gunakan:

* boxplot;
* jittered points;
* sample size;
* median marker.

X-axis:

```text
Hospital class
```

Y-axis:

```text
Digital maturity score
```

Tooltip:

* median;
* Q1;
* Q3;
* sample size;
* minimum;
* maximum.

---

## 12.6 Digital Maturity by Ownership

Gunakan horizontal boxplot atau dot-interval plot.

Jangan gunakan bar chart rata-rata tanpa distribusi.

---

## 12.7 Actual vs Expected Digital Maturity

**X-axis**

```text
Expected digital maturity
```

**Y-axis**

```text
Actual digital maturity
```

**Reference line**

```text
y = x
```

Interpretasi:

* di atas garis: overperform;
* dekat garis: sesuai ekspektasi;
* di bawah garis: underperform.

**Bubble size**

```text
Investment intensity
```

**Color**

```text
Conversion segment
```

Tooltip:

* actual maturity;
* expected maturity;
* conversion gap;
* IT budget per bed;
* IT staff per 100 beds;
* IoT per 100 beds;
* class;
* ownership.

---

## 12.8 Investment Conversion Matrix

Gunakan 2×2 matrix.

### Sumbu X

```text
Investment intensity
```

### Sumbu Y

```text
Digital conversion gap
```

### Segmen

| Investment | Conversion | Segment                      |
| ---------- | ---------- | ---------------------------- |
| Tinggi     | Positif    | Investor Digital Efektif     |
| Tinggi     | Negatif    | Kegagalan Konversi Investasi |
| Rendah     | Positif    | Pemimpin Efisien Sumber Daya |
| Rendah     | Negatif    | Keterbatasan Sumber Daya     |

Gunakan label segmen secara eksplisit.

---

## 12.9 Investment Component Analysis

Tampilkan tiga komponen:

* IT budget per bed;
* IT staff per 100 beds;
* IoT devices per 100 beds.

Pilihan visual:

* small multiples scatterplot;
* ranked dot plot;
* standardized component comparison.

Jangan gunakan radar chart.

---

## 12.10 Action Table

Kolom:

```text
Hospital
Province
Class
Ownership
Digital Maturity
Expected Maturity
Conversion Gap
IT Budget per Bed
IT Staff per 100 Beds
IoT per 100 Beds
Conversion Segment
Suggested Investigation
```

Urutan default:

```text
Conversion Gap ascending
```

Rumah sakit dengan gap paling negatif ditampilkan pertama.

---

## 12.11 Suggested Investigation Rules

Contoh rules:

### High Budget, Low Maturity

```text
Audit governance investasi IT, utilisasi sistem, dan kesesuaian implementasi dengan workflow.
```

### Low IT Staff, Low Maturity

```text
Evaluasi kecukupan kapasitas staf IT dan kebutuhan pendampingan implementasi.
```

### High Infrastructure, Low Integration

```text
Prioritaskan interoperabilitas, integrasi SATUSEHAT, dan standardisasi pertukaran data.
```

### Low Investment, High Maturity

```text
Identifikasi praktik efisien yang dapat direplikasi ke rumah sakit lain.
```

---

# 13. Page 3: Dampak terhadap Operasional

## 13.1 Tujuan

Menilai hubungan antara kesiapan digital dan performa operasional.

## 13.2 Pertanyaan Utama

> Apakah kesiapan digital berkaitan dengan performa operasional yang lebih baik?

---

## 13.3 Layout

```text
Page Header
Active Filter Summary
5 Operational KPI Cards
Adjusted Association Plot
Digital Maturity vs Referral Response
Operational Performance by Maturity Group
Operational Profile Heatmap
Interpretation Panel
```

---

## 13.4 KPI Cards

1. Median Referral Response
2. Median BOR
3. Share Outside BOR Range
4. Median LOS
5. Median Telemedicine Share

---

## 13.5 Adjusted Association Coefficient Plot

Tampilkan hasil model untuk outcome:

```text
Referral response time
```

Predictor utama:

* digital maturity;
* RME implementation;
* SATUSEHAT connection.

Tampilkan:

* coefficient;
* confidence interval;
* reference line pada zero;
* sample size;
* model specification.

Untuk digital maturity, tampilkan efek per 10 poin.

Contoh transformasi:

```python
effect_per_10_points = coefficient * 10
```

Label:

```text
Perubahan estimasi waktu respons untuk kenaikan 10 poin digital maturity
```

Jangan hanya menampilkan p-value.

---

## 13.6 Digital Maturity vs Referral Response

**X-axis**

```text
Digital maturity
```

**Y-axis**

```text
Referral response time
```

**Color**

```text
Hospital class
```

**Trend**

* regression line;
* LOWESS;
* atau adjusted prediction line.

Jika menggunakan trend line, jelaskan:

```text
Garis menunjukkan pola asosiasi, bukan hubungan kausal.
```

---

## 13.7 Operational Performance by Maturity Group

Bagi digital maturity menjadi kelompok:

```text
Low
Medium
High
```

Gunakan:

* tertile;
* atau threshold berdasarkan distribusi.

Tampilkan:

* referral response;
* BOR deviation;
* LOS;
* telemedicine share;
* patient load.

Visual yang disarankan:

* dot plot;
* boxplot;
* small multiples.

---

## 13.8 Operational Profile Heatmap

Rows:

* hospital class;
* ownership;
* atau cohort digital maturity.

Columns:

* BOR deviation;
* LOS;
* referral response;
* patient load per bed;
* patient load per employee.

Values:

```text
Standardized score
```

Standardisasi harus dilakukan dengan arah yang konsisten.

Contoh:

* nilai tinggi selalu berarti beban lebih buruk;
* jika KPI makin rendah makin buruk, reverse sign sebelum standardisasi.

---

## 13.9 Interpretation Panel

Panel harus menjelaskan:

* arah asosiasi;
* kekuatan efek;
* uncertainty;
* adjusted covariates;
* limitation.

Contoh:

```text
Setelah mengontrol karakteristik rumah sakit yang tersedia, kematangan digital yang lebih tinggi berkaitan dengan waktu respons rujukan yang lebih rendah. Hubungan ini bersifat observasional dan tidak dapat ditafsirkan sebagai efek kausal.
```

---

# 14. Page 4: Prioritas Intervensi

## 14.1 Tujuan

Mengubah hasil analisis menjadi daftar prioritas dan rekomendasi tindakan.

## 14.2 Pertanyaan Utama

> Rumah sakit mana yang harus ditangani terlebih dahulu, mengapa, dan dengan intervensi apa?

---

## 14.3 Layout

```text
Page Header
Active Filter Summary
5 Priority KPI Cards
Priority Matrix
Root Cause Pareto
Prioritized Action Table
Cohort-Level Action Plan
Selected Hospital Detail
```

---

## 14.4 KPI Cards

1. Jumlah Rumah Sakit Prioritas
2. Persentase Portofolio Terflag
3. Median Priority Score
4. Dominant Bottleneck
5. Highest-Priority Cohort

---

## 14.5 Priority Score

Default formula:

```python
priority_score = (
    0.35 * digital_deficit_percentile
    + 0.45 * operational_burden_percentile
    + 0.20 * investment_underperformance_percentile
)
```

Simpan bobot pada konfigurasi:

```python
PRIORITY_WEIGHTS = {
    "digital_deficit": 0.35,
    "operational_burden": 0.45,
    "investment_underperformance": 0.20,
}
```

Validasi:

```python
assert abs(sum(PRIORITY_WEIGHTS.values()) - 1.0) < 1e-9
```

---

## 14.6 Priority Matrix

### X-axis

```text
Digital deficit percentile
```

### Y-axis

```text
Operational burden percentile
```

### Bubble size

```text
Investment underperformance
```

### Color

```text
Priority tier
```

Priority tier:

```text
Low
Watch
High
Critical
```

Contoh threshold:

```python
if score >= 0.80:
    tier = "Critical"
elif score >= 0.65:
    tier = "High"
elif score >= 0.45:
    tier = "Watch"
else:
    tier = "Low"
```

Threshold harus configurable.

---

## 14.7 Root Cause Classification

Setiap rumah sakit harus memiliki satu `dominant_bottleneck`.

Kategori minimum:

```text
Investment Conversion Failure
IT Staffing Limitation
Infrastructure Limitation
Integration and Adoption Gap
Operational Overload
Capacity Imbalance
No Dominant Bottleneck
```

Logika root cause harus rule-based dan transparan.

Contoh:

```python
if (
    investment_intensity_high
    and digital_conversion_gap_low
):
    bottleneck = "Investment Conversion Failure"

elif (
    it_staff_per_100_beds_low
    and digital_maturity_low
):
    bottleneck = "IT Staffing Limitation"

elif (
    iot_intensity_low
    and digital_maturity_low
):
    bottleneck = "Infrastructure Limitation"

elif (
    satusehat_not_connected
    or rme_not_implemented
):
    bottleneck = "Integration and Adoption Gap"

elif (
    patient_load_high
    and operational_burden_high
):
    bottleneck = "Operational Overload"

elif (
    bor_deviation_high
):
    bottleneck = "Capacity Imbalance"

else:
    bottleneck = "No Dominant Bottleneck"
```

---

## 14.8 Root Cause Pareto

Tampilkan:

* jumlah rumah sakit per bottleneck;
* persentase rumah sakit prioritas;
* cumulative share.

Urutkan dari kategori paling sering.

---

## 14.9 Prioritized Action Table

Kolom:

```text
Rank
Hospital
Province
Class
Ownership
Priority Score
Priority Tier
Digital Deficit
Operational Burden
Investment Underperformance
Dominant Bottleneck
Recommended Action
Monitoring KPI
```

Default sort:

```text
Priority Score descending
```

Fitur:

* search;
* filter tier;
* filter bottleneck;
* export CSV;
* row selection.

---

## 14.10 Recommendation Mapping

Gunakan mapping deterministic.

### Investment Conversion Failure

**Recommended action**

```text
Lakukan audit tata kelola investasi IT, utilisasi sistem, integrasi workflow, dan tingkat adopsi pengguna sebelum menambah pengadaan baru.
```

**Monitoring KPI**

```text
Digital conversion gap
```

---

### IT Staffing Limitation

**Recommended action**

```text
Tambahkan kapasitas operasional IT, susun rencana pengembangan kompetensi, dan evaluasi kebutuhan support implementasi.
```

**Monitoring KPI**

```text
IT staff per 100 beds
```

---

### Infrastructure Limitation

**Recommended action**

```text
Prioritaskan infrastruktur dasar dan perangkat yang berhubungan langsung dengan kebutuhan layanan sebelum implementasi teknologi lanjutan.
```

**Monitoring KPI**

```text
IoT devices per 100 beds
```

---

### Integration and Adoption Gap

**Recommended action**

```text
Prioritaskan interoperabilitas, koneksi SATUSEHAT, implementasi RME, dan standardisasi workflow penggunaan sistem.
```

**Monitoring KPI**

```text
SATUSEHAT coverage dan RME adoption
```

---

### Operational Overload

**Recommended action**

```text
Evaluasi distribusi beban pasien, kapasitas layanan, alur rujukan, dan kebutuhan redistribusi sumber daya.
```

**Monitoring KPI**

```text
Patient load per bed dan referral response time
```

---

### Capacity Imbalance

**Recommended action**

```text
Tinjau kapasitas tempat tidur, pola utilisasi, alur masuk dan keluar pasien, serta potensi ketidakseimbangan layanan.
```

**Monitoring KPI**

```text
BOR deviation dan LOS
```

---

## 14.11 Cohort-Level Action Plan

Tampilkan tabel ringkas:

| Cohort                         | Evidence                | Recommended Intervention      | Monitoring KPI          |
| ------------------------------ | ----------------------- | ----------------------------- | ----------------------- |
| High investment, low maturity  | Negative conversion gap | Governance and workflow audit | Conversion gap          |
| Low IT staffing, high burden   | Staffing limitation     | Increase IT capacity          | IT staff per 100 beds   |
| High maturity, poor operations | Operational bottleneck  | Process redesign              | Referral response, LOS  |
| Low resources, high maturity   | Efficient conversion    | Replicate best practices      | Maturity per investment |

---

# 15. Page 5: Eksplorasi Rumah Sakit

## 15.1 Tujuan

Menyediakan analisis individual terhadap satu rumah sakit dan perbandingannya dengan peer.

## 15.2 Pertanyaan Utama

> Bagaimana posisi rumah sakit ini dibandingkan dengan rumah sakit sejenis?

---

## 15.3 Hospital Selector

Pengguna dapat memilih rumah sakit melalui:

* search bar;
* dropdown;
* table selection;
* cross-navigation dari halaman lain.

Simpan ID rumah sakit pada `session_state`.

---

## 15.4 Hospital Header

Tampilkan:

```text
Hospital Name
Hospital ID
Province
Class
Ownership
Number of Beds
Number of Services
RME Status
SATUSEHAT Status
Priority Tier
Dominant Bottleneck
```

---

## 15.5 Peer Benchmark Panel

Gunakan bullet chart atau horizontal comparison bar.

KPI:

* digital maturity;
* IT budget per bed;
* IT staff per 100 beds;
* IoT per 100 beds;
* BOR;
* LOS;
* referral response;
* patient load per bed;
* telemedicine share.

Setiap KPI menampilkan:

* hospital value;
* peer median;
* peer Q1;
* peer Q3;
* national median;
* percentile rank;
* status.

---

## 15.6 Benchmark Card Example

```text
Digital Maturity
Hospital: 58
Peer median: 67
Peer IQR: 61–74
National median: 65
Peer percentile: 23
Status: Below Peer
```

---

## 15.7 Digital Conversion Panel

Tampilkan:

* actual maturity;
* expected maturity;
* digital conversion gap;
* investment intensity;
* conversion segment.

Interpretation example:

```text
Rumah sakit memiliki intensitas investasi di atas median peer, tetapi kematangan digital berada di bawah nilai yang diharapkan berdasarkan karakteristik sumber daya yang tersedia.
```

---

## 15.8 Operational Burden Panel

Tampilkan komponen pembentuk operational burden:

* referral response;
* BOR deviation;
* LOS;
* patient load per bed;
* patient load per employee.

Tampilkan kontribusi setiap komponen terhadap burden score.

Gunakan horizontal contribution bar.

---

## 15.9 Priority Score Decomposition

Tampilkan tiga komponen:

```text
Digital Deficit
Operational Burden
Investment Underperformance
```

Formula harus terlihat melalui expander.

Contoh:

```text
Priority Score = 35% Digital Deficit
               + 45% Operational Burden
               + 20% Investment Underperformance
```

---

## 15.10 Root Cause and Recommendation

Tampilkan:

```text
Dominant Bottleneck
Supporting Evidence
Recommended Action
Monitoring KPI
```

Contoh:

```text
Dominant Bottleneck:
IT Staffing Limitation

Evidence:
Staf IT per 100 tempat tidur berada pada persentil 18 peer group.
Digital maturity berada 11 poin di bawah ekspektasi.

Recommended Action:
Evaluasi kecukupan staf IT dan kebutuhan support implementasi.

Monitoring KPI:
IT staff per 100 beds
Digital conversion gap
```

---

## 15.11 Peer Table

Kolom:

```text
Hospital
Digital Maturity
Expected Maturity
Conversion Gap
IT Staff per 100 Beds
BOR
LOS
Referral Response
Operational Burden
Priority Score
```

Filter peer table mengikuti benchmark aktif.

---

# 16. Page 6: Metodologi & Kualitas Data

## 16.1 Tujuan

Menyediakan transparansi analitik dan menjelaskan batas interpretasi dashboard.

## 16.2 Sections

Gunakan expander atau tabs:

```text
Dataset
KPI Dictionary
Derived Metrics
Peer Definition
Priority Methodology
Statistical Models
Data Quality
Limitations
Versioning
```

---

## 16.3 Dataset Section

Tampilkan:

* jumlah rumah sakit;
* jumlah variabel;
* unit analisis;
* cakupan geografis;
* jenis data;
* data source;
* data version.

---

## 16.4 KPI Dictionary

Tabel:

```text
KPI Name
Source Column
Formula
Unit
Direction
Interpretation
Page Usage
```

---

## 16.5 Derived Metric Documentation

Dokumentasikan:

* IT budget per bed;
* IT staff per 100 beds;
* IoT per 100 beds;
* patient load per bed;
* patient load per employee;
* telemedicine share;
* investment intensity;
* expected maturity;
* conversion gap;
* operational burden;
* digital deficit;
* priority score.

---

## 16.6 Statistical Model Documentation

Untuk setiap model, tampilkan:

```text
Outcome
Predictors
Controls
Estimator
Cross-validation
Sample size
MAE
RMSE
R²
Limitations
```

Jika menggunakan out-of-fold prediction untuk expected maturity:

* jelaskan jumlah folds;
* random seed;
* preprocessing;
* handling missing data;
* model type.

---

## 16.7 Data Quality

Tampilkan:

* missingness per variable;
* duplicate count;
* invalid value count;
* outlier flags;
* sample size setelah filter;
* peer group size;
* variable coverage.

Gunakan heatmap missingness atau ranked bar chart.

---

## 16.8 Limitation Section

Minimal harus mencakup:

* data bersifat cross-sectional;
* hubungan tidak dapat diinterpretasikan sebagai kausal;
* threshold bersifat analytical atau operational assumption;
* priority score merupakan alat prioritization;
* kualitas hasil bergantung pada kelengkapan data;
* peer comparison dapat tidak stabil pada kelompok kecil;
* expected maturity merupakan estimasi model;
* binary adoption tidak mengukur kualitas implementasi.

---

# 17. Data Contract

## 17.1 Raw Dataset

Buat data loader yang memvalidasi kolom minimum.

Contoh:

```python
REQUIRED_RAW_COLUMNS = [
    "hospital_id",
    "hospital_name",
    "province",
    "hospital_class",
    "ownership",
    "number_of_beds",
    "monthly_patient_visits",
    "digital_maturity_score",
    "rme_status",
    "satusehat_status",
    "referral_response_minutes",
    "bor",
    "los",
    "annual_it_budget",
    "it_staff_count",
    "iot_device_count",
    "telemedicine_visits",
]
```

Nama final harus mengikuti nama kolom aktual dataset.

---

## 17.2 Dashboard Analytics Dataset

Disarankan memiliki satu tabel hasil preprocessing:

```text
hospital_id
hospital_name
province
hospital_class
ownership
number_of_beds
number_of_services
monthly_patient_visits
digital_maturity_score
rme_status
satusehat_status
referral_response_minutes
bor
los
annual_it_budget
it_staff_count
iot_device_count
telemedicine_visits
it_budget_per_bed
it_staff_per_100_beds
iot_per_100_beds
patient_load_per_bed
patient_load_per_employee
telemedicine_share
investment_intensity_score
investment_intensity_percentile
expected_digital_maturity
digital_conversion_gap
conversion_segment
digital_deficit_score
digital_deficit_percentile
operational_burden_score
operational_burden_percentile
investment_underperformance_score
investment_underperformance_percentile
double_inefficiency_flag
priority_score
priority_rank
priority_tier
dominant_bottleneck
recommended_action
monitoring_kpi
peer_group
peer_group_size
```

---

## 17.3 Model Result Tables

Simpan output model secara terpisah.

### Association Model

```text
model_name
outcome
predictor
coefficient
standard_error
ci_lower
ci_upper
p_value
n_obs
model_specification
```

### Model Metrics

```text
model_name
mae
rmse
r2
n_obs
cv_folds
random_seed
```

---

# 18. Suggested Project Structure

```text
dashboard/
├── app.py
├── pages/
│   ├── 01_executive_summary.py
│   ├── 02_digital_investment.py
│   ├── 03_operational_impact.py
│   ├── 04_intervention_priority.py
│   ├── 05_hospital_explorer.py
│   └── 06_methodology.py
├── components/
│   ├── filters.py
│   ├── kpi_cards.py
│   ├── charts.py
│   ├── tables.py
│   ├── insight_panels.py
│   ├── hospital_header.py
│   ├── benchmark_components.py
│   └── empty_states.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── exports/
├── analytics/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── peer_benchmark.py
│   ├── digital_conversion.py
│   ├── operational_burden.py
│   ├── priority_scoring.py
│   ├── bottleneck_rules.py
│   └── model_outputs.py
├── utils/
│   ├── config.py
│   ├── constants.py
│   ├── formatting.py
│   ├── validation.py
│   ├── session_state.py
│   └── export.py
├── styles/
│   ├── theme.css
│   └── components.css
├── tests/
│   ├── test_feature_engineering.py
│   ├── test_priority_scoring.py
│   ├── test_peer_benchmark.py
│   ├── test_bottleneck_rules.py
│   └── test_data_validation.py
└── README.md
```

---

# 19. Component Requirements

## 19.1 KPI Card Component

Function signature:

```python
def render_kpi_card(
    title: str,
    value: str,
    comparison: str | None = None,
    status: str | None = None,
    denominator: str | None = None,
    help_text: str | None = None,
) -> None:
    ...
```

---

## 19.2 Filter Component

Function signature:

```python
def render_global_filters(
    df: pd.DataFrame,
) -> dict:
    ...
```

Output:

```python
{
    "province": ...,
    "hospital_class": ...,
    "ownership": ...,
    "rme_status": ...,
    "satusehat_status": ...,
    "benchmark": ...,
}
```

---

## 19.3 Benchmark Function

```python
def get_peer_group(
    df: pd.DataFrame,
    hospital_row: pd.Series,
    benchmark_mode: str,
    min_peer_size: int = 10,
) -> pd.DataFrame:
    ...
```

Fallback logic harus diuji.

---

## 19.4 Priority Scoring Function

```python
def calculate_priority_score(
    df: pd.DataFrame,
    weights: dict[str, float],
) -> pd.DataFrame:
    ...
```

Function harus:

* memvalidasi bobot;
* menangani missing value;
* menghasilkan percentile;
* menghasilkan tier;
* menghasilkan rank.

---

## 19.5 Recommendation Function

```python
def assign_recommendation(
    bottleneck: str,
) -> tuple[str, str]:
    ...
```

Output:

```python
recommended_action, monitoring_kpi
```

---

# 20. Charting Requirements

## 20.1 General

Gunakan library chart yang mendukung interaksi.

Rekomendasi:

```text
Plotly
```

Gunakan satu library utama secara konsisten.

---

## 20.2 Tooltip

Tooltip harus:

* memiliki unit;
* menggunakan nama field yang mudah dipahami;
* tidak menampilkan nama kolom mentah;
* menampilkan sample context;
* membatasi jumlah desimal.

---

## 20.3 Axis

Semua axis harus memiliki:

* label;
* unit;
* format angka;
* direction yang jelas.

Contoh:

```text
Waktu Respons Rujukan, menit
Anggaran IT per Tempat Tidur, juta rupiah
```

---

## 20.4 Number Formatting

Gunakan helper function:

```python
format_integer()
format_decimal()
format_percentage()
format_currency_idr()
format_minutes()
format_score()
```

Contoh format:

```text
1.250
67,4%
Rp12,5 juta
31,4 menit
```

---

## 20.5 Color Semantics

Color harus konsisten:

```text
Neutral
Positive
Watch
Priority
Critical
Selected
```

Jangan menggunakan warna merah dan hijau sebagai satu-satunya pembeda.

Selalu sertakan:

* label;
* icon;
* pattern;
* border;
* atau text annotation.

---

## 20.6 Selected Hospital

Rumah sakit terpilih harus:

* memiliki outline lebih tebal;
* tetap terlihat meskipun berada di bawah bubble lain;
* memiliki annotation;
* disimpan pada session state.

---

# 21. Table Requirements

Semua tabel utama harus mendukung:

* sorting;
* searching;
* filtering;
* pagination;
* download CSV;
* conditional formatting;
* fixed header.

Jangan menampilkan seluruh kolom secara default.

Gunakan kolom detail pada expander atau drill-down.

---

# 22. Download and Export

Sediakan export untuk:

* filtered hospital dataset;
* priority table;
* peer comparison;
* KPI summary;
* methodology configuration.

Nama file contoh:

```text
hospital_priority_filtered.csv
hospital_peer_comparison.csv
dashboard_kpi_summary.csv
```

Tambahkan metadata:

* export timestamp;
* active filters;
* benchmark type;
* data version.

---

# 23. Performance Requirements

## 23.1 Caching

Gunakan:

```python
@st.cache_data
```

Untuk:

* loading dataset;
* preprocessing;
* reading model outputs;
* aggregated statistics;
* peer benchmark computation.

Gunakan:

```python
@st.cache_resource
```

Hanya jika ada model atau resource berat.

Dashboard sebaiknya tidak retrain model setiap reload.

---

## 23.2 Precomputed Outputs

Precompute:

* expected digital maturity;
* digital conversion gap;
* percentiles;
* operational burden;
* priority score;
* rank;
* bottleneck;
* recommendation;
* model coefficient output.

Simpan sebagai Parquet jika memungkinkan.

---

## 23.3 Runtime

Runtime dashboard fokus pada:

* filtering;
* aggregation;
* rendering;
* lookup;
* export.

Jangan menjalankan cross-validation atau model fitting pada runtime normal.

---

# 24. Validation Requirements

## 24.1 Data Validation

Validasi:

* required columns;
* unique hospital ID;
* non-negative beds;
* non-negative staff;
* BOR range;
* LOS range;
* referral time range;
* maturity score range;
* valid categorical values.

---

## 24.2 Derived Metrics Validation

Contoh:

```python
assert (df["it_staff_per_100_beds"] >= 0).all()
assert df["priority_score"].between(0, 1).all()
assert df["priority_rank"].notna().all()
```

---

## 24.3 Filter Validation

Pastikan:

* filter tidak menghasilkan error;
* state konsisten antarhalaman;
* benchmark fallback berjalan;
* empty state muncul saat data kosong.

---

## 24.4 Scoring Validation

Test:

* weights sum to 1;
* score direction benar;
* semakin buruk input, semakin tinggi priority score;
* missing values tidak otomatis menjadi nol;
* ranking stabil untuk input yang sama.

---

# 25. Error and Empty States

## 25.1 Missing Data

```text
Data tidak tersedia untuk KPI ini pada filter aktif.
```

## 25.2 Peer Group Too Small

```text
Jumlah rumah sakit peer terlalu kecil. Benchmark dialihkan ke kelompok yang lebih luas.
```

## 25.3 Model Output Missing

```text
Hasil model belum tersedia. Visual hubungan teradjust tidak dapat ditampilkan.
```

## 25.4 Invalid Data

```text
Sebagian observasi tidak dapat digunakan karena nilai tidak valid.
Lihat halaman Metodologi untuk detail.
```

---

# 26. Accessibility Requirements

Dashboard harus:

* memiliki contrast ratio yang cukup;
* tidak bergantung hanya pada warna;
* menggunakan font minimal 14 px;
* menggunakan label axis yang jelas;
* memiliki tooltip yang dapat dibaca;
* menghindari teks panjang di dalam chart;
* menyediakan table alternative untuk informasi utama.

---

# 27. Responsive Behaviour

## Desktop

* KPI cards satu baris;
* chart utama dua kolom;
* sidebar terbuka.

## Tablet

* KPI cards dua atau tiga per baris;
* chart menjadi satu kolom jika sempit.

## Mobile

* satu kolom;
* sidebar collapsible;
* table dapat horizontal scroll;
* chart labels disederhanakan.

Prioritas utama tetap desktop karena dashboard kompetisi kemungkinan dinilai melalui layar laptop atau desktop.

---

# 28. Content and Terminology

Gunakan istilah Bahasa Indonesia yang konsisten.

| Raw term               | Display term                    |
| ---------------------- | ------------------------------- |
| Digital maturity       | Kematangan Digital              |
| Referral response time | Waktu Respons Rujukan           |
| Investment intensity   | Intensitas Investasi IT         |
| Conversion gap         | Kesenjangan Konversi Digital    |
| Operational burden     | Beban Operasional               |
| Double inefficiency    | Inefisiensi Ganda               |
| Priority score         | Skor Prioritas                  |
| Dominant bottleneck    | Hambatan Dominan                |
| Peer group             | Kelompok Pembanding             |
| Expected maturity      | Kematangan Digital Ekspektasian |
| Actual maturity        | Kematangan Digital Aktual       |

Jangan mengganti istilah pada halaman berbeda.

---

# 29. Acceptance Criteria

## 29.1 Functional

Dashboard dianggap selesai jika:

* seluruh enam halaman tersedia;
* filter global bekerja;
* state rumah sakit terpilih konsisten;
* KPI berubah sesuai filter;
* benchmark peer bekerja;
* priority table dapat diekspor;
* hospital explorer dapat dibuka dari halaman lain;
* methodology page menjelaskan seluruh skor;
* empty states tersedia;
* tidak ada retraining model saat reload.

---

## 29.2 Analytical

* formula KPI sesuai definisi;
* priority score konsisten;
* peer group fallback benar;
* model outputs berasal dari hasil precomputed;
* tidak ada klaim kausal;
* threshold terdokumentasi;
* denominator ditampilkan;
* missing values ditangani secara eksplisit.

---

## 29.3 Visual

* tidak ada halaman dengan lebih dari enam KPI card;
* satu halaman memiliki satu visual utama;
* chart tidak saling mengulang;
* semua metric memiliki unit;
* selected hospital terlihat jelas;
* warna status konsisten;
* semua tabel memiliki sort dan export;
* insight utama terlihat tanpa scroll berlebihan pada halaman ringkasan.

---

# 30. Implementation Priority

Kerjakan dalam urutan berikut.

## Phase 1: Foundation

1. Validasi dataset
2. Buat preprocessing pipeline
3. Buat derived metrics
4. Buat configuration constants
5. Buat global filter
6. Buat session state
7. Buat KPI card component

## Phase 2: Core Pages

1. Ringkasan Eksekutif
2. Kesiapan Digital & Investasi
3. Prioritas Intervensi
4. Eksplorasi Rumah Sakit

## Phase 3: Analytical Pages

1. Dampak terhadap Operasional
2. Metodologi & Kualitas Data
3. Model coefficient visual
4. Data quality visual

## Phase 4: Refinement

1. Responsive layout
2. Export
3. Error states
4. Tooltips
5. Accessibility
6. Tests
7. Performance optimization

---

# 31. Codex Execution Instructions


Sebelum menulis kode:

1. inspeksi struktur repository;
2. identifikasi nama kolom aktual;
3. baca file preprocessing dan notebook yang tersedia;
4. cari hasil model dan export yang sudah dibuat;
5. jangan mengubah formula analitik tanpa alasan;
6. jangan menduplikasi logic di file halaman;
7. pindahkan shared logic ke modules;
8. pertahankan kompatibilitas dengan struktur project yang ada.

Saat terdapat ketidaksesuaian antara dokumen ini dan dataset:

1. prioritaskan data contract aktual;
2. dokumentasikan mapping kolom;
3. pertahankan tujuan analitik;
4. hindari membuat data sintetis;
5. gunakan placeholder hanya untuk komponen yang belum memiliki output data.

Jangan:

* membuat fake historical delta;
* mengarang benchmark;
* menggunakan angka contoh sebagai data aktual;
* menampilkan model metric yang tidak tersedia;
* melakukan retraining model saat dashboard dibuka;
* menggunakan visual yang tidak memiliki fungsi keputusan;
* mengubah threshold tanpa mendokumentasikannya.

---

# 32. Definition of Done

Implementasi selesai ketika pengguna dapat melakukan alur berikut:

1. membuka Ringkasan Eksekutif;
2. melihat kondisi umum portofolio;
3. memfilter provinsi, kelas, dan ownership;
4. melihat perubahan KPI;
5. mengidentifikasi kelompok prioritas;
6. membuka halaman Prioritas Intervensi;
7. melihat rank, bottleneck, dan rekomendasi;
8. memilih satu rumah sakit;
9. membuka Eksplorasi Rumah Sakit;
10. membandingkan rumah sakit tersebut dengan peer;
11. memahami komponen priority score;
12. mengekspor hasil;
13. memverifikasi formula pada halaman Metodologi.

Dashboard harus membuat pengguna dapat berpindah dari:

```text
Masalah portofolio
```

menjadi:

```text
Rumah sakit prioritas
```

kemudian menjadi:

```text
Akar masalah
```

dan akhirnya:

```text
Intervensi serta KPI monitoring
```
