<div align="center">

# 📊 Data Analyst Pro

**Turn raw data into actionable insights — fast.**

A production-ready skill package for AI coding agents that brings professional data analysis, visualization, cleaning, and reporting capabilities to your workflow.

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-brightgreen.svg)](https://opensource.org/licenses/MIT-0)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-%2311557c.svg)](https://matplotlib.org/)

[Features](#-features) · [Quick Start](#-quick-start) · [Scripts](#-scripts) · [Examples](#-examples) · [License](#-license)

</div>

---

## ✨ What This Does

**Data Analyst Pro** is a self-contained skill package that equips AI agents (Gemini, Copilot, Claude, etc.) with real, runnable scripts for:

- 📈 **Analyzing** any tabular dataset (CSV, Excel, JSON, Parquet)
- 🎨 **Visualizing** data with 10 chart types and premium dark 
- 🧹 **Cleaning** messy data with quality scoring and auto-fix
- 📋 **Generating** polished markdown reports with insights & recommendations
- 🗄️ **Querying** databases (SQLite, PostgreSQL, MySQL) from the terminal

> Unlike typical skills that provide stubs or code snippets, every script here is **fully functional** and **production-ready**.

---

## 🗂️ Project Structure

```
data-analyst-pro/
├── SKILL.md                        # Main instruction file (500+ lines)
├── TOOLS.md                        # Data source configuration
├── requirements.txt                # Python dependencies
│
├── scripts/
│   ├── analyze.py                  # 📊 Data analysis engine
│   ├── visualize.py                # 🎨 Chart generator (10 types)
│   ├── clean.py                    # 🧹 Data cleaning & validation
│   ├── report.py                   # 📋 Automated report builder
│   ├── data-init.sh                # ⚙️ Workspace setup
│   └── query.sh                    # 🗄️ SQL query runner
│
├── examples/
│   ├── sample_data.csv             # 99-row test dataset
│   └── sample_analysis.md          # Example output report
│
└── resources/
    ├── chart_templates.py          # Reusable chart library
    ├── report_template.md          # Jinja2 report template
    └── sql_patterns.md             # Advanced SQL reference
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or run the setup script:

```bash
bash scripts/data-init.sh
```

### 2. Analyze Data

```bash
python scripts/analyze.py --input your_data.csv --full
```

### 3. Generate Charts

```bash
python scripts/visualize.py --input your_data.csv --auto
```

### 4. Clean & Validate

```bash
python scripts/clean.py --input your_data.csv --audit
```

### 5. Build a Report

```bash
python scripts/report.py --input your_data.csv --title "Q1 Review" --charts
```

---

## 📦 Scripts

### `analyze.py` — Data Analysis Engine

Loads tabular data, auto-detects column types, and produces comprehensive statistics.

```bash
# Full analysis with correlations and outliers
python scripts/analyze.py --input data.csv --full

# Analyze specific columns and save report
python scripts/analyze.py --input data.csv --columns revenue,category --output report.md

# Get JSON summary for programmatic use
python scripts/analyze.py --input data.csv --json
```

**Features:**
| Capability | Details |
|---|---|
| **Auto Type Detection** | Numeric, categorical, datetime, boolean, ID-like |
| **Statistics** | Mean, median, std dev, skewness, quartiles |
| **Correlation** | Pearson matrix with notable correlation highlights |
| **Outlier Detection** | IQR-based with per-column breakdown |
| **Missing Values** | Analysis with suggested fill strategies |
| **Format Support** | CSV, Excel (.xlsx/.xls), JSON, Parquet, TSV |

---

### `visualize.py` — Chart Generator

Creates publication-quality charts with a premium dark theme.

```bash
# Auto-generate recommended charts
python scripts/visualize.py --input data.csv --auto

# Specific chart types
python scripts/visualize.py --input data.csv --type bar --x category --y revenue
python scripts/visualize.py --input data.csv --type scatter --x price --y sales --hue region
python scripts/visualize.py --input data.csv --type heatmap --output correlation.png
```

**Supported Charts:**

| Type | Use Case |
|------|----------|
| `line` | Trends over time |
| `bar` / `hbar` | Category comparisons |
| `scatter` | Correlations with trend line |
| `hist` | Distribution with mean/median markers |
| `box` | Spread & outlier detection |
| `heatmap` | Correlation matrix |
| `pie` | Proportions (donut style) |
| `violin` | Distribution shape by group |
| `pair` | Multi-variable overview |

---

### `clean.py` — Data Cleaning & Validation

Detects and fixes data quality issues automatically.

```bash
# Generate quality audit (score 0–100)
python scripts/clean.py --input data.csv --audit

# Clean and save
python scripts/clean.py --input data.csv --output clean.csv --drop-dupes --fill-nulls median

# Full pipeline
python scripts/clean.py --input data.csv --output clean.csv --fix-types --drop-dupes --fill-nulls median --audit --report audit.md
```

**Quality Score Breakdown:**

| Dimension | Weight | What It Checks |
|-----------|--------|----------------|
| Completeness | 40 pts | Null/missing values |
| Uniqueness | 20 pts | Duplicate rows |
| Consistency | 20 pts | Mixed types per column |
| Validity | 20 pts | Extreme outliers |

**Null Fill Strategies:** `mean` · `median` · `mode` · `forward` · `zero` · `drop`

---

### `report.py` — Automated Report Generator

Produces polished markdown reports with executive summaries, insights, and optional embedded charts.

```bash
# Basic report
python scripts/report.py --input data.csv --output reports/weekly.md

# Full report with charts
python scripts/report.py --input data.csv --output reports/q1.md --title "Q1 Sales Report" --charts
```

**Report Sections:**
- 📌 Executive Summary (auto-generated)
- 📊 Key Metrics Table
- 📈 Visualizations (optional)
- 🔍 Detailed Numeric & Categorical Analysis
- 💡 Auto-Generated Insights
- ✅ Actionable Recommendations
- 📐 Methodology & Appendix

---

### `query.sh` — SQL Query Runner

Execute SQL queries from the terminal against SQLite, PostgreSQL, or MySQL.

```bash
# SQLite
./scripts/query.sh "SELECT COUNT(*) FROM users"

# PostgreSQL
./scripts/query.sh --db postgresql --dbname analytics "SELECT * FROM users LIMIT 10"

# From file with CSV output
./scripts/query.sh --file queries/export.sql --output data/export.csv
```

---

## 📄 Examples

The `examples/` directory includes:

- **`sample_data.csv`** — 99-row dataset with dates, categories, products, regions, quantities, prices, and ratings
- **`sample_analysis.md`** — Complete analysis report generated from the sample data

Try it yourself:

```bash
python scripts/analyze.py --input examples/sample_data.csv --full --output my_report.md
```

---

## 🔗 Pipeline: Chain Scripts Together

The scripts are designed to be **modular** — chain them for a complete data workflow:

```
Raw Data → clean.py → analyze.py → visualize.py → report.py → Polished Report
```

```bash
# Step 1: Clean the data
python scripts/clean.py --input raw_data.csv --output data/clean.csv --fix-types --drop-dupes --fill-nulls median

# Step 2: Analyze
python scripts/analyze.py --input data/clean.csv --full --output output/analysis.md

# Step 3: Generate charts
python scripts/visualize.py --input data/clean.csv --auto --output-dir output/charts

# Step 4: Build final report
python scripts/report.py --input data/clean.csv --output reports/final_report.md --title "Monthly Report" --charts
```

---

## 📚 Resources

| File | Description |
|------|-------------|
| `resources/chart_templates.py` | Reusable chart functions with dark/light themes and 4 color palettes |
| `resources/report_template.md` | Jinja2 markdown template for custom report layouts |
| `resources/sql_patterns.md` | Advanced SQL reference — window functions, CTEs, pivots, JSON queries, performance tips |

---

## ⚙️ Requirements

| Package | Min Version | Purpose |
|---------|-------------|---------|
| Python | 3.9+ | Runtime |
| pandas | 2.0+ | Data manipulation |
| matplotlib | 3.7+ | Chart rendering |
| seaborn | 0.12+ | Statistical plots |
| scipy | 1.10+ | Statistical functions |
| numpy | 1.24+ | Numerical computing |
| openpyxl | 3.1+ | Excel file support |
| tabulate | 0.9+ | Markdown table formatting |
| Jinja2 | 3.1+ | Report templating |

---

## 📜 License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

<div align="center">

**Built by [Nandan Priyadarshi](https://github.com/nandanosql)**

Senior Product Manager @ Xiaomi · Data Strategy · 10+ Years in Data Engineering & Analytics

</div>
