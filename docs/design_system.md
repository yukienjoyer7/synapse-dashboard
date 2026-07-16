# SYNAPSE HealthOps Design System

**Version:** 1.0  
**Product:** SYNAPSE 2026 Smart Hospital Analytics Dashboard  
**Primary platform:** Streamlit with Plotly or Altair  
**Primary users:** consortium executives, hospital operations managers, digital-transformation teams, and data analysts

---

## 1. System Definition

### 1.1 Name

**SYNAPSE HealthOps** is a professional healthcare analytics design system for comparing digital readiness, investment, and operational performance across a national portfolio of hospitals.

It is not designed to imitate a bedside monitor or an electronic medical record. It is an executive and analytical decision interface that must remain clinically credible, operationally useful, and visually restrained.

### 1.2 Hybrid design lineage

The system deliberately combines four design traditions:

| Source tradition | Adopted role in HealthOps |
|---|---|
| **NHS Design System and VA Design System** | Trustworthy healthcare shell, accessible content hierarchy, semantic states, forms, filters, and tables |
| **IBM Carbon Design System** | Data-visualization grammar, chart color discipline, density, annotations, and categorical palettes |
| **Oracle Health and GE HealthCare command-center patterns** | Operational prioritization, portfolio surveillance, target comparison, watchlists, and escalation queues |
| **MEDITECH Atrium and OpenMRS O3** | Dense hospital drilldown, workflow-oriented cards, compact clinical data presentation, and progressive disclosure |

### 1.3 Product character

The interface should feel:

- calm rather than dramatic
- clinical rather than corporate-marketing oriented
- analytical rather than decorative
- dense but not cramped
- authoritative without appearing infallible
- operationally urgent only when the data justifies urgency

### 1.4 Core design principles

1. **Decision first**  
   Every view must answer a management question or lead to a specific next action.

2. **Neutral by default**  
   Most of the interface uses white, ink, and cool gray. Strong color is earned by meaning.

3. **Color has one job at a time**  
   Interface color, data-series color, and risk color are separated. Red never acts as decoration.

4. **Comparison before isolation**  
   A hospital value should appear with a target, peer benchmark, historical context, or portfolio distribution.

5. **Progressive disclosure**  
   Portfolio signal first, hospital cause second, methodology and evidence third.

6. **Operational density with readable hierarchy**  
   Tables and compact cards are preferred over large ornamental visualizations.

7. **No unexplained authority**  
   Risk scores, thresholds, and model outputs must expose definitions, inputs, and limitations.

8. **Accessible without color**  
   Every status also uses text, icons, shape, line style, ordering, or annotation.

---

## 2. Information Architecture

### 2.1 Recommended navigation

Use a persistent left navigation or a compact top navigation with the following pages:

1. **Ringkasan Eksekutif**
2. **Kesiapan Digital**
3. **Dampak Operasional**
4. **Bottleneck & Inefisiensi Ganda**
5. **Eksplorasi Rumah Sakit**
6. **Rekomendasi Aksi**
7. **Metodologi & Kualitas Data**

The first four pages tell the competition narrative. The final three provide evidence, drilldown, and auditability.

### 2.2 Narrative sequence

The interface should preserve this analytical sequence:

```text
Portfolio condition
    -> inequality in digital readiness
    -> relationship between investment and maturity
    -> relationship between maturity and operations
    -> identification of double inefficiency
    -> prioritized hospital or cohort action
    -> evidence, assumptions, and data quality
```

Do not place all analyses on one scrolling page. A long single page weakens the decision hierarchy and makes cross-filter state difficult to understand.

### 2.3 Three disclosure levels

| Level | User question | Main interface pattern |
|---|---|---|
| **L1 Portfolio** | Where is attention required? | KPI strip, target-centered heatmap, ranking, map, watchlist |
| **L2 Cohort or hospital** | Which entities drive the signal and why? | filtered comparison, bullet charts, compact profile, contribution analysis |
| **L3 Evidence** | How was this calculated and how reliable is it? | metric definition, denominator, source, model note, data-quality flags |

---

## 3. Design Tokens

## 3.1 Color architecture

HealthOps uses four separate color layers:

1. **Foundation colors** for application structure
2. **Data colors** for measurement and comparison
3. **Semantic colors** for status and risk
4. **Program colors** for digital-transformation overlays

A color must not change meaning between pages.

### 3.2 Foundation colors

