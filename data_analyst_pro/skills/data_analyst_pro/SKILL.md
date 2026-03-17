---
name: data-analyst-pro
version: 1.0.0
description: "Advanced data analysis skill — SQL queries, spreadsheet automation, visualization, statistical analysis, data cleaning, and automated report generation. Fully functional scripts included."
author: Nandan Priyadarshi
license: MIT-0
dependencies:
  python: ">=3.9"
  packages: "see requirements.txt"
---

# Data Analyst Pro 📊🔬

**Transform your AI agent into a production-grade data analysis powerhouse.**

Analyze spreadsheets, query databases, generate visualizations, clean messy data, and produce executive-ready reports — all with fully functional scripts, not just code snippets.

---

## ✨ What Makes This Different

| Feature | Status |
|---------|--------|
| **6 runnable scripts** — not stubs, real tools | ✅ |
| **Auto-detect column types** and suggest analyses | ✅ |
| **Premium chart themes** with dark mode support | ✅ |
| **Data quality auditing** with actionable fix suggestions | ✅ |
| **Automated report generation** with embedded charts | ✅ |
| **Sample dataset** for immediate testing | ✅ |
| **Declared dependencies** via `requirements.txt` | ✅ |
| **Advanced SQL patterns** (CTEs, window funcs, pivots) | ✅ |

---

## Quick Start

### 1. Initialize Workspace
```bash
# On macOS/Linux
chmod +x scripts/data-init.sh
./scripts/data-init.sh

# On Windows (PowerShell)
pip install -r requirements.txt
mkdir -p data, output/charts, output/cleaned, reports, queries
```

### 2. Analyze Data
```bash
# Analyze a CSV file
python scripts/analyze.py --input data/sales.csv

# Analyze with full statistics
python scripts/analyze.py --input data/sales.csv --full

# Analyze the included sample data
python scripts/analyze.py --input examples/sample_data.csv
```

### 3. Visualize
```bash
# Auto-suggest charts
python scripts/visualize.py --input data/sales.csv --auto

# Specific chart
python scripts/visualize.py --input data/sales.csv --type bar --x category --y revenue

# Save to specific location
python scripts/visualize.py --input data/sales.csv --type line --x date --y revenue --output output/charts/trend.png
```

### 4. Clean Data
```bash
# Audit data quality
python scripts/clean.py --input data/messy.csv --audit

# Clean and save
python scripts/clean.py --input data/messy.csv --output output/cleaned/clean.csv

# Full clean with report
python scripts/clean.py --input data/messy.csv --output output/cleaned/clean.csv --audit --report
```

### 5. Generate Reports
```bash
# Generate analysis report
python scripts/report.py --input data/sales.csv --output reports/weekly-report.md

# Include charts
python scripts/report.py --input data/sales.csv --output reports/weekly-report.md --charts
```

---

## Scripts Reference

### `scripts/analyze.py` — Analysis Toolkit

The core analysis engine. Loads any tabular data, auto-detects types, and produces comprehensive statistics.

**Usage:**
```bash
python scripts/analyze.py --input <file> [--full] [--columns col1,col2] [--output report.md]
```

**Capabilities:**
- Load CSV, Excel (.xlsx/.xls), JSON, Parquet
- Auto-detect numeric, categorical, datetime, boolean columns
- Descriptive statistics (mean, median, mode, std, quartiles)
- Correlation matrix for numeric columns
- Value counts for categorical columns
- Time-series trend detection
- Missing value analysis
- Output as terminal table or markdown file

---

### `scripts/visualize.py` — Chart Generator

Creates publication-quality charts with a premium theme.

**Usage:**
```bash
python scripts/visualize.py --input <file> --type <chart_type> [--x col] [--y col] [--hue col] [--output path.png]
```

**Chart Types:**
| Type | Flag | Best For |
|------|------|----------|
| Line | `--type line` | Trends over time |
| Bar | `--type bar` | Category comparisons |
| Horizontal Bar | `--type hbar` | Rankings, many categories |
| Scatter | `--type scatter` | Correlations |
| Histogram | `--type hist` | Distributions |
| Box Plot | `--type box` | Spread & outliers |
| Heatmap | `--type heatmap` | Correlation matrices |
| Pie | `--type pie` | Proportions (≤6 slices) |
| Violin | `--type violin` | Distribution shape |
| Pair Plot | `--type pair` | Multi-variable overview |

