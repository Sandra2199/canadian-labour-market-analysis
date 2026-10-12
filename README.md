# Canadian Labour Market Analysis
### Provincial unemployment trends, 2021–2025

A reproducible analysis of annual unemployment rates across Canada's ten provinces, using Canada's published national rate as a benchmark.

**Author:** Sandra Quinones  
**Professional focus:** Business & Operations | Reporting & Data Analysis | Financial Operations

## Business questions

1. How did annual unemployment rates change across provinces from 2021 to 2025?
2. How did British Columbia compare with Canada's published rate each year?
3. Which provinces had the largest net increases or decreases over the period?

The project supports clear provincial comparisons and identifies patterns for further investigation. It demonstrates data quality controls, reproducible preparation, KPI calculations and reporting. It does not claim a workplace implementation or measured business impact.

## Key findings

- All ten provinces had lower rates in 2025 than in 2021. There were **no net provincial increases** over the selected period.
- Newfoundland and Labrador recorded the largest net decrease: **13.0% to 10.1%, or −2.9 percentage points (pp)**. It still had the highest provincial rate in 2025.
- British Columbia and Ontario tied for the smallest net decrease: **−0.4 pp each**.
- BC was below Canada's published rate in every year. Its gap ranged from **−0.9 pp to −0.2 pp**; in 2025, BC was **6.2%**, compared with **6.8%** for Canada, a **−0.6 pp** gap.
- Canada's rate moved from **7.5% in 2021 to 6.8% in 2025 (−0.7 pp)**.
- The net decrease does not imply continuous improvement: all provinces declined between 2021 and 2022, and all increased between 2023 and 2024.
- Saskatchewan had the lowest provincial rate in 2025, at **5.2%**.

### Provincial results

Rates are percentages; changes are percentage points. Sorted by net change, from largest to smallest decrease.

| Province | 2021 (%) | 2025 (%) | Net change (pp) |
|---|---:|---:|---:|
| Newfoundland and Labrador | 13.0 | 10.1 | −2.9 |
| New Brunswick | 9.3 | 7.1 | −2.2 |
| Nova Scotia | 8.6 | 6.6 | −2.0 |
| Prince Edward Island | 9.8 | 8.0 | −1.8 |
| Alberta | 8.6 | 7.2 | −1.4 |
| Saskatchewan | 6.5 | 5.2 | −1.3 |
| Manitoba | 6.5 | 5.9 | −0.6 |
| Quebec | 6.1 | 5.6 | −0.5 |
| British Columbia | 6.6 | 6.2 | −0.4 |
| Ontario | 8.1 | 7.7 | −0.4 |

The [full summary](outputs/tables/provincial_summary.csv) includes all five annual rates and provincial rankings. Rankings use published point estimates, with tied values sharing the minimum rank; they are not statistical significance claims.

## Visualizations

### Provincial trends

Ten small multiples share a 0–14% vertical scale for consistent comparisons. Endpoint labels show 2025 rates.

![Provincial unemployment trends](outputs/figures/provincial_unemployment_trends.png)

### British Columbia and Canada

Both series use the same zero-based scale. Canada is the published benchmark, not an average calculated from provincial rates.

![British Columbia versus Canada](outputs/figures/bc_vs_canada_unemployment.png)

### Net changes

Signed changes use 2025 minus 2021. Negative values indicate a net decrease; the zero reference is visible.

![Provincial net changes](outputs/figures/provincial_net_changes.png)

## Source and scope