| Token | Hex | Use |
|---|---:|---|
| `--color-bg-canvas` | `#F7F9FA` | Application background |
| `--color-bg-surface` | `#FFFFFF` | Cards, panels, tables |
| `--color-bg-subtle` | `#F2F4F5` | Grouped filters, table headers, quiet sections |
| `--color-bg-selected` | `#EAF5FC` | Selected row, selected filter, active chart context |
| `--color-border-subtle` | `#D8DDE0` | Default borders and chart rules |
| `--color-border-strong` | `#AEB7BD` | Focused groups and table boundaries |
| `--color-text-primary` | `#212B32` | Main text and chart labels |
| `--color-text-secondary` | `#4C6272` | Descriptions and secondary labels |
| `--color-text-muted` | `#768692` | Metadata only, not body-sized essential text |
| `--color-primary` | `#005EB8` | Active navigation, primary action, selected series |
| `--color-primary-hover` | `#003087` | Hover, selected emphasis, active tab underline |
| `--color-focus` | `#FFDD00` | Keyboard focus ring only |

### 3.3 Program and capability colors

| Token | Hex | Meaning |
|---|---:|---|
| `--color-capability` | `#007D79` | Digital capability, infrastructure, interoperability |
| `--color-program` | `#6929C4` | RME, SATUSEHAT, IoT, telemedicine, transformation program overlay |
| `--color-information` | `#1192E8` | Informational callouts and neutral analytical emphasis |

Program purple must not be used for risk. Capability teal must not automatically mean success.

### 3.4 Semantic status colors

| Status | Foreground | Background | Border | Meaning |
|---|---:|---:|---:|---|
| **On target** | `#006747` | `#EAF6EE` | `#8BC7A6` | Within governed target or acceptable band |
| **Watch** | `#7A5B00` | `#FFF7E0` | `#D6B656` | Near threshold or deteriorating |
| **High risk** | `#A2191F` | `#FFF1F1` | `#F1A7AA` | Confirmed threshold breach or high-priority condition |
| **Critical** | `#750E13` | `#FDE7E9` | `#DA1E28` | Severe, immediate operational escalation only |
| **Information** | `#004B76` | `#EAF5FC` | `#8FCDEB` | Explanation, methodology, neutral notification |
| **Unknown** | `#4C6272` | `#F2F4F5` | `#AEB7BD` | Missing, unavailable, or not evaluated |

Rules:

- Never use amber text directly on white for small labels. Use the darker watch foreground or dark text on an amber-tinted background.
- Every status chip includes a written label.
- Critical red should be rare. If more than roughly 10 percent of visible elements are red, the page probably has poor prioritization.

### 3.5 Sequential palette for digital maturity

Use for digital maturity, system adoption, interoperability, IT staffing density, and similar capability variables.

| Step | Hex |
|---|---:|
| 1 | `#EAF5FC` |
| 2 | `#CDE6F7` |
| 3 | `#8FCDEB` |
| 4 | `#41B6E6` |
| 5 | `#005EB8` |
| 6 | `#003087` |

The highest value is darkest. This palette indicates magnitude, not moral success.

### 3.6 Target-centered palette for operational pressure

Use for BOR, LOS, referral response, queue pressure, and deviations from an accepted band.

| Position | Hex | Meaning |
|---|---:|---|
| Far below target | `#003A6D` | Material negative deviation below the center |
| Below target | `#1192E8` | Moderate negative deviation |
| Slightly below | `#CDE6F7` | Small negative deviation |
| Target band | `#E8EDEE` | Governed acceptable range |
| Slightly above | `#F6D68A` | Small positive pressure deviation |
| Above target | `#B28600` | Significant pressure |
| Severe breach | `#DA1E28` | High-risk pressure or severe deviation |

The midpoint must be a policy target, operational target band, or peer-adjusted benchmark. It must not silently default to the dataset mean.

### 3.7 Categorical palette

Use only when categories are nominal and not ordered.

```text
#005EB8  Trusted blue
#007D79  Teal
#6929C4  Purple
#1192E8  Cyan
#9F1853  Magenta
#198038  Green
#002D9C  Deep blue
#B28600  Ochre
```

Rules:

- Prefer direct labels over a detached legend.
- Use no more than six categories on a static competition screen.
- Use eight only in a filtered or interactive view.
- Ownership and hospital class should keep stable colors across the entire product.

### 3.8 Contrast requirements

Minimum requirements:

- Normal text: **4.5:1**
- Large text: **3:1**
- UI controls, chart marks, and focus indicators: **3:1**
- Primary ink on white: approximately **14.4:1**
- White on primary blue: approximately **6.4:1**
- White on capability teal: approximately **5.0:1**
- White on risk red: approximately **5.0:1**

Muted text must not be used for essential explanations at small sizes.

---

## 4. Typography

### 4.1 Font family

Use:

```css
font-family: "Source Sans 3", "Source Sans Pro", Arial, sans-serif;
```

Use `IBM Plex Mono`, `SFMono-Regular`, or `Consolas` only for hospital IDs, codes, model versions, and compact technical metadata.

Do not use a serif display font. Do not use condensed fonts for metric labels.

### 4.2 Type scale