**Auto Mode:**
```bash
python scripts/visualize.py --input data.csv --auto
```
Automatically suggests and generates the most useful charts based on data types.

---

### `scripts/clean.py` — Data Cleaning Utility

Detects and fixes data quality issues automatically.

**Usage:**
```bash
python scripts/clean.py --input <file> [--output <file>] [--audit] [--report] [--fix-types] [--drop-dupes] [--fill-nulls <strategy>]
```

**Null Fill Strategies:**
| Strategy | Description |
|----------|-------------|
| `mean` | Fill with column mean (numeric only) |
| `median` | Fill with column median (numeric only) |
| `mode` | Fill with most frequent value |
| `forward` | Forward fill (time-series) |
| `zero` | Fill with 0 |
| `drop` | Drop rows with nulls |

**Audit Output Includes:**
- Row count, duplicate count
- Per-column: type, nulls, unique values, min/max
- Outlier detection (IQR method)
- Data quality score (0-100)

---

### `scripts/report.py` — Report Generator

Produces polished markdown reports with insights and embedded charts.

**Usage:**
```bash
python scripts/report.py --input <file> [--output report.md] [--title "Report Name"] [--charts] [--template <path>]
```

---

### `scripts/query.sh` — SQL Query Runner

Execute SQL against databases directly from the terminal.

**Usage:**
```bash
# Inline query
./scripts/query.sh "SELECT COUNT(*) FROM users"

# From file
./scripts/query.sh --file queries/daily.sql

# Save output
./scripts/query.sh --file queries/export.sql --output data/export.csv

# Specify database
./scripts/query.sh --db postgresql --host localhost --dbname analytics "SELECT * FROM users LIMIT 10"
```

---

## Analysis Workflow

```
┌─────────────────┐
│  Define Question │
│  What are we     │
│  trying to       │
│  answer?         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Load & Inspect  │  ← analyze.py --input data.csv
│  Shape, types,   │
│  sample rows     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Clean & Prepare │  ← clean.py --input data.csv --audit
│  Nulls, dupes,   │
│  types, outliers │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Explore         │  ← analyze.py --input data.csv --full
│  Statistics,     │
│  correlations    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualize       │  ← visualize.py --input data.csv --auto
│  Charts, trends, │
│  distributions   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Report          │  ← report.py --input data.csv --charts
│  Insights,       │
│  recommendations │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deliver         │
│  Share findings  │
│  with stakeholders│
└─────────────────┘
```

---

## SQL Query Patterns

### Basic Exploration
```sql
-- Quick profile of any table
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT id) as unique_ids,
    MIN(created_at) as earliest,
    MAX(created_at) as latest
FROM table_name;

-- Column-level statistics
SELECT 
    column_name,
    COUNT(*) as count,
    COUNT(DISTINCT column_name) as unique_values,
    ROUND(COUNT(DISTINCT column_name) * 100.0 / COUNT(*), 2) as uniqueness_pct,
    SUM(CASE WHEN column_name IS NULL THEN 1 ELSE 0 END) as null_count
FROM table_name
GROUP BY column_name;
```

### Time-Series Analysis
```sql
-- Daily aggregation with running totals
SELECT 
    DATE(created_at) as date,
    COUNT(*) as daily_count,
    SUM(amount) as daily_total,
    SUM(SUM(amount)) OVER (ORDER BY DATE(created_at)) as running_total,
    AVG(SUM(amount)) OVER (
        ORDER BY DATE(created_at) 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as seven_day_avg
FROM transactions
GROUP BY DATE(created_at)
ORDER BY date;

-- Month-over-month growth
WITH monthly AS (
    SELECT 
        DATE_TRUNC('month', created_at) as month,
        COUNT(*) as count,
        SUM(amount) as total
    FROM transactions
    GROUP BY DATE_TRUNC('month', created_at)
)
SELECT 
    month,
    count,
    total,
    LAG(total) OVER (ORDER BY month) as prev_total,
    ROUND((total - LAG(total) OVER (ORDER BY month)) * 100.0 / 
        NULLIF(LAG(total) OVER (ORDER BY month), 0), 2) as growth_pct
FROM monthly
ORDER BY month;
```

