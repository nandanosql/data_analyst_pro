#!/usr/bin/env python3
"""
report.py — Automated Report Generator
Produces polished markdown reports with analysis and optional charts.

Usage:
    python report.py --input <file> [--output report.md] [--title "Report Name"] [--charts]
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


# ─── Data Loading ──────────────────────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load data from supported file formats."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    ext = path.suffix.lower()
    try:
        if ext == '.csv':
            return pd.read_csv(filepath)
        elif ext == '.tsv':
            return pd.read_csv(filepath, sep='\t')
        elif ext in ('.xlsx', '.xls'):
            return pd.read_excel(filepath)
        elif ext == '.json':
            return pd.read_json(filepath)
        elif ext == '.parquet':
            return pd.read_parquet(filepath)
        else:
            print(f"ERROR: Unsupported format: {ext}")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR loading file: {e}")
        sys.exit(1)


# ─── Analysis Helpers ──────────────────────────────────────────────────────────

def get_executive_summary(df: pd.DataFrame) -> str:
    """Generate an executive summary of the dataset."""
    numeric_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    parts = []
    parts.append(f"This dataset contains **{len(df):,} records** across **{len(df.columns)} columns**.")

    if len(numeric_cols) > 0:
        # Find the most significant numeric column (highest variance relative to mean)
        best_col = None
        best_cv = 0
        for col in numeric_cols:
            mean = df[col].mean()
            if mean != 0:
                cv = df[col].std() / abs(mean)
                if cv > best_cv:
                    best_cv = cv
                    best_col = col

        if best_col:
            total = df[best_col].sum()
            avg = df[best_col].mean()
            parts.append(
                f"The primary metric **{best_col}** totals **{total:,.2f}** "
                f"with an average of **{avg:,.2f}** per record."
            )

    if len(cat_cols) > 0:
        top_cat = cat_cols[0]
        top_val = df[top_cat].value_counts().index[0] if len(df[top_cat].value_counts()) > 0 else "N/A"
        parts.append(f"The most common **{top_cat}** is **{top_val}**.")

    null_pct = df.isnull().mean().mean() * 100
    if null_pct > 5:
        parts.append(f"Data quality note: **{null_pct:.1f}%** of values are missing.")
    elif null_pct > 0:
        parts.append(f"Data quality is good with only **{null_pct:.1f}%** missing values.")
    else:
        parts.append("Data quality is excellent with **no missing values**.")

    return " ".join(parts)


def get_key_metrics(df: pd.DataFrame) -> list:
    """Extract key metrics from the dataset."""
    metrics = []
    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols[:5]:  # Top 5 numeric columns
        s = df[col].dropna()
        if len(s) == 0:
            continue

        metrics.append({
            'name': col.replace('_', ' ').title(),
            'total': f"{s.sum():,.2f}",
            'average': f"{s.mean():,.2f}",
            'median': f"{s.median():,.2f}",
            'std_dev': f"{s.std():,.2f}",
        })

    return metrics


def get_insights(df: pd.DataFrame) -> list:
    """Generate automatic insights from the data."""
    insights = []
    numeric_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    # Insight 1: Distribution skewness
    for col in numeric_cols[:3]:
        skew = df[col].skew()
        if abs(skew) > 1:
            direction = "right-skewed (long tail of high values)" if skew > 0 else "left-skewed (long tail of low values)"
            insights.append({
                'title': f'{col.title()} Distribution',
                'detail': f'The distribution of `{col}` is significantly {direction} (skewness: {skew:.2f}). '
                         f'Consider using median ({df[col].median():,.2f}) instead of mean ({df[col].mean():,.2f}) for central tendency.'
            })

    # Insight 2: Top category dominance
    for col in cat_cols[:2]:
        vc = df[col].value_counts(normalize=True)
        if len(vc) > 1 and vc.iloc[0] > 0.4:
            insights.append({
                'title': f'{col.title()} Concentration',
                'detail': f'**{vc.index[0]}** dominates the `{col}` distribution at {vc.iloc[0]*100:.1f}%. '
                         f'The top 3 categories account for {vc.head(3).sum()*100:.1f}% of all records.'
            })

    # Insight 3: Correlations
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        np.fill_diagonal(corr.values, 0)
        max_corr_val = corr.abs().max().max()
        if max_corr_val > 0.5:
            idx = np.unravel_index(corr.abs().values.argmax(), corr.shape)
            col1, col2 = numeric_cols[idx[0]], numeric_cols[idx[1]]
            r = corr.iloc[idx[0], idx[1]]
            direction = "positive" if r > 0 else "negative"
            insights.append({
                'title': f'Strong Correlation Found',
                'detail': f'`{col1}` and `{col2}` show a strong {direction} correlation (r={r:.3f}). '
                         f'As `{col1}` increases, `{col2}` tends to {"increase" if r > 0 else "decrease"}.'
            })

    # Insight 4: Outliers
    for col in numeric_cols[:3]:
        s = df[col].dropna()
        if len(s) < 10:
            continue
        Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((s < Q1 - 1.5 * IQR) | (s > Q3 + 1.5 * IQR)).sum()
        if outliers > 0 and outliers / len(s) > 0.02:
            insights.append({
                'title': f'{col.title()} Outliers',
                'detail': f'`{col}` contains {outliers:,} outliers ({outliers/len(s)*100:.1f}% of data). '
                         f'Range: {s.min():,.2f} to {s.max():,.2f}, with most values between {Q1:,.2f} and {Q3:,.2f}.'
            })

    if not insights:
        insights.append({
            'title': 'Data Overview',
            'detail': 'The dataset appears well-distributed with no significant anomalies detected.'
        })

    return insights


def get_recommendations(df: pd.DataFrame) -> list:
    """Generate actionable recommendations."""
    recs = []

    # Missing data
    null_pct = df.isnull().mean()
    high_null_cols = null_pct[null_pct > 0.2].index.tolist()
    if high_null_cols:
        recs.append({
            'action': 'Address Missing Data',
            'detail': f'Columns with >20% missing values: {", ".join(high_null_cols)}. '
                     f'Investigate data collection processes and consider imputation strategies.'
        })

    # Duplicates
    dupes = df.duplicated().sum()
    if dupes > 0:
        recs.append({
            'action': 'Remove Duplicates',
            'detail': f'{dupes:,} duplicate rows detected ({dupes/len(df)*100:.1f}%). '
                     f'Review and deduplicate using: `python scripts/clean.py --input data.csv --drop-dupes`'
        })

    # High cardinality categoricals
    for col in df.select_dtypes('object').columns:
        if df[col].nunique() > 50:
            recs.append({
                'action': f'Bin/Group `{col}`',
                'detail': f'`{col}` has {df[col].nunique()} unique values — consider grouping into broader categories for analysis.'
            })

    # Visualization suggestions
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) >= 2:
        recs.append({
            'action': 'Generate Visualizations',
            'detail': f'Run `python scripts/visualize.py --input data.csv --auto` to auto-generate recommended charts.'
        })

    if not recs:
        recs.append({
            'action': 'Next Steps',
            'detail': 'Data is clean and ready for deeper analysis. Consider hypothesis testing or predictive modeling.'
        })

    return recs


# ─── Chart Generation ─────────────────────────────────────────────────────────

def generate_charts(df: pd.DataFrame, output_dir: Path) -> list:
    """Generate charts and return paths."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("WARNING: matplotlib/seaborn not available — skipping charts")
        return []

    # Apply dark theme
    plt.rcParams.update({
        'figure.facecolor': '#0d1117',
        'axes.facecolor': '#161b22',
        'text.color': '#e6edf3',
        'axes.labelcolor': '#e6edf3',
        'xtick.color': '#8b949e',
        'ytick.color': '#8b949e',
        'axes.edgecolor': '#30363d',
        'grid.color': '#21262d',
        'font.size': 11,
    })
    colors = ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#bc8cff', '#79c0ff']

    charts = []
    chart_dir = output_dir / 'charts'
    chart_dir.mkdir(parents=True, exist_ok=True)

    numeric_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns

    # 1. Distribution of primary numeric
    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(df[col].dropna(), bins=30, color=colors[0], edgecolor='#0d1117', alpha=0.8)
        ax.axvline(df[col].mean(), color=colors[3], linestyle='--', label=f'Mean: {df[col].mean():,.2f}')
        ax.axvline(df[col].median(), color=colors[1], linestyle='--', label=f'Median: {df[col].median():,.2f}')
        ax.legend()
        ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold', pad=10)
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        path = str(chart_dir / f'distribution_{col}.png')
        fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
        plt.close(fig)
        charts.append(path)

    # 2. Category bar chart
    if len(cat_cols) > 0 and len(numeric_cols) > 0:
        cat_col = cat_cols[0]
        num_col = numeric_cols[0]
        if df[cat_col].nunique() <= 12:
            fig, ax = plt.subplots(figsize=(10, 5))
            data = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False)
            bars = ax.bar(range(len(data)), data.values, color=colors[:len(data)], edgecolor='none')
            ax.set_xticks(range(len(data)))
            ax.set_xticklabels(data.index, rotation=45, ha='right')
            ax.set_title(f'{num_col} by {cat_col}', fontsize=14, fontweight='bold', pad=10)
            ax.set_ylabel(num_col)
            path = str(chart_dir / f'bar_{num_col}_by_{cat_col}.png')
            fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
            plt.close(fig)
            charts.append(path)

    # 3. Correlation heatmap
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax,
                    linewidths=0.5, fmt='.2f', square=True)
        ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold', pad=10)
        path = str(chart_dir / 'correlation_heatmap.png')
        fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
        plt.close(fig)
        charts.append(path)

    return charts


