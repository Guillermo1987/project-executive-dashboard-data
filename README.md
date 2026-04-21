# Executive Dashboard 360° — Business Intelligence Portfolio

> **BI / RevOps Portfolio Project** · 24 KPIs · Finance · Marketing · Pipeline
> **Status:** Finished · Deployed to production (2026-04)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-%E2%86%92%20Open%20Dashboard-60a5fa?style=for-the-badge&logo=firebase&logoColor=white)](https://proyectos-personales.web.app/executive)
[![Portfolio](https://img.shields.io/badge/Portfolio-proyectos--personales.web.app-8b5cf6?style=for-the-badge&logo=firebase&logoColor=white)](https://proyectos-personales.web.app)
[![ETL Pipeline](https://img.shields.io/badge/Also%20See-Sales%20%26%20Weather%20ETL-f472b6?style=for-the-badge)](https://proyectos-personales.web.app)

---

## Project Status

| Phase | Status |
|---|---|
| KPI framework design (24 metrics) | Done |
| Data model (5 analytical tables × 36 months) | Done |
| Synthetic data generation | Done |
| React dashboard integration | Done |
| Firebase deployment | Done |

**Current phase:** maintenance — dashboard live and open for Power BI / Tableau reuse.

---

## What This Project Does

Defines, calculates and structures the 24 most critical executive KPIs for data-driven leadership decisions. Covers Finance, RevOps and Marketing in a single 360° view. The dataset drives a live React dashboard deployed on Firebase.

**Live dashboard → [proyectos-personales.web.app/executive](https://proyectos-personales.web.app/executive)**

---

## KPIs Included

| Category | KPI | Description |
|----------|-----|-------------|
| **Finance** | Revenue, MRR, ARR | Top-line growth |
| | Gross Margin %, EBITDA | Profitability & efficiency |
| **Retention** | Churn Rate, NRR | Customer health |
| | Expansion Revenue | Upsell / cross-sell |
| **RevOps** | CAC, LTV, LTV:CAC ratio | Unit economics |
| | Payback Period | CAC recovery time |
| | Win Rate, Sales Cycle | Sales efficiency |
| | Pipeline Value, Coverage | Pipeline health |
| **Marketing** | MQLs, SQLs, CPL, ROAS | Marketing funnel |

---

## Data Model

5 analytical tables, 36 months (2022–2024), all generated synthetically with realistic trends, seasonality and noise:

```
executive_summary.csv     36 rows  · 24 KPIs  (main executive view)
revenue_by_segment.csv   108 rows  · SMB / Mid-Market / Enterprise
revenue_by_channel.csv   144 rows  · Inbound / Outbound / Partners / Direct
marketing_funnel.csv      36 rows  · MQL→SQL→Won funnel + ROAS + CPL
pipeline_stages.csv      180 rows  · 5 stages × 36 months
```

---

## Skills Demonstrated

- **Business Intelligence:** Designing an interconnected KPI framework for executive decisions
- **Revenue Operations (RevOps):** Integrating Finance, Sales and Marketing into a single source of truth
- **Financial Analysis:** CAC, LTV, NRR, Gross Margin, EBITDA from first principles
- **Python / Pandas:** Synthetic data generation with trends, seasonality and gaussian noise
- **Data Storytelling:** Dashboard-ready structure for Power BI, Tableau or Looker

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data generation | Python 3.12, Pandas 2.2, NumPy |
| Web | React 19, Vite, Recharts — [proyectos-personales.web.app/executive](https://proyectos-personales.web.app/executive) |
| Hosting | Firebase Hosting (Spark plan) |

---

## How to Run

```bash
# Clone
git clone https://github.com/mindset-code/project-executive-dashboard-data.git
cd project-executive-dashboard-data

# Generate datasets
pip install pandas numpy
python generate_data.py
# Output: data/*.csv — ready for Power BI / Tableau
```

---

## Use in Power BI / Tableau

The CSV files in `data/` are ready to import directly. Join tables on the `month` field.

Recommended star schema:
- **Fact table:** `executive_summary.csv`
- **Dimension-fact tables:** `revenue_by_segment`, `revenue_by_channel`, `pipeline_stages`

---

## Links

- **Portfolio:** [proyectos-personales.web.app](https://proyectos-personales.web.app)
- **LinkedIn:** [Mindset & Code](https://www.linkedin.com/company/mindset-code/?locale=en_US)
- **Email:** contacto@mindset-code.com

---

*Built by [Mindset & Code](https://github.com/mindset-code) · Data & BI Analyst · MBA · ISC2 CC*