**Statistics Canada, Table 14-10-0464-01:** [Labour force characteristics by province, territory and economic region, annual](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410046401). [DOI](https://doi.org/10.25318/1410046401-eng). Source survey: Labour Force Survey. The supplied export reports a release date of **January 9, 2026**.

- Metric: annual unemployment rate (%), as published.
- Period: 2021–2025.
- Geography: Canada and the ten provinces. Territories and economic regions are excluded.
- Canada's published estimates exclude the territories, as documented in source note 8.
- Source note 6 defines unemployment rate as unemployed persons as a percentage of the labour force. Rates are survey estimates rounded to the nearest tenth.
- Prince Edward Island is retained as a province even though it also constitutes one economic region (source note 7).

The [original CSV](data/raw/1410046401-eng.csv) is preserved byte-for-byte. This is an as-displayed export containing metadata and footnotes, not a database-style CSV. An `x` suppression occurs for Northeast, British Columbia in 2022, outside the selected scope. No selected rate is missing or suppressed. The export does not supply separate status, vector or geographic-code columns.

## Method and controls

The [notebook](notebooks/unemployment_analysis.ipynb) is the analytical source of truth:

1. Check the fixed source SHA-256, table identifier, title, frequency, release date, metric, unit and exact year header.
2. Read the geography block and select Canada plus the ten provinces by exact labels. Rename only `Canada 8` to `Canada` to remove its footnote marker.
3. Reshape to `year`, `geography`, `unemployment_rate`; retain the percentage scale (7.5 means 7.5%).
4. Require exactly **55 observations**, a complete 11 × 5 grid, unique geography-year keys, numeric rates, zero nulls and values between 0 and 100.
5. Calculate net changes, annual movements, BC's benchmark gaps and provincial rankings.
6. Export validated tables and charts, then compare saved tables with the calculations.

Violations raise explicit errors. No silent deduplication, coercion of unexpected symbols, imputation or interpolation is performed. The checksum intentionally blocks unreviewed source revisions.

**Formulas:** net change = rate in 2025 − rate in 2021; annual movement = current rate − previous-year rate; BC gap = BC rate − Canada's published rate. All differences are in **percentage points**, not percentage changes. In the annual-change table, 2021 has an intentionally blank change because 2020 is outside the scope.

A separate [verification script](scripts/verify_project.py) uses Python's standard library and exact decimal arithmetic to cross-check the processed observations against the raw export, and independently verify calculations and ranks.

## Reproduce the project

Use Python 3.11 or later; the delivered project was executed with Python 3.12. Run these commands from the project root:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install and run:

```bash
python -m pip install -r requirements.txt
python scripts/execute_notebook.py
python scripts/verify_project.py
```

The execution script runs every notebook code cell in order in a fresh Python process and saves outputs back into the notebook. It uses IPython in-process execution and does not require a kernel network socket. All tables and charts are regenerated locally; the raw input remains unchanged. No live API, credential or data download is needed.

Alternatively, open `notebooks/unemployment_analysis.ipynb` in an installed Jupyter or VS Code notebook interface and run all cells using the project environment. A notebook UI is optional and is not included in the minimal requirements.

## Project files

- [Executed notebook](notebooks/unemployment_analysis.ipynb)
- [Processed dataset](data/processed/provincial_unemployment_2021_2025.csv)
- [Provincial summary](outputs/tables/provincial_summary.csv)
- [BC–Canada comparison](outputs/tables/bc_canada_comparison.csv)
- [Annual movements](outputs/tables/annual_changes.csv)
- [Data quality report](outputs/tables/data_quality_report.json)
- [Verification record](VERIFICATION.md)
- [Execution script](scripts/execute_notebook.py)
- [Independent verification script](scripts/verify_project.py)
- [Dependencies](requirements.txt)

## Limitations and next steps

This is descriptive economic reporting. Rounded survey estimates carry sampling uncertainty; no confidence intervals, significance tests, causal analysis or forecasting are included. Small gaps should not be overinterpreted. Annual rates hide monthly changes and within-province differences; the fixed 2021 baseline affects the net-change comparison.

Unemployment rates alone do not establish overall labour-market health. Participation rates, employment rates, wages, hours and population composition are not analysed. The fixed export may differ from later revised estimates, and separate status metadata is not available in this file.

Further analysis could add published participation and employment rates, monthly trends and appropriate demographic or regional breakdowns. Review uncertainty before making inferential comparisons, and gather additional evidence before proposing causal explanations.

**Tools actually used:** Python, pandas, matplotlib, IPython and nbformat. SQL, Tableau, machine learning and forecasting were not used.