# ─── Report Assembly ──────────────────────────────────────────────────────────

def generate_report(df: pd.DataFrame, filepath: str, title: str = None,
                    include_charts: bool = False, output_dir: Path = None) -> str:
    """Generate complete analysis report."""
    now = datetime.now()
    report_title = title or f"Data Analysis Report — {Path(filepath).stem.replace('_', ' ').title()}"

    lines = []
    lines.append(f"# {report_title}\n")
    lines.append(f"**Period:** Full dataset  ")
    lines.append(f"**Generated:** {now.strftime('%B %d, %Y at %H:%M')}  ")
    lines.append(f"**Source:** `{Path(filepath).name}`  ")
    lines.append(f"**Records:** {len(df):,} rows × {len(df.columns)} columns\n")
    lines.append("---\n")

    # Executive Summary
    lines.append("## Executive Summary\n")
    lines.append(get_executive_summary(df))
    lines.append("")

    # Key Metrics
    metrics = get_key_metrics(df)
    if metrics:
        lines.append("## Key Metrics\n")
        lines.append("| Metric | Total | Average | Median | Std Dev |")
        lines.append("|--------|-------|---------|--------|---------|")
        for m in metrics:
            lines.append(f"| {m['name']} | {m['total']} | {m['average']} | {m['median']} | {m['std_dev']} |")
        lines.append("")

    # Charts
    if include_charts and output_dir:
        chart_paths = generate_charts(df, output_dir)
        if chart_paths:
            lines.append("## Visualizations\n")
            for path in chart_paths:
                chart_name = Path(path).stem.replace('_', ' ').title()
                lines.append(f"### {chart_name}\n")
                lines.append(f"![{chart_name}]({path})\n")

    # Detailed Analysis
    lines.append("## Detailed Analysis\n")

    # Numeric columns
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        lines.append("### Numeric Columns\n")
        lines.append("| Column | Mean | Median | Std Dev | Min | Max | Skew |")
        lines.append("|--------|------|--------|---------|-----|-----|------|")
        for col in numeric_cols:
            s = df[col].dropna()
            if len(s) == 0:
                continue
            lines.append(
                f"| {col} | {s.mean():,.2f} | {s.median():,.2f} | {s.std():,.2f} "
                f"| {s.min():,.2f} | {s.max():,.2f} | {s.skew():,.2f} |"
            )
        lines.append("")

    # Categorical columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        lines.append("### Categorical Columns\n")
        for col in cat_cols[:3]:
            vc = df[col].value_counts().head(8)
            lines.append(f"**{col}** ({df[col].nunique()} unique values)\n")
            lines.append("| Value | Count | % |")
            lines.append("|-------|-------|---|")
            for val, count in vc.items():
                pct = count / len(df) * 100
                lines.append(f"| {str(val)[:25]} | {count:,} | {pct:.1f}% |")
            lines.append("")

    # Insights
    insights = get_insights(df)
    lines.append("## Insights\n")
    for i, insight in enumerate(insights, 1):
        lines.append(f"{i}. **{insight['title']}**: {insight['detail']}\n")

    # Recommendations
    recs = get_recommendations(df)
    lines.append("## Recommendations\n")
    for i, rec in enumerate(recs, 1):
        lines.append(f"{i}. **{rec['action']}**: {rec['detail']}\n")

    # Methodology
    lines.append("## Methodology\n")
    lines.append(f"- **Data source:** `{Path(filepath).name}`")
    lines.append(f"- **Total records:** {len(df):,}")
    lines.append(f"- **Analysis date:** {now.strftime('%Y-%m-%d')}")
    lines.append(f"- **Missing values:** {df.isnull().sum().sum():,} ({df.isnull().mean().mean()*100:.1f}%)")
    lines.append(f"- **Duplicate rows:** {df.duplicated().sum():,}")
    lines.append(f"- **Tools used:** pandas {pd.__version__}, numpy {np.__version__}")
    lines.append("")

    # Sample Data
    lines.append("## Appendix: Sample Data\n")
    try:
        from tabulate import tabulate
        lines.append(tabulate(df.head(10), headers='keys', tablefmt='github', showindex=False))
    except ImportError:
        lines.append(df.head(10).to_markdown(index=False))
    lines.append("")

    return "\n".join(lines)


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="📋 Report Generator — Produce polished analysis reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python report.py --input data.csv --output reports/weekly.md
  python report.py --input data.csv --output reports/sales.md --title "Sales Report Q1" --charts
        """
    )
    parser.add_argument('--input', '-i', required=True, help='Input data file')
    parser.add_argument('--output', '-o', default=None, help='Output report file (markdown)')
    parser.add_argument('--title', help='Report title')
    parser.add_argument('--charts', action='store_true', help='Generate and embed charts')
    parser.add_argument('--template', help='Custom report template (Jinja2 markdown)')

    args = parser.parse_args()

    df = load_data(args.input)
    print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns")

    output_path = args.output or f"reports/report_{Path(args.input).stem}_{datetime.now().strftime('%Y%m%d')}.md"
    output_dir = Path(output_path).parent

    report = generate_report(
        df, args.input,
        title=args.title,
        include_charts=args.charts,
        output_dir=output_dir
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Report generated → {output_path}")

    if args.charts:
        print(f"✓ Charts saved → {output_dir / 'charts'}/")


if __name__ == '__main__':
    main()
