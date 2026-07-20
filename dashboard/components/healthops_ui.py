"""Reusable Streamlit Custom Components v2 presentation layer."""

from __future__ import annotations

from typing import Any

import streamlit as st

COMPONENT_HTML = """
<div id="healthops-root" class="healthops-root"></div>
"""

COMPONENT_CSS = """
:host {
  display: block;
  color: var(--st-text-color, #212b32);
  font-family: var(--st-font, "Source Sans 3", Arial, sans-serif);
}

* { box-sizing: border-box; }
.healthops-root { display: block; min-width: 0; }

.page-hero {
  position: relative;
  padding: 0.25rem 0 1.35rem;
  border-bottom: 1px solid var(--st-border-color-light, #e8edee);
}

.page-hero::before {
  position: absolute;
  top: 0.25rem;
  bottom: 1.35rem;
  left: -1.25rem;
  width: 3px;
  content: "";
  background: var(--st-primary-color, #1f4f3f);
}

.hero-topline,
.context-strip,
.sidebar-brand,
.chart-heading,
.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.entity-header {
  position: relative;
  padding: 1rem 1.05rem;
  overflow: hidden;
  border: 1px solid var(--st-border-color, #d8dde0);
  border-radius: var(--st-base-radius, 6px);
  background:
    linear-gradient(100deg, var(--st-blue-background-color, #eff4f3), transparent 52%),
    var(--st-secondary-background-color, #fff);
}

.entity-header::after {
  position: absolute;
  top: 0;
  right: 0;
  width: 4rem;
  height: 4rem;
  content: "";
  border: solid var(--st-primary-color, #1f4f3f);
  border-width: 0 1px 1px 0;
  opacity: 0.12;
  transform: translate(1.5rem, -1.5rem) rotate(45deg);
}

.entity-topline {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.entity-title {
  margin: 0;
  color: var(--st-heading-color, #212b32);
  font-family: var(--st-heading-font, var(--st-font));
  font-size: clamp(1.2rem, 2vw, 1.5rem);
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.2;
}

.entity-id {
  flex: 0 0 auto;
  margin: 0.2rem 0 0;
  color: var(--st-primary-color, #1f4f3f);
  font-family: var(--st-code-font, monospace);
  font-size: 0.72rem;
  font-weight: 600;
}

.entity-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.38rem;
  margin-top: 0.7rem;
}

.entity-pill {
  display: inline-flex;
  align-items: center;
  min-height: 1.45rem;
  padding: 0.2rem 0.48rem;
  color: var(--st-gray-text-color, #4c6272);
  border: 1px solid var(--st-border-color, #d8dde0);
  border-radius: 999px;
  background: var(--st-secondary-background-color, #fff);
  font-size: 0.66rem;
  font-weight: 700;
  line-height: 1.25;
}

.entity-pill[data-tone="info"] {
  color: var(--st-blue-text-color, #2a6354);
  border-color: var(--st-blue-color, #1f4f3f);
  background: var(--st-blue-background-color, #eff4f3);
}

.entity-pill[data-tone="risk"] {
  color: var(--st-red-text-color, #a2191f);
  border-color: var(--st-red-color, #a2191f);
  background: var(--st-red-background-color, #fff1f1);
}

.entity-meta {
  margin: 0.72rem 0 0;
  color: var(--st-gray-text-color, #4c6272);
  font-size: 0.76rem;
  line-height: 1.45;
}

.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  min-height: 2rem;
  padding-top: 0.38rem;
  color: var(--st-gray-text-color, #4c6272);
  border-top: 1px solid var(--st-border-color-light, #e8edee);
  font-size: 0.7rem;
  line-height: 1.4;
}

.table-range {
  color: var(--st-text-color, #212b32);
  font-family: var(--st-code-font, monospace);
  font-weight: 600;
}

.table-hint { margin: 0; text-align: right; }

.eyebrow,
.context-kicker,
.brand-kicker,
.section-kicker {
  margin: 0;
  color: var(--st-primary-color, #1f4f3f);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  line-height: 1.2;
  text-transform: uppercase;
}

.eyebrow { color: var(--st-blue-text-color, #2a6354); }

.version-chip,
.context-count,
.status-chip {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  border: 1px solid var(--st-border-color, #d8dde0);
  border-radius: 999px;
  white-space: nowrap;
}

.version-chip {
  padding: 0.3rem 0.62rem;
  color: var(--st-gray-text-color, #4c6272);
  background: var(--st-secondary-background-color, #fff);
  font-family: var(--st-code-font, "IBM Plex Mono", monospace);
  font-size: 0.68rem;
}

.hero-title {
  max-width: 54rem;
  margin: 0.72rem 0 0;
  color: var(--st-heading-color, #212b32);
  font-family: var(--st-heading-font, var(--st-font));
  font-size: clamp(1.8rem, 3.1vw, 2.35rem);
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.08;
}

.hero-question {
  max-width: 62rem;
  margin: 0.6rem 0 0;
  color: var(--st-text-color, #212b32);
  font-size: 1.02rem;
  font-weight: 600;
  line-height: 1.45;
}

.hero-meta {
  margin: 0.62rem 0 0;
  color: var(--st-gray-text-color, #4c6272);
  font-size: 0.8rem;
  line-height: 1.45;
}

.context-strip {
  padding: 0.78rem 0.92rem;
  border: 1px solid var(--st-blue-color, #1f4f3f);
  border-left-width: 3px;
  border-radius: var(--st-base-radius, 6px);
  background: var(--st-blue-background-color, #eff4f3);
}

.context-copy { min-width: 0; }
.context-kicker {
  margin-bottom: 0.22rem;
  color: var(--st-blue-text-color, #2a6354);
  letter-spacing: 0.09em;
}

.context-summary {
  overflow: hidden;
  margin: 0;
  color: var(--st-text-color, #212b32);
  font-size: 0.86rem;
  font-weight: 600;
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.context-count {
  flex: 0 0 auto;
  padding: 0.34rem 0.66rem;
  color: var(--st-blue-text-color, #2a6354);
  border-color: var(--st-blue-color, #1f4f3f);
  background: var(--st-background-color, #f7f9fa);
  font-size: 0.76rem;
  font-weight: 700;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.8rem;
}

.kpi-card {
  position: relative;
  min-width: 0;
  min-height: 156px;
  padding: 1rem 1rem 0.9rem;
  overflow: hidden;
  border: 1px solid var(--st-border-color, #d8dde0);
  border-radius: var(--st-base-radius, 6px);
  background: var(--st-secondary-background-color, #fff);
}

.kpi-card:focus-visible {
  outline: 3px solid var(--st-focus-color, #ffdd00);
  outline-offset: 2px;
}

.kpi-card::before {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  height: 3px;
  content: "";
  background: var(--st-primary-color, #1f4f3f);
}

.kpi-card[data-tone="success"]::before { background: var(--st-green-color, #006747); }
.kpi-card[data-tone="watch"]::before { background: var(--st-orange-color, #b28600); }
.kpi-card[data-tone="risk"]::before { background: var(--st-red-color, #a2191f); }
.kpi-card[data-tone="neutral"]::before { background: var(--st-gray-color, #4c6272); }

.kpi-label {
  min-height: 2.25rem;
  margin: 0;
  color: var(--st-gray-text-color, #4c6272);
  font-size: 0.73rem;
  font-weight: 700;
  letter-spacing: 0.045em;
  line-height: 1.35;
  text-transform: uppercase;
}

.kpi-value {
  margin: 0.3rem 0 0;
  color: var(--st-heading-color, #212b32);
  font-family: var(--st-heading-font, var(--st-font));
  font-size: clamp(1.55rem, 2.35vw, 2.05rem);
  font-variant-numeric: tabular-nums;
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.08;
  overflow-wrap: anywhere;
}

.kpi-value.is-long {
  font-size: 1.08rem;
  letter-spacing: -0.018em;
  line-height: 1.2;
}

.kpi-comparison {
  min-height: 1.15rem;
  margin: 0.42rem 0 0;
  color: var(--st-gray-text-color, #4c6272);
  font-size: 0.76rem;
  line-height: 1.35;
}

.kpi-footer {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.35rem;
  margin-top: 0.72rem;
}

.status-chip {
  gap: 0.34rem;
  padding: 0.25rem 0.48rem;
  color: var(--st-blue-text-color, #2a6354);
  border-color: var(--st-blue-color, #1f4f3f);
  background: var(--st-blue-background-color, #eff4f3);
  font-size: 0.64rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  line-height: 1.2;
  text-transform: uppercase;
}

.status-chip::before {
  width: 0.38rem;
  height: 0.38rem;
  border-radius: 50%;
  content: "";
  background: currentcolor;
}

.status-chip[data-tone="success"] {
  color: var(--st-green-text-color, #006747);
  border-color: var(--st-green-color, #006747);
  background: var(--st-green-background-color, #eaf6ee);
}

.status-chip[data-tone="watch"] {
  color: var(--st-orange-text-color, #7a5b00);
  border-color: var(--st-orange-color, #b28600);
  background: var(--st-orange-background-color, #fff7e0);
}

.status-chip[data-tone="risk"] {
  color: var(--st-red-text-color, #a2191f);
  border-color: var(--st-red-color, #a2191f);
  background: var(--st-red-background-color, #fff1f1);
}

.status-chip[data-tone="neutral"] {
  color: var(--st-gray-text-color, #4c6272);
  border-color: var(--st-gray-color, #4c6272);
  background: var(--st-gray-background-color, #f2f4f5);
}

.kpi-denominator {
  min-width: 0;
  margin: 0;
  color: var(--st-gray-text-color, #4c6272);
  font-size: 0.68rem;
  line-height: 1.3;
  text-align: left;
}

.chart-heading { align-items: flex-start; padding: 0 0 0.65rem; }
.chart-copy { min-width: 0; }

.chart-title,
.section-title {
  margin: 0;
  color: var(--st-heading-color, #212b32);
  font-family: var(--st-heading-font, var(--st-font));
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -0.018em;
  line-height: 1.35;
}

.chart-subtitle,
.section-subtitle {
  max-width: 64rem;
  margin: 0.25rem 0 0;
  color: var(--st-gray-text-color, #4c6272);
  font-size: 0.76rem;
  line-height: 1.45;
}

.chart-index {
  flex: 0 0 auto;
  padding-top: 0.1rem;
  color: var(--st-primary-color, #1f4f3f);
  font-family: var(--st-code-font, monospace);
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.chart-insight {
  margin: 0;
  padding: 0.72rem 0 0.1rem;
  color: var(--st-text-color, #212b32);
  border-top: 1px solid var(--st-border-color-light, #e8edee);
  font-size: 0.78rem;
  font-weight: 500;
  line-height: 1.45;
}

.chart-insight::before {
  display: inline-block;
  width: 0.42rem;
  height: 0.42rem;
  margin-right: 0.48rem;
  border-radius: 50%;
  content: "";
  background: #9dc03f;
  transform: translateY(-0.04rem);
}

.sidebar-brand {
  justify-content: flex-start;
  padding: 0.85rem 0 1rem;
  border-bottom: 1px solid var(--st-border-color, #d8dde0);
}

.brand-mark {
  display: grid;
  flex: 0 0 auto;
  grid-template-columns: repeat(2, 0.46rem);
  grid-template-rows: repeat(2, 0.46rem);
  gap: 0.16rem;
  width: 1.4rem;
  height: 1.4rem;
  padding: 0.16rem;
  border-radius: var(--st-base-radius, 6px);
  background: var(--st-primary-color, #1f4f3f);
}

.brand-mark span { border-radius: 1px; background: var(--st-background-color, #fff); }
.brand-mark span:nth-child(2),
.brand-mark span:nth-child(3) { opacity: 0.64; }
.brand-copy { min-width: 0; }

.brand-name {
  margin: 0;
  color: var(--st-heading-color, #212b32);
  font-family: var(--st-heading-font, var(--st-font));
  font-size: 0.94rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.brand-kicker {
  margin-top: 0.22rem;
  color: var(--st-gray-text-color, #4c6272);
  font-size: 0.58rem;
  letter-spacing: 0.1em;
}

.section-heading {
  align-items: flex-end;
  padding: 0.25rem 0 0.48rem;
  border-bottom: 1px solid var(--st-border-color-light, #e8edee);
}

.section-title { font-size: 1.2rem; }
.section-kicker { flex: 0 0 auto; padding-bottom: 0.18rem; font-size: 0.63rem; }

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 991px) {
  .kpi-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

@media (max-width: 767px) {
  .page-hero::before { left: -0.75rem; }
  .hero-topline,
  .context-strip,
  .chart-heading,
  .section-heading {
    align-items: flex-start;
    flex-direction: column;
    gap: 0.55rem;
  }
  .context-summary { white-space: normal; }
  .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .kpi-card { min-height: 148px; }
}

@media (max-width: 480px) {
  .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 359px) {
  .kpi-grid { grid-template-columns: 1fr; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
"""