| Token | Size | Line height | Weight | Use |
|---|---:|---:|---:|---|
| `display` | 32 px | 40 px | 700 | Page-level number or rare hero statement |
| `h1` | 28 px | 36 px | 700 | Page title |
| `h2` | 22 px | 30 px | 650 | Major section |
| `h3` | 18 px | 26 px | 650 | Card group or chart section |
| `title-sm` | 16 px | 22 px | 600 | Card and chart title |
| `body` | 15 px | 22 px | 400 | Default body copy |
| `body-sm` | 14 px | 20 px | 400 | Tables, filters, annotations |
| `label` | 13 px | 18 px | 600 | Control labels, KPI labels, chips |
| `caption` | 12 px | 16 px | 400 | Sources, update time, notes |
| `metric-xl` | 36 px | 40 px | 700 | Primary KPI value |
| `metric-lg` | 28 px | 34 px | 700 | Secondary KPI value |
| `metric-sm` | 20 px | 26 px | 700 | Dense comparison rows |

### 4.3 Numeric conventions

- Use tabular numerals where available.
- Right-align numeric table columns.
- Include units in labels, not repeated in every cell when the table heading already states the unit.
- Use a decimal comma or decimal point consistently across the entire dashboard. For Indonesian presentation, prefer locale-aware formatting.
- Avoid false precision. Percentages generally use zero or one decimal place.
- Large currency values use compact forms such as `Rp12,4 miliar`, with full values in tooltips.

---

## 5. Spacing, Shape, and Elevation

### 5.1 Spacing scale

Use an 8 px base with 4 px micro-spacing.

```text
4, 8, 12, 16, 24, 32, 40, 48, 64
```

Recommended defaults:

- control internal gap: 8 px
- card internal padding: 20 or 24 px
- compact table cell vertical padding: 8 px
- section gap: 32 px
- page top and bottom padding: 24 to 32 px

### 5.2 Radius

| Token | Value | Use |
|---|---:|---|
| `radius-sm` | 4 px | chips, small inputs |
| `radius-md` | 6 px | cards, dropdowns, tables |
| `radius-lg` | 8 px | modal or major container only |

Avoid highly rounded pill-shaped cards. Status chips may be pill-shaped, but general surfaces should remain structured.

### 5.3 Borders and shadows

Default card:

```css
border: 1px solid #D8DDE0;
box-shadow: 0 1px 2px rgba(33, 43, 50, 0.06);
```

Selected or focused card:

```css
border: 1px solid #005EB8;
box-shadow: 0 0 0 2px rgba(0, 94, 184, 0.12);
```

Do not use deep floating shadows. Dashboard hierarchy should come from spacing, border, and background, not simulated depth.

---

## 6. Layout System

### 6.1 Desktop grid

Use a 12-column grid.

| Property | Recommended value |
|---|---:|
| Maximum content width | 1600 px |
| Typical analytical width | fluid, 1180 to 1520 px |
| Outer margin | 24 to 40 px |
| Column gutter | 16 or 20 px |
| Sidebar width | 224 to 256 px |
| Sticky filter-bar height | 56 to 64 px |

### 6.2 Standard page anatomy

```text
Application header
Page title + decision statement + updated time
Sticky global filter bar
Primary KPI strip
Primary decision visualization
Supporting comparisons
Priority table or watchlist
Interpretation and recommended action
Method and data-quality footer
```

### 6.3 KPI strip

Use four to six cards. More than six weakens prioritization.

Recommended executive set:

1. Median digital maturity score
2. Percentage integrated with SATUSEHAT
3. Hospitals outside the BOR target band
4. Median referral response time
5. Double-inefficiency hospital count
6. Data completeness or coverage

Each KPI card must contain:

- metric label
- current value
- comparison or delta
- benchmark context
- status, only when governed
- tooltip with definition and denominator

### 6.4 Responsive behavior

This competition dashboard should be desktop-first, but must remain usable on narrower screens.

| Breakpoint | Behavior |
|---|---|
| `>= 1280 px` | Full 12-column layout and persistent navigation |
| `992 to 1279 px` | 8-column equivalent, smaller card groups, table remains primary |
| `768 to 991 px` | 4-column stacking, filters collapse into drawer |
| `< 768 px` | One-column view, no complex multi-panel comparison, simplified tables |

Do not force a 276-row analytical table into a card carousel on mobile.

---

## 7. Component Library

## 7.1 Application header

Contains:

- product name or competition title
- active portfolio context
- last refresh timestamp
- methodology or data-quality shortcut
- optional team identity, kept visually secondary

Use white background and a 1 px bottom border. Avoid a large blue banner that consumes analytical space.

## 7.2 Global filter bar

Recommended filters:

- period
- region or province
- hospital class
- ownership
- SATUSEHAT status
- RME status
- risk tier

Rules:

- Show active-filter count.
- Provide a visible **Reset filter** action.
- Persist filters across pages when the metric definitions remain compatible.
- Display the resulting hospital count, for example `87 dari 276 rumah sakit`.
- Filters must not silently change benchmark logic. State whether benchmarks are portfolio-wide or filter-relative.