### Window Functions
```sql
-- Rank within groups
SELECT 
    category,
    product_name,
    revenue,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as rank_in_category,
    ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) as pct_of_category
FROM products;

-- Cumulative distribution
SELECT 
    value,
    CUME_DIST() OVER (ORDER BY value) as cumulative_pct,
    NTILE(10) OVER (ORDER BY value) as decile
FROM metrics;
```

### Cohort Analysis
```sql
-- Retention cohorts
WITH cohorts AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', MIN(created_at)) as cohort_month
    FROM orders
    GROUP BY user_id
),
activity AS (
    SELECT 
        c.cohort_month,
        DATE_TRUNC('month', o.created_at) as activity_month,
        COUNT(DISTINCT o.user_id) as active_users
    FROM cohorts c
    JOIN orders o ON c.user_id = o.user_id
    GROUP BY c.cohort_month, DATE_TRUNC('month', o.created_at)
),
cohort_size AS (
    SELECT cohort_month, COUNT(*) as users
    FROM cohorts
    GROUP BY cohort_month
)
SELECT 
    a.cohort_month,
    a.activity_month,
    a.active_users,
    cs.users as cohort_size,
    ROUND(a.active_users * 100.0 / cs.users, 2) as retention_pct
FROM activity a
JOIN cohort_size cs ON a.cohort_month = cs.cohort_month
ORDER BY a.cohort_month, a.activity_month;
```

### Funnel Analysis
```sql
WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as step1_views,
        COUNT(DISTINCT CASE WHEN event = 'add_to_cart' THEN user_id END) as step2_cart,
        COUNT(DISTINCT CASE WHEN event = 'checkout' THEN user_id END) as step3_checkout,
        COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as step4_purchase
    FROM events
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT 
    step1_views as "Page Views",
    step2_cart as "Add to Cart",
    ROUND(step2_cart * 100.0 / NULLIF(step1_views, 0), 1) as "View→Cart %",
    step3_checkout as "Checkout",
    ROUND(step3_checkout * 100.0 / NULLIF(step2_cart, 0), 1) as "Cart→Checkout %",
    step4_purchase as "Purchase",
    ROUND(step4_purchase * 100.0 / NULLIF(step3_checkout, 0), 1) as "Checkout→Purchase %",
    ROUND(step4_purchase * 100.0 / NULLIF(step1_views, 0), 1) as "Overall Conversion %"
FROM funnel;
```

### Recursive CTEs
```sql
-- Generate date series (PostgreSQL)
WITH RECURSIVE dates AS (
    SELECT DATE '2024-01-01' as date
    UNION ALL
    SELECT date + INTERVAL '1 day'
    FROM dates
    WHERE date < DATE '2024-12-31'
)
SELECT 
    d.date,
    COALESCE(t.daily_total, 0) as total
FROM dates d
LEFT JOIN (
    SELECT DATE(created_at) as date, SUM(amount) as daily_total
    FROM transactions
    GROUP BY DATE(created_at)
) t ON d.date = t.date
ORDER BY d.date;

-- Organizational hierarchy
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 as depth, name::text as path
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, t.depth + 1, t.path || ' → ' || e.name
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree ORDER BY path;
```

---

## Data Cleaning Patterns

### Detection Checklist

| Check | SQL | Python |
|-------|-----|--------|
| Row count | `SELECT COUNT(*) FROM t` | `len(df)` |
| Duplicates | `GROUP BY ... HAVING COUNT(*) > 1` | `df.duplicated().sum()` |
| Nulls per column | `SUM(CASE WHEN col IS NULL ...)` | `df.isnull().sum()` |
| Unique values | `COUNT(DISTINCT col)` | `df['col'].nunique()` |
| Outliers (IQR) | See SQL patterns below | `clean.py --audit` |
| Type mismatches | `WHERE col !~ '^\d+$'` | `pd.to_numeric(df['col'], errors='coerce')` |