COMPONENT_JS = """
function element(tag, className, text) {
  const node = document.createElement(tag)
  if (className) node.className = className
  if (text !== undefined && text !== null) node.textContent = String(text)
  return node
}

function toneForStatus(status) {
  const tones = {
    "BAIK": "success",
    "STABIL": "info",
    "PERLU PERHATIAN": "watch",
    "PRIORITAS": "risk",
    "DATA TERBATAS": "neutral",
  }
  return tones[status] || "neutral"
}

function renderPageHeader(root, data) {
  const section = element("header", "page-hero")
  const top = element("div", "hero-topline")
  top.append(element("p", "eyebrow", data.eyebrow || "Decision intelligence"))
  top.append(element("span", "version-chip", data.data_version || "data-unversioned"))
  section.append(top)
  section.append(element("h1", "hero-title", data.title))
  section.append(element("p", "hero-question", data.question))
  section.append(element("p", "hero-meta", data.meta))
  root.append(section)
}

function renderContext(root, data) {
  const section = element("section", "context-strip")
  section.setAttribute("role", "status")
  section.setAttribute("aria-label", "Konteks filter aktif")
  const copy = element("div", "context-copy")
  copy.append(element("p", "context-kicker", "Filter aktif"))
  copy.append(element("p", "context-summary", data.summary))
  section.append(copy)
  section.append(element("span", "context-count", `${data.shown} / ${data.total} rumah sakit`))
  root.append(section)
}

function renderKpiGrid(root, data) {
  const region = element("section", "kpi-grid")
  region.setAttribute("aria-label", data.aria_label || "Indikator utama")
  for (const card of data.cards || []) {
    const article = element("article", "kpi-card")
    const tone = toneForStatus(card.status)
    article.dataset.tone = tone
    if (card.help_text) {
      article.title = card.help_text
      article.tabIndex = 0
    }
    article.append(element("p", "kpi-label", card.title))
    const value = element("p", "kpi-value", card.value)
    if (String(card.value || "").length > 20) value.classList.add("is-long")
    article.append(value)
    article.append(element("p", "kpi-comparison", card.comparison || ""))

    const footer = element("div", "kpi-footer")
    if (card.status) {
      const status = element("span", "status-chip", card.status)
      status.dataset.tone = tone
      footer.append(status)
    }
    footer.append(element("p", "kpi-denominator", card.denominator || ""))
    article.append(footer)
    if (card.help_text) article.append(element("span", "sr-only", `Definisi: ${card.help_text}`))
    region.append(article)
  }
  root.append(region)
}

function renderChartHeader(root, data) {
  const header = element("header", "chart-heading")
  const copy = element("div", "chart-copy")
  copy.append(element("h3", "chart-title", data.title))
  copy.append(element("p", "chart-subtitle", data.subtitle))
  header.append(copy)
  header.append(element("span", "chart-index", data.label || "ANALISIS"))
  root.append(header)
}

function renderChartInsight(root, data) {
  const insight = element("p", "chart-insight", data.insight)
  insight.setAttribute("role", "note")
  root.append(insight)
}

function renderSidebarBrand(root, data) {
  const brand = element("header", "sidebar-brand")
  brand.setAttribute("aria-label", "SYNAPSE HealthOps")
  const mark = element("span", "brand-mark")
  mark.setAttribute("aria-hidden", "true")
  for (let index = 0; index < 4; index += 1) mark.append(element("span"))
  const copy = element("div", "brand-copy")
  copy.append(element("p", "brand-name", "SYNAPSE HealthOps"))
  copy.append(element("p", "brand-kicker", `${data.total} RS · ${data.data_version}`))
  brand.append(mark, copy)
  root.append(brand)
}

function renderSectionHeader(root, data) {
  const header = element("header", "section-heading")
  const copy = element("div", "chart-copy")
  copy.append(element("h2", "section-title", data.title))
  if (data.subtitle) copy.append(element("p", "section-subtitle", data.subtitle))
  header.append(copy)
  if (data.kicker) header.append(element("span", "section-kicker", data.kicker))
  root.append(header)
}

function renderEntityHeader(root, data) {
  const article = element("article", "entity-header")
  const top = element("div", "entity-topline")
  top.append(element("h2", "entity-title", data.title))
  top.append(element("p", "entity-id", data.identifier))
  article.append(top)

  const pills = element("div", "entity-pills")
  pills.setAttribute("aria-label", "Atribut rumah sakit")
  for (const item of data.pills || []) {
    const pill = element("span", "entity-pill", item.label)
    pill.dataset.tone = item.tone || "neutral"
    pills.append(pill)
  }
  article.append(pills)
  article.append(element("p", "entity-meta", data.meta))
  root.append(article)
}

function renderTableFooter(root, data) {
  const footer = element("footer", "table-footer")
  footer.setAttribute("aria-label", "Ringkasan tabel")
  footer.append(
    element(
      "span",
      "table-range",
      `${data.start}–${data.end} / ${data.total} baris · halaman ${data.page} dari ${data.pages}`,
    ),
  )
  footer.append(
    element(
      "p",
      "table-hint",
      data.selectable ? "Pilih satu baris untuk membuka konteks rumah sakit." : "Tabel informasi.",
    ),
  )
  root.append(footer)
}

export default function(component) {
  const { data, parentElement } = component
  const root = parentElement.querySelector("#healthops-root")
  if (!root || !data) return
  root.replaceChildren()
  const renderers = {
    page_header: renderPageHeader,
    filter_context: renderContext,
    kpi_grid: renderKpiGrid,
    chart_header: renderChartHeader,
    chart_insight: renderChartInsight,
    sidebar_brand: renderSidebarBrand,
    section_header: renderSectionHeader,
    entity_header: renderEntityHeader,
    table_footer: renderTableFooter,
  }
  const renderer = renderers[data.variant]
  if (renderer) renderer(root, data)
}
"""

_HEALTHOPS_UI = st.components.v2.component(
    "synapse_healthops_ui",
    html=COMPONENT_HTML,
    css=COMPONENT_CSS,
    js=COMPONENT_JS,
)


def mount_healthops_ui(
    variant: str,
    payload: dict[str, Any],
    *,
    key: str,
) -> None:
    """Mount one display-only HealthOps surface with stable typed inputs."""
    _HEALTHOPS_UI(
        data={"variant": variant, **payload},
        key=key,
        width="stretch",
        height="content",
    )


def render_sidebar_brand(data_version: str, total: int) -> None:
    """Render the compact product lockup in the control rail."""
    mount_healthops_ui(
        "sidebar_brand",
        {"data_version": data_version, "total": total},
        key="healthops-sidebar-brand",
    )