## 7.3 KPI card

### Standard KPI

```text
Label
36 px value
Delta versus benchmark
One-line interpretation
```

### Target KPI

Adds a compact bullet bar with target band.

### Risk KPI

Uses a left status border and status label. Do not fill the entire card red.

Rules:

- Never use only an up or down arrow. State whether the direction is favorable.
- Avoid decorative icons unless the icon adds semantic meaning.
- No mini donut charts inside KPI cards.

## 7.4 Status chip

Structure:

```text
[icon or shape] Status label
```

Recommended labels:

- **Sesuai target**
- **Perlu dipantau**
- **Risiko tinggi**
- **Kritis**
- **Data belum lengkap**
- **Belum dinilai**

The chip must be text-readable in grayscale.

## 7.5 Chart container

Every chart container includes:

1. decision-oriented title
2. metric and time-basis subtitle
3. chart area
4. legend or direct labels
5. decision-oriented insight footer
6. source and update note, or a shared page-level provenance note
7. accessible data-table or export affordance

Layout rules:

- Align the title and subtitle with the chart's plotting frame, not the outer image edge.
- Provide 24 to 32 px of whitespace above the title block.
- Keep approximately 32 px between the subtitle and the plotting area; avoid oversized empty title bands.
- Keep the insight footer to one or two short sentences: finding first, decision implication or caveat second.
- Lead with a concrete value, comparison, cohort size, or governed threshold whenever one is available; avoid generic action copy that merely repeats the title.
- Present the footer sentence directly; do not prefix it with `Insight`, `Key insight`, or a decorative label.
- Leave 12 to 20 px below the insight footer; do not reserve a large empty bottom band.
- When every chart uses the same dataset and period, show provenance once at page or notebook level rather than repeating an identical source below every chart.
- Standalone image exports retain compact provenance metadata because they may leave the original page context.
- Embedded PNG fallbacks use a desktop analytical width of 1,400 px and preserve the interactive figure's configured height. Do not rely on Plotly's narrow 700 px static-image default.
- Static fallback sizing must not set the interactive layout width; interactive charts remain responsive to their notebook or application container.

Example:

```text
Rumah sakit dengan deviasi BOR tertinggi
Deviasi terhadap target operasional 60-85%, periode 2025
18 rumah sakit berada di atas batas atas target.
```

## 7.6 Bullet comparison row

Use for hospital actual versus benchmark.

Structure:

```text
Hospital label | target-band bar | actual marker | exact value | status
```

This component should replace gauge charts.

## 7.7 Hospital ranking row

Recommended columns:

- rank
- hospital name and class
- province or region
- digital maturity
- operational pressure score
- referral response
- double-inefficiency status
- trend sparkline
- detail action

Use in-cell bars for comparable numeric values. Use row color only for selection, not risk. Risk belongs in a status column.

## 7.8 Hospital profile header

Contains:

- hospital name
- hospital ID
- class and ownership
- region
- latest data period
- risk tier
- selected peer group

Below the header, show three domains:

1. **Digital capability**
2. **Operational performance**
3. **Investment and resources**

Do not merge all metrics into one opaque composite score without showing its dimensions.

## 7.9 Watchlist panel

A watchlist is preferable to a screen full of alerts.

Each item contains:

- hospital or cohort
- concise trigger
- duration or trend
- impact metric
- recommended investigation
- severity

Example:

```text
RS Kelas C Pemerintah, Jawa Timur
Waktu respons rujukan di atas peer median selama 3 periode.
Periksa kapasitas koordinasi rujukan dan integrasi sistem.
```

Only critical items should interrupt interaction.

## 7.10 Recommendation card

Structure:

- **Action**
- **Target cohort**
- **Evidence**
- **Expected operational effect**
- **Implementation priority**
- **Caveat or dependency**

Example:

```text
Prioritaskan penguatan staf integrasi, bukan penambahan perangkat.
Target: RS Kelas C pemerintah dengan belanja IT menengah tetapi maturitas rendah.
Evidence: staffing density is more consistently associated with maturity than device count in this cohort.
Priority: High.
Dependency: confirm local workflow and procurement constraints.
```

Recommendations must not look like automated clinical orders.

## 7.11 Data-quality callout

Use an information or watch treatment, not risk red unless data failure creates a severe decision hazard.

Required fields:

- affected metric
- missing or delayed proportion
- affected cohort
- likely impact on interpretation
- action taken in analysis

## 7.12 Method note

Use a compact expandable panel containing:

- definition
- numerator and denominator
- unit
- time basis
- source fields
- transformation
- benchmark rule
- model or statistical method
- limitations

This is mandatory for composite risk, double inefficiency, and modeled association views.

## 7.13 Empty, loading, and error states