### Python Cleaning Patterns

```python
import pandas as pd

df = pd.read_csv('data.csv')

# ── Type Fixes ──────────────────────────────────
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['category'] = df['category'].astype('category')

# ── String Cleaning ─────────────────────────────
df['name'] = df['name'].str.strip().str.title()
df['email'] = df['email'].str.lower().str.strip()

# ── Deduplication ───────────────────────────────
df = df.drop_duplicates(subset=['email', 'date'], keep='last')

# ── Null Handling ───────────────────────────────
df['amount'] = df['amount'].fillna(df['amount'].median())
df['category'] = df['category'].fillna('Unknown')
df = df.dropna(subset=['email'])       # Required fields

# ── Outlier Capping (IQR) ──────────────────────
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
df['amount'] = df['amount'].clip(lower, upper)

# ── Validation ──────────────────────────────────
assert df['email'].str.contains('@').all(), "Invalid emails found"
assert df['amount'].ge(0).all(), "Negative amounts found"

# ── Export ──────────────────────────────────────
df.to_csv('cleaned_data.csv', index=False)
```

---

## Spreadsheet Analysis Patterns

### Loading Different Formats

```python
import pandas as pd

# CSV with options
df = pd.read_csv('data.csv', encoding='utf-8', parse_dates=['date_col'])

# Excel with specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sales', header=1)

# Multiple sheets
sheets = pd.read_excel('data.xlsx', sheet_name=None)  # dict of DataFrames

# JSON (nested)
df = pd.json_normalize(json_data, record_path='items', meta=['id', 'name'])

# Parquet (fast, columnar)
df = pd.read_parquet('data.parquet', columns=['id', 'amount', 'date'])
```

### Aggregation & Pivot Tables

```python
# Multi-level aggregation
summary = df.groupby(['region', 'category']).agg(
    total_revenue=('amount', 'sum'),
    avg_order=('amount', 'mean'),
    order_count=('amount', 'count'),
    unique_customers=('customer_id', 'nunique')
).round(2).reset_index()

# Pivot table
pivot = df.pivot_table(
    values='amount',
    index='month',
    columns='category',
    aggfunc='sum',
    fill_value=0,
    margins=True
)

# Cross-tabulation
cross = pd.crosstab(
    df['region'], df['status'],
    values=df['amount'], aggfunc='sum',
    normalize='index'  # Row percentages
).round(4) * 100
```

### Time-Series Operations

```python
# Set datetime index
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date').sort_index()

# Resample to different frequencies
weekly = df['amount'].resample('W').agg(['sum', 'mean', 'count'])
monthly = df['amount'].resample('M').sum()

# Rolling calculations
df['rolling_7d'] = df['amount'].rolling(7).mean()
df['rolling_30d'] = df['amount'].rolling(30).mean()
df['ewma'] = df['amount'].ewm(span=7).mean()

# Period-over-period comparison
df['pct_change'] = df['amount'].pct_change()
df['yoy_change'] = df['amount'].pct_change(periods=365)
```

---

## Visualization Guide

### Chart Selection Decision Tree

```
What are you showing?
│
├── Change over time?
│   ├── Few series (≤5) → Line Chart
│   ├── Many series → Area Chart (stacked)
│   └── Discrete periods → Bar Chart
│
├── Comparison?
│   ├── Few categories (≤8) → Vertical Bar
│   ├── Many categories → Horizontal Bar
│   └── Two variables → Grouped/Stacked Bar
│
├── Distribution?
│   ├── Single variable → Histogram
│   ├── Compare distributions → Box Plot / Violin
│   └── Density → KDE Plot
│
├── Relationship?
│   ├── Two variables → Scatter Plot
│   ├── Three variables → Bubble Chart
│   └── Many variables → Heatmap / Pair Plot
│
├── Composition?
│   ├── Static, ≤6 parts → Pie / Donut
│   ├── Over time → Stacked Area
│   └── Hierarchical → Treemap
│
└── Geographic?
    └── Map / Choropleth
```