### Empty state

State why no result exists and which filter caused it.

### Loading state

Use skeleton blocks or a compact spinner with the operation name. Avoid animated medical imagery.

### Error state

State what failed, what remains available, and whether the user can retry. Do not expose raw stack traces in the competition interface.

---

## 8. Visualization Grammar

## 8.1 General chart rules

- Begin axes at zero for bars unless a clearly annotated exception is analytically necessary.
- Lines may use a non-zero axis when variation would otherwise be unreadable, but the range must be explicit.
- Use light gridlines only where they support estimation.
- Use direct labels for one to three series.
- Use a legend for more complex category sets.
- Use tooltips for exact values, never as the only place where the core conclusion exists.
- Place the key conclusion in the title, subtitle, or annotation.
- Include denominators and sample size for filtered cohorts.
- Use target bands rather than single target lines when the operational definition is a range.
- Avoid dual axes except when one series is clearly secondary and the relationship cannot be represented more honestly another way.

## 8.2 Required chart mappings

| Analytical question | Primary chart | Secondary support |
|---|---|---|
| How unequal is digital maturity? | boxplot or strip plot by class and ownership | distribution table and cohort median |
| Does IT budget align with maturity? | scatterplot with trend and cohort encoding | quadrant summary |
| Does maturity align with better operations? | peer-adjusted scatterplot or coefficient plot | hospital-level comparison table |
| Which hospitals have double inefficiency? | target-centered heatmap and ranked dot plot | watchlist table |
| Where are geographic concentrations? | choropleth or symbol map linked to ranking | exact-value table |
| How far is each hospital from target? | bullet chart | compact sortable table |
| What contributes to a bottleneck? | Pareto, grouped horizontal bar, or contribution plot | evidence table |
| Which actions are highest priority? | impact-feasibility matrix or ranked action list | recommendation cards |

## 8.3 Ranked dot or lollipop plot

Use for 15 to 50 visible hospitals after filtering.

- Sort by the decision metric.
- Show a target line or peer median.
- Gray all entities except selected, watch, and high-risk entities.
- Provide a synchronized table for all 276 hospitals.

Do not use 276 vertical bars.

## 8.4 Scatterplot and quadrant

Use for investment-to-outcome or maturity-to-operation questions.

Recommended mapping:

- x-axis: digital maturity or IT investment
- y-axis: operational performance or risk
- size: hospital scale or referral volume
- color: selected risk tier or cohort, not a second continuous metric by default
- shape: optional RME or SATUSEHAT status

Required annotations:

- reference lines and their definitions
- filtered sample size
- regression or association note
- selected hospital label

Quadrant labels should be analytical, not moralized. Use:

- **High capability, lower pressure**
- **High capability, higher pressure**
- **Low capability, lower pressure**
- **Low capability, higher pressure**

The last quadrant represents double inefficiency only when the governed definition matches the axes and thresholds.

## 8.5 Heatmap

Use a target-centered heatmap for portfolio scanning.

Rows: hospitals or cohorts  
Columns: selected digital and operational dimensions

Rules:

- Separate capability columns from pressure columns with a divider.
- Do not apply one color scale to variables with different semantics.
- Use blue or teal sequential scales for capability.
- Use target-centered or risk scales for operational pressure.
- Support sorting by risk, class, ownership, or region.
- Show exact values in tooltip and selected-row detail.

## 8.6 Bullet chart

Use target bands:

```text
suboptimal range | acceptable target band | pressure range
                              ^ actual
```

Required labels:

- actual
- target band
- peer median
- unit

Use bullets for BOR, LOS, referral response, staffing, and maturity targets when thresholds are defensible.

## 8.7 Map

The map is a location context tool, not the main ranking mechanism.

Rules:

- Pair it with a linked ranked list.
- Encode one primary measure at a time.
- Use clear handling for provinces with different hospital counts.
- State whether values are counts, rates, medians, or weighted averages.
- Avoid red-green maps.
- Do not imply causality from geographic clustering.

## 8.8 Trend and sparkline

Use a full trend chart for causal or operational interpretation. Use a sparkline only as a compact scanning aid.

Full trend chart includes:

- target band
- period labels
- selected hospital and peer reference
- event annotations where justified
- missing-period indication

A sparkline must still include a directional cue or start/end value in its table row.

## 8.9 Tables

Tables are first-class analytical components.

Use:

- sticky headers
- sortable numeric columns
- compact 8 px vertical cell padding
- right-aligned numbers
- in-cell bars or sparklines
- persistent selected row
- column glossary
- export matching the current filter state

Do not use zebra striping and risk coloring simultaneously. Prefer subtle row dividers and selected-row highlighting.

---

## 9. Interaction Model

### 9.1 Cross-filtering

Clicking a chart mark may filter the page only when:

- the selected state is clearly visible
- the active filter appears in the filter bar
- there is an obvious reset action
- the result count updates

Hover alone must never change permanent state.

### 9.2 Drilldown

Recommended flow:

```text
Portfolio signal
-> filtered hospital ranking
-> selected hospital profile
-> metric evidence and recommended action
```

Preserve breadcrumb context such as:

```text
Indonesia / RS Kelas C / Pemerintah / Jawa Timur / RS selected
```

### 9.3 Tooltips

Every analytical tooltip should expose:

1. exact value
2. unit
3. benchmark or target
4. denominator or sample basis
5. last updated period
6. status definition, when relevant

Modeled results additionally expose:

- model type
- whether the output is descriptive, predictive, or inferential
- uncertainty or confidence interval where available

### 9.4 Selection behavior

Selected entity styling:

- primary blue outline or mark
- persistent label
- selected-row background
- all other points desaturated, not hidden by default

### 9.5 Export behavior

Exports must:

- preserve current filters
- include metric definitions or a metadata sheet/file
- include generation timestamp
- include data period
- not export hidden personally identifiable patient data

---

## 10. Content and Microcopy

### 10.1 Language style

Use professional Indonesian with short, explicit sentences.

Prefer:

- `18 rumah sakit berada di atas batas BOR.`
- `Hubungan ini bersifat asosiasi, bukan bukti kausal.`
- `Data SATUSEHAT belum lengkap untuk 7 rumah sakit.`

Avoid:

- `Performa sangat buruk!`
- `Rumah sakit gagal bertransformasi.`
- `AI menyimpulkan bahwa...`
- unexplained abbreviations or analytics jargon

### 10.2 Chart-title formula

Use:

```text
[Decision finding or question]
[Metric], [time basis], [comparison frame]
```

Examples:

```text
Kematangan digital belum merata pada RS Kelas C dan D
Distribusi skor menurut kelas rumah sakit, data 2025
```

```text
Belanja IT tinggi tidak selalu diikuti efisiensi operasional
Anggaran IT dibanding waktu respons rujukan, disesuaikan kelompok sebaya
```

### 10.3 Status microcopy

Status must state the trigger.

Weak:

```text
Risiko tinggi
```

Better:

```text
Risiko tinggi
BOR di atas batas target dan waktu respons rujukan memburuk.
```

### 10.4 Uncertainty language

Use:

- `berasosiasi dengan`
- `menunjukkan pola`
- `setelah penyesuaian terhadap...`
- `estimasi model`
- `interval kepercayaan`
- `belum cukup untuk menyimpulkan sebab-akibat`

Do not use `terbukti menyebabkan` unless the method genuinely supports causal inference.

---

## 11. Accessibility and Safety Rules

### 11.1 Non-negotiable accessibility

- keyboard-accessible controls
- visible focus indicator
- meaningful control labels
- no color-only status
- chart data available in a table or export
- sufficient contrast
- minimum touch target around 44 by 44 px where applicable
- screen-reader-friendly chart summaries where technically feasible
- no critical information available only on hover

### 11.2 Alert discipline

Use three escalation levels:

| Level | Interaction | Example |
|---|---|---|
| **Information** | passive callout | data refreshed, benchmark definition |
| **Watch** | visible in watchlist | worsening trend near threshold |
| **High risk or critical** | prioritized panel, optional interruption | severe multi-metric threshold breach |

Do not show toast notifications for ordinary analytical findings.

### 11.3 Model-output labeling

Every model-derived component must state one of:

- **Descriptive index**
- **Statistical association**
- **Predictive estimate**
- **Scenario estimate**

A predictive or inferential output must not be styled as a clinical recommendation.

### 11.4 Data provenance

Display:

- source dataset
- covered period
- refresh time
- affected hospital count
- data completeness
- transformation or imputation note

---

## 12. Page Specifications

## 12.1 Ringkasan Eksekutif

### Objective

Answer: **Where should consortium leadership focus first?**

### Layout

1. Decision statement
2. Five or six KPI cards
3. Portfolio target-centered heatmap
4. Geographic map and linked ranking
5. Priority watchlist
6. Three action recommendations

### Color balance

- 70 to 80 percent neutral
- 10 to 20 percent blue or teal
- less than 10 percent amber or red

## 12.2 Kesiapan Digital

### Objective

Answer: **How mature and unequal is digital readiness?**

### Core visuals

- boxplot or strip plot by hospital class
- ownership comparison
- IT budget versus maturity scatterplot
- RME, SATUSEHAT, IoT, and staffing capability matrix
- cohort ranking table

### Primary color logic

Blue and teal. Purple is limited to program-status overlays.

## 12.3 Dampak Operasional

### Objective

Answer: **Is digital capability associated with better operations?**

### Core visuals

- adjusted association or coefficient plot
- maturity versus referral-response scatterplot
- bullet charts for BOR and LOS
- peer-adjusted hospital table
- trend comparisons where time data exists