### Quick Chart Examples

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Apply premium theme
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams.update({
    'figure.facecolor': '#0d1117',
    'axes.facecolor': '#161b22',
    'text.color': '#c9d1d9',
    'axes.labelcolor': '#c9d1d9',
    'xtick.color': '#8b949e',
    'ytick.color': '#8b949e',
    'axes.edgecolor': '#30363d',
    'grid.color': '#21262d',
    'font.family': 'sans-serif',
    'font.size': 11
})

COLORS = ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#bc8cff', '#79c0ff']

# ── Trend Line ─────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['date'], df['revenue'], color=COLORS[0], linewidth=2, marker='o', markersize=4)
ax.fill_between(df['date'], df['revenue'], alpha=0.1, color=COLORS[0])
ax.set_title('Revenue Trend', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Date')
ax.set_ylabel('Revenue ($)')
plt.tight_layout()
plt.savefig('trend.png', dpi=150, bbox_inches='tight')

# ── Comparison Bar ─────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df['category'], df['total'], color=COLORS[:len(df)], edgecolor='none', width=0.6)
for bar, val in zip(bars, df['total']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'${val:,.0f}', ha='center', va='bottom', fontsize=10, color='#c9d1d9')
ax.set_title('Revenue by Category', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('comparison.png', dpi=150, bbox_inches='tight')

# ── Distribution ───────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['amount'], bins=30, color=COLORS[0], edgecolor=COLORS[0], alpha=0.7)
ax.axvline(df['amount'].mean(), color=COLORS[3], linestyle='--', label=f"Mean: {df['amount'].mean():.0f}")
ax.axvline(df['amount'].median(), color=COLORS[1], linestyle='--', label=f"Median: {df['amount'].median():.0f}")
ax.legend()
ax.set_title('Amount Distribution', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('distribution.png', dpi=150, bbox_inches='tight')

# ── Correlation Heatmap ────────────────────────
fig, ax = plt.subplots(figsize=(10, 8))
corr = df.select_dtypes(include='number').corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax,
            linewidths=0.5, fmt='.2f', square=True)
ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('correlation.png', dpi=150, bbox_inches='tight')
```

---

## Statistical Analysis

### Descriptive Statistics Cheat Sheet

| Statistic | What It Tells You | When to Use | Python |
|-----------|-------------------|-------------|--------|
| **Mean** | Average value | Normal distributions | `df['col'].mean()` |
| **Median** | Middle value | Skewed data, outliers | `df['col'].median()` |
| **Mode** | Most common | Categorical data | `df['col'].mode()[0]` |
| **Std Dev** | Spread | Variability measurement | `df['col'].std()` |
| **Skewness** | Asymmetry | Distribution shape | `df['col'].skew()` |
| **Kurtosis** | Tail heaviness | Outlier propensity | `df['col'].kurtosis()` |
| **IQR** | Robust spread | Outlier detection | `df['col'].quantile(.75) - df['col'].quantile(.25)` |

### Hypothesis Testing Quick Reference

| Question | Test | Python | Assumptions |
|----------|------|--------|-------------|
| Are two means different? | t-test | `scipy.stats.ttest_ind(a, b)` | Normal, equal variance |
| Are 3+ means different? | ANOVA | `scipy.stats.f_oneway(a, b, c)` | Normal, equal variance |
| Are variables related? | Pearson r | `scipy.stats.pearsonr(x, y)` | Linear, normal |
| Non-normal correlation? | Spearman ρ | `scipy.stats.spearmanr(x, y)` | Monotonic |
| Categorical independence? | Chi-square | `scipy.stats.chi2_contingency(table)` | Expected freq ≥ 5 |
| Non-normal means? | Mann-Whitney | `scipy.stats.mannwhitneyu(a, b)` | Independent samples |

### Interpreting Results

```
p-value < 0.001  →  Very strong evidence against null hypothesis  ★★★
p-value < 0.01   →  Strong evidence                               ★★
p-value < 0.05   →  Moderate evidence                              ★
p-value ≥ 0.05   →  Weak/no evidence — fail to reject null         ✗

Correlation strength:
|r| = 0.00–0.19  →  Very weak
|r| = 0.20–0.39  →  Weak
|r| = 0.40–0.59  →  Moderate
|r| = 0.60–0.79  →  Strong
|r| = 0.80–1.00  →  Very strong
```

---

## Report Templates

### Executive Summary Report
```markdown
# [Report Title]
**Period:** [Start] – [End]  
**Generated:** [Date]  
**Prepared by:** [Name/Agent]

## Executive Summary
[2-3 sentences: What happened? What's the takeaway?]

## Key Metrics
| Metric | Current | Previous | Δ Change |
|--------|---------|----------|----------|
| Total Revenue | $X | $Y | +Z% |
| Orders | X | Y | +Z% |
| Avg Order Value | $X | $Y | +Z% |

## Key Findings
1. **[Finding]**: [Evidence with numbers]
2. **[Finding]**: [Evidence with numbers]
3. **[Finding]**: [Evidence with numbers]

## Recommendations
1. **[Action]**: [Expected impact]
2. **[Action]**: [Expected impact]

## Methodology
- **Source:** [Data source]
- **Period:** [Date range]  
- **Filters:** [Any filters applied]
- **Limitations:** [Known gaps]
```

---

## Data Storytelling Best Practices

### The SCQA Framework
1. **S**ituation — Set the context
2. **C**omplication — What changed or went wrong
3. **Q**uestion — What we need to figure out
4. **A**nswer — The insight and recommendation

### Example
> **Situation:** Monthly revenue has been growing 5% month-over-month.  
> **Complication:** March showed a 12% decline despite increased marketing spend.  
> **Question:** What caused the drop and how do we recover?  
> **Answer:** The decline is concentrated in the West region (−28%) due to a shipping delays. Recommend expediting West region fulfillment and offering affected customers 15% discount codes.

---

## Integration

### Compatible Data Sources
- **Databases:** SQLite, PostgreSQL, MySQL, MariaDB
- **Files:** CSV, Excel, JSON, Parquet, TSV
- **Warehouses:** BigQuery, Snowflake, Redshift
- **APIs:** Any REST/GraphQL endpoint that returns tabular data

### Project Structure
```
your-project/
├── SKILL.md              # This file
├── TOOLS.md              # Data source configuration
├── requirements.txt      # Python dependencies
├── scripts/
│   ├── data-init.sh      # Workspace setup
│   ├── query.sh          # SQL query runner
│   ├── analyze.py        # Analysis engine
│   ├── visualize.py      # Chart generator
│   ├── clean.py          # Data cleaning
│   └── report.py         # Report builder
├── examples/
│   ├── sample_data.csv   # Test dataset
│   └── sample_analysis.md# Example output
├── resources/
│   ├── chart_templates.py# Reusable chart functions
│   ├── report_template.md# Report template
│   └── sql_patterns.md   # Advanced SQL reference
├── data/                  # Your data files
├── output/
│   ├── charts/            # Generated charts
│   └── cleaned/           # Cleaned datasets
├── reports/               # Generated reports
└── queries/               # Saved SQL queries
```

---

## Best Practices

1. **Start with the question** — Don't explore aimlessly
2. **Validate first** — Run `clean.py --audit` before analysis
3. **Right chart for right data** — See the decision tree above
4. **Context > numbers** — Always compare against a baseline
5. **Lead with insight** — "Revenue dropped 12%" beats "Revenue was $45K"
6. **Document methodology** — Future you will thank present you
7. **Version your queries** — Save SQL in `queries/` directory

## Common Pitfalls

| ❌ Pitfall | ✅ Instead |
|-----------|-----------|
| Cherry-picking favorable data | Include all relevant data, note limitations |
| Correlation = causation | State correlations, investigate causality separately |
| Ignoring outliers | Investigate outliers before removing |
| Over-engineering | Start simple, add complexity only when needed |
| Presenting raw data | Synthesize into insights with recommendations |
| Forgetting the audience | Tailor detail level to stakeholders |

---

## License

**License:** MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

*"Without data, you're just another person with an opinion." — W. Edwards Deming*