### Primary color logic

Neutral and blue for estimates. Use confidence intervals and target bands. Do not use green to imply causality.

## 12.4 Bottleneck & Inefisiensi Ganda

### Objective

Answer: **Which hospitals have low capability and high operational pressure, and what characterizes them?**

### Core visuals

- governed double-inefficiency quadrant
- ranked dot plot
- capability-pressure heatmap
- bottleneck contribution plot
- high-priority watchlist

### Primary color logic

Neutral page with amber and red reserved for governed risk tiers.

## 12.5 Eksplorasi Rumah Sakit

### Objective

Answer: **What is the complete, auditable profile of a selected hospital?**

### Layout

- search and filter
- hospital profile header
- three-domain KPI grid
- six to ten bullet comparisons
- trend strip
- peer table
- trigger history
- evidence and data-quality panels

This page may be denser than the executive pages.

## 12.6 Rekomendasi Aksi

### Objective

Answer: **What should be done, for whom, and why?**

### Core components

- ranked action list
- impact-feasibility matrix
- target cohort definition
- recommendation cards
- dependency and limitation notes

Avoid presenting generic recommendations that do not identify a cohort or evidence source.

## 12.7 Metodologi & Kualitas Data

### Objective

Answer: **Can the findings be trusted and reproduced?**

### Core components

- metric dictionary
- threshold definitions
- data coverage
- missingness and anomaly summary
- statistical-method cards
- model-governance note
- download section

This page is part of the product, not an appendix hidden from judges.

---

## 13. Streamlit Implementation Tokens

### 13.1 `.streamlit/config.toml`

```toml
[theme]
base = "light"
primaryColor = "#005EB8"
backgroundColor = "#F7F9FA"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#212B32"
font = "sans serif"

[browser]
gatherUsageStats = false
```

### 13.2 CSS token block

```css
:root {
  --color-bg-canvas: #F7F9FA;
  --color-bg-surface: #FFFFFF;
  --color-bg-subtle: #F2F4F5;
  --color-bg-selected: #EAF5FC;

  --color-border-subtle: #D8DDE0;
  --color-border-strong: #AEB7BD;

  --color-text-primary: #212B32;
  --color-text-secondary: #4C6272;
  --color-text-muted: #768692;

  --color-primary: #005EB8;
  --color-primary-hover: #003087;
  --color-capability: #007D79;
  --color-program: #6929C4;
  --color-information: #1192E8;

  --color-success: #006747;
  --color-watch: #B28600;
  --color-danger: #DA1E28;
  --color-critical: #750E13;
  --color-focus: #FFDD00;

  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 40px;
  --space-8: 48px;
}

html, body, [class*="css"] {
  font-family: "Source Sans 3", "Source Sans Pro", Arial, sans-serif;
  color: var(--color-text-primary);
}

[data-testid="stAppViewContainer"] {
  background: var(--color-bg-canvas);
}

.healthops-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  box-shadow: 0 1px 2px rgba(33, 43, 50, 0.06);
}

.healthops-card--selected {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(0, 94, 184, 0.12);
}

.healthops-section-title {
  margin: 0 0 var(--space-4) 0;
  font-size: 22px;
  line-height: 30px;
  font-weight: 650;
}

.healthops-caption {
  color: var(--color-text-secondary);
  font-size: 12px;
  line-height: 16px;
}
```

### 13.3 Plotly base template

```python
HEALTHOPS_COLORS = {
    "ink": "#212B32",
    "secondary": "#4C6272",
    "grid": "#D8DDE0",
    "surface": "#FFFFFF",
    "primary": "#005EB8",
    "primary_dark": "#003087",
    "teal": "#007D79",
    "purple": "#6929C4",
    "cyan": "#1192E8",
    "success": "#006747",
    "watch": "#B28600",
    "danger": "#DA1E28",
}

HEALTHOPS_CATEGORICAL = [
    "#005EB8", "#007D79", "#6929C4", "#1192E8",
    "#9F1853", "#198038", "#002D9C", "#B28600",
]

HEALTHOPS_MATURITY_SCALE = [
    [0.00, "#EAF5FC"],
    [0.20, "#CDE6F7"],
    [0.40, "#8FCDEB"],
    [0.60, "#41B6E6"],
    [0.80, "#005EB8"],
    [1.00, "#003087"],
]

HEALTHOPS_PRESSURE_SCALE = [
    [0.00, "#003A6D"],
    [0.17, "#1192E8"],
    [0.33, "#CDE6F7"],
    [0.50, "#E8EDEE"],
    [0.67, "#F6D68A"],
    [0.83, "#B28600"],
    [1.00, "#DA1E28"],
]

PLOTLY_LAYOUT = {
    "paper_bgcolor": "#FFFFFF",
    "plot_bgcolor": "#FFFFFF",
    "font": {
        "family": "Source Sans 3, Source Sans Pro, Arial, sans-serif",
        "color": "#212B32",
        "size": 13,
    },
    "title": {
        "font": {"size": 16, "color": "#212B32"},
        "x": 0,
        "xanchor": "left",
    },
    "margin": {"l": 48, "r": 24, "t": 56, "b": 48},
    "hoverlabel": {
        "bgcolor": "#FFFFFF",
        "bordercolor": "#AEB7BD",
        "font": {"color": "#212B32", "size": 13},
    },
    "xaxis": {
        "showgrid": False,
        "zeroline": False,
        "linecolor": "#AEB7BD",
        "tickfont": {"color": "#4C6272"},
        "title_font": {"color": "#4C6272"},
    },
    "yaxis": {
        "showgrid": True,
        "gridcolor": "#E8EDEE",
        "zeroline": False,
        "linecolor": "#AEB7BD",
        "tickfont": {"color": "#4C6272"},
        "title_font": {"color": "#4C6272"},
    },
    "colorway": HEALTHOPS_CATEGORICAL,
}
```

### 13.4 Streamlit implementation boundary

Recommended implementation split:

- **70 to 80 percent** native Streamlit layout and controls
- **15 to 25 percent** targeted CSS and controlled HTML wrappers
- **0 to 10 percent** custom components only where native behavior blocks an essential interaction

Do not rebuild the entire application in injected HTML. Preserve Streamlit state management, accessibility, and maintainability.

---

## 14. Do and Do Not

| Do | Do not |
|---|---|
| Use target bands and peer benchmarks | Show isolated metrics without context |
| Use a ranked dot plot and table | Use 276 bars in one chart |
| Reserve red for genuine high risk | Use red as a general brand accent |
| Use blue and teal for capability magnitude | Use green to imply all higher investment is good |
| Label modeled outputs explicitly | Present risk scores as objective clinical truth |
| Keep tables as first-class components | Hide exact values behind hover only |
| Use progressive disclosure | Put every metric on one screen |
| Pair map with ranking | Use a map as the only exact comparison tool |
| Use bullet charts | Use speedometer or gauge charts |
| Use short action-oriented titles | Use generic titles such as `Dashboard Overview` |
| Expose methodology and missingness | Hide data-quality limitations |
| Keep most surfaces neutral | Fill each card with a different saturated color |

---

## 15. Design Quality Checklist

### Foundation

- [ ] All colors use named semantic tokens.
- [ ] Red is used only for governed risk or severe deviation.
- [ ] Capability and risk palettes are not mixed.
- [ ] Essential text meets contrast requirements.
- [ ] Spacing follows the 4/8 px scale.

### Information architecture

- [ ] The first page identifies priority areas within 10 seconds.
- [ ] Every major analysis links to hospital or cohort drilldown.
- [ ] Methodology and data quality are accessible from every analytical page.
- [ ] Filter state is visible and reversible.

### KPI and charts

- [ ] Every KPI has a benchmark or comparison frame.
- [ ] Every chart title states the metric and decision context.
- [ ] Target-centered metrics use governed target bands.
- [ ] Chart tooltips include value, unit, benchmark, basis, and period.
- [ ] A table or export exists for key visualizations.
- [ ] No chart depends on red-green distinction alone.

### Tables and drilldown

- [ ] Numeric columns are right-aligned.
- [ ] Tables support sorting and selected-row persistence.
- [ ] Hospital profiles separate capability, operations, and investment.
- [ ] Composite metrics expose component definitions.

### Content and safety

- [ ] Association is not described as causation.
- [ ] Model-derived results are labeled.
- [ ] Recommendations identify a target cohort and evidence.
- [ ] Missingness and delayed data are visible.
- [ ] Alert severity is proportional and non-dramatic.

### Streamlit quality

- [ ] CSS selectors are isolated and documented.
- [ ] Dashboard remains usable if custom CSS partially fails.
- [ ] Native widgets retain keyboard focus and labels.
- [ ] Chart sizing works between 992 px and 1600 px widths.
- [ ] Exports preserve filter state and metadata.

---

## 16. Final Visual Direction

The finished dashboard should not look like a futuristic hospital control room. It should look like a credible health-system analytics product used to allocate attention and investment across 276 hospitals.

The visual signature is:

- white and cool-gray analytical surfaces
- NHS-style trusted blue for navigation and selection
- teal for digital capability
- purple for transformation-program overlays
- amber and red used narrowly for operational pressure
- compact Source Sans typography
- thin borders and minimal shadows
- strong tables, bullet charts, rankings, and target-centered heatmaps
- explicit benchmark, time, source, and uncertainty context

The system succeeds when a judge can quickly answer four questions:

1. **What is happening?**
2. **Where is it happening?**
3. **Why does it matter?**
4. **What action is supported by the evidence?**
