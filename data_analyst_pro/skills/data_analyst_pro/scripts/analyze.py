#!/usr/bin/env python3
"""
analyze.py — Data Analysis Toolkit
Loads tabular data, auto-detects column types, and produces comprehensive statistics.

Usage:
    python analyze.py --input <file> [--full] [--columns col1,col2] [--output report.md]
"""

import argparse
import sys
import os
import json
from pathlib import Path

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


# ─── Constants ──────────────────────────────────────────────────────────────────

SUPPORTED_FORMATS = {'.csv', '.xlsx', '.xls', '.json', '.parquet', '.tsv'}

COLUMN_TYPE_MAP = {
    'numeric': ['int16', 'int32', 'int64', 'float16', 'float32', 'float64'],
    'categorical': ['object', 'category', 'bool'],
    'datetime': ['datetime64[ns]', 'datetime64[ns, UTC]'],
}


# ─── Data Loading ───────────────────────────────────────────────────────────────

def load_data(filepath: str, **kwargs) -> pd.DataFrame:
    """Load data from various file formats."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    ext = path.suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        print(f"ERROR: Unsupported format '{ext}'. Supported: {', '.join(SUPPORTED_FORMATS)}")
        sys.exit(1)

    loaders = {
        '.csv': lambda: pd.read_csv(filepath, **kwargs),
        '.tsv': lambda: pd.read_csv(filepath, sep='\t', **kwargs),
        '.xlsx': lambda: pd.read_excel(filepath, **kwargs),
        '.xls': lambda: pd.read_excel(filepath, **kwargs),
        '.json': lambda: pd.read_json(filepath, **kwargs),
        '.parquet': lambda: pd.read_parquet(filepath, **kwargs),
    }

    try:
        df = loaders[ext]()
        print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns from {path.name}")
        return df
    except Exception as e:
        print(f"ERROR loading {filepath}: {e}")
        sys.exit(1)


# ─── Type Detection ─────────────────────────────────────────────────────────────

def classify_columns(df: pd.DataFrame) -> dict:
    """Classify columns into numeric, categorical, datetime, and boolean types."""
    classification = {
        'numeric': [],
        'categorical': [],
        'datetime': [],
        'boolean': [],
        'id_like': [],
    }

    for col in df.columns:
        dtype = str(df[col].dtype)

        # Try to detect datetime columns stored as strings
        if dtype == 'object':
            try:
                pd.to_datetime(df[col].dropna().head(20))
                classification['datetime'].append(col)
                continue
            except (ValueError, TypeError):
                pass

        # Boolean detection
        if dtype == 'bool' or (dtype == 'object' and
            set(df[col].dropna().unique()) <= {'True', 'False', 'true', 'false', 'yes', 'no', '0', '1'}):
            classification['boolean'].append(col)
        # Numeric
        elif dtype in COLUMN_TYPE_MAP['numeric']:
            # Check if it's an ID column (high cardinality integers)
            if df[col].nunique() == len(df) and 'id' in col.lower():
                classification['id_like'].append(col)
            else:
                classification['numeric'].append(col)
        # Datetime
        elif 'datetime' in dtype:
            classification['datetime'].append(col)
        # Categorical
        else:
            if df[col].nunique() / max(len(df), 1) > 0.9 and len(df) > 50:
                classification['id_like'].append(col)
            else:
                classification['categorical'].append(col)

    return classification


# ─── Analysis Functions ─────────────────────────────────────────────────────────

def basic_overview(df: pd.DataFrame) -> str:
    """Generate basic overview of the dataset."""
    lines = []
    lines.append("## Dataset Overview\n")
    lines.append(f"| Property | Value |")
    lines.append(f"|----------|-------|")
    lines.append(f"| **Rows** | {len(df):,} |")
    lines.append(f"| **Columns** | {len(df.columns)} |")
    lines.append(f"| **Memory** | {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB |")
    lines.append(f"| **Duplicated Rows** | {df.duplicated().sum():,} ({df.duplicated().mean()*100:.1f}%) |")

    total_nulls = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    lines.append(f"| **Missing Values** | {total_nulls:,} ({total_nulls/max(total_cells,1)*100:.1f}%) |")
    lines.append("")

    return "\n".join(lines)


def column_summary(df: pd.DataFrame) -> str:
    """Generate column-level summary."""
    lines = []
    lines.append("## Column Summary\n")
    lines.append("| Column | Type | Non-Null | Nulls (%) | Unique | Sample Values |")
    lines.append("|--------|------|----------|-----------|--------|---------------|")

    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        null_pct = df[col].isnull().mean() * 100
        unique = df[col].nunique()
        samples = df[col].dropna().head(3).tolist()
        sample_str = ", ".join(str(s)[:20] for s in samples)
        lines.append(f"| {col} | {dtype} | {non_null:,} | {null_pct:.1f}% | {unique:,} | {sample_str} |")

    lines.append("")
    return "\n".join(lines)


def numeric_statistics(df: pd.DataFrame, columns: list) -> str:
    """Generate statistics for numeric columns."""
    if not columns:
        return ""

    lines = []
    lines.append("## Numeric Statistics\n")
    lines.append("| Column | Mean | Median | Std Dev | Min | 25% | 75% | Max | Skew |")
    lines.append("|--------|------|--------|---------|-----|-----|-----|-----|------|")

    for col in columns:
        s = df[col].dropna()
        if len(s) == 0:
            continue
        lines.append(
            f"| {col} "
            f"| {s.mean():,.2f} "
            f"| {s.median():,.2f} "
            f"| {s.std():,.2f} "
            f"| {s.min():,.2f} "
            f"| {s.quantile(0.25):,.2f} "
            f"| {s.quantile(0.75):,.2f} "
            f"| {s.max():,.2f} "
            f"| {s.skew():,.2f} |"
        )

    lines.append("")
    return "\n".join(lines)


def categorical_statistics(df: pd.DataFrame, columns: list, top_n: int = 10) -> str:
    """Generate statistics for categorical columns."""
    if not columns:
        return ""

    lines = []
    lines.append("## Categorical Analysis\n")

    for col in columns:
        vc = df[col].value_counts().head(top_n)
        total = len(df[col].dropna())
        lines.append(f"### {col}\n")
        lines.append(f"Unique values: **{df[col].nunique():,}** | Top {min(top_n, len(vc))} shown\n")
        lines.append("| Value | Count | Percentage |")
        lines.append("|-------|-------|------------|")

        for val, count in vc.items():
            pct = count / max(total, 1) * 100
            bar = "█" * int(pct / 2)
            lines.append(f"| {str(val)[:30]} | {count:,} | {pct:.1f}% {bar} |")

        lines.append("")

    return "\n".join(lines)


def datetime_statistics(df: pd.DataFrame, columns: list) -> str:
    """Generate statistics for datetime columns."""
    if not columns:
        return ""

    lines = []
    lines.append("## DateTime Analysis\n")

    for col in columns:
        try:
            s = pd.to_datetime(df[col], errors='coerce').dropna()
        except Exception:
            continue

        if len(s) == 0:
            continue

        span = s.max() - s.min()
        lines.append(f"### {col}\n")
        lines.append(f"| Property | Value |")
        lines.append(f"|----------|-------|")
        lines.append(f"| **Earliest** | {s.min()} |")
        lines.append(f"| **Latest** | {s.max()} |")
        lines.append(f"| **Span** | {span.days:,} days |")
        lines.append(f"| **Records** | {len(s):,} |")
        lines.append("")

    return "\n".join(lines)


def correlation_analysis(df: pd.DataFrame, columns: list) -> str:
    """Generate correlation matrix for numeric columns."""
    if len(columns) < 2:
        return ""

    lines = []
    lines.append("## Correlation Matrix\n")

    corr = df[columns].corr().round(3)

    # Header
    header = "| |" + "|".join(f" {c[:12]} " for c in corr.columns) + "|"
    sep = "|---|" + "|".join("---" for _ in corr.columns) + "|"
    lines.append(header)
    lines.append(sep)

    for idx, row in corr.iterrows():
        vals = "|".join(f" {v:+.3f} " if abs(v) >= 0.5 and idx != c else f" {v:.3f} "
                        for c, v in row.items())
        lines.append(f"| {str(idx)[:12]} |{vals}|")

    lines.append("")
    lines.append("*Strong correlations (|r| ≥ 0.5) shown with sign prefix*\n")

    # List notable correlations
    notable = []
    for i, c1 in enumerate(columns):
        for j, c2 in enumerate(columns):
            if i < j:
                r = corr.loc[c1, c2]
                if abs(r) >= 0.5:
                    strength = "Very strong" if abs(r) >= 0.8 else "Strong" if abs(r) >= 0.6 else "Moderate"
                    direction = "positive" if r > 0 else "negative"
                    notable.append(f"- **{c1}** ↔ **{c2}**: {r:+.3f} ({strength} {direction})")

    if notable:
        lines.append("### Notable Correlations\n")
        lines.extend(notable)
        lines.append("")

    return "\n".join(lines)


def missing_value_analysis(df: pd.DataFrame) -> str:
    """Analyze missing value patterns."""
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]

    if len(null_cols) == 0:
        return "## Missing Values\n\n✅ No missing values found.\n"

    lines = []
    lines.append("## Missing Values\n")
    lines.append("| Column | Missing | % Missing | Suggested Action |")
    lines.append("|--------|---------|-----------|------------------|")

    for col in null_cols.index:
        count = null_cols[col]
        pct = count / len(df) * 100
        dtype = str(df[col].dtype)

        if pct > 50:
            action = "⚠️ Consider dropping column"
        elif pct > 20:
            action = "Flag + investigate source"
        elif dtype in COLUMN_TYPE_MAP['numeric']:
            action = "Fill with median"
        else:
            action = "Fill with mode or 'Unknown'"

        lines.append(f"| {col} | {count:,} | {pct:.1f}% | {action} |")

    lines.append("")
    return "\n".join(lines)


def outlier_analysis(df: pd.DataFrame, columns: list) -> str:
    """Detect outliers using IQR method."""
    if not columns:
        return ""

    lines = []
    lines.append("## Outlier Detection (IQR Method)\n")
    lines.append("| Column | Lower Bound | Upper Bound | Outliers | % Outliers |")
    lines.append("|--------|-------------|-------------|----------|------------|")

    any_outliers = False
    for col in columns:
        s = df[col].dropna()
        Q1 = s.quantile(0.25)
        Q3 = s.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = ((s < lower) | (s > upper)).sum()
        pct = outliers / max(len(s), 1) * 100

        if outliers > 0:
            any_outliers = True
            lines.append(f"| {col} | {lower:,.2f} | {upper:,.2f} | {outliers:,} | {pct:.1f}% |")

    if not any_outliers:
        return "## Outlier Detection\n\n✅ No significant outliers detected (IQR method).\n"

    lines.append("")
    return "\n".join(lines)


# ─── Report Assembly ────────────────────────────────────────────────────────────

def generate_report(df: pd.DataFrame, filepath: str, full: bool = False,
                    selected_columns: list = None) -> str:
    """Generate complete analysis report."""
    if selected_columns:
        missing = [c for c in selected_columns if c not in df.columns]
        if missing:
            print(f"WARNING: Columns not found: {', '.join(missing)}")
        df = df[[c for c in selected_columns if c in df.columns]]

    types = classify_columns(df)

    sections = []
    sections.append(f"# Data Analysis Report\n")
    sections.append(f"**Source:** `{Path(filepath).name}`  ")
    sections.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}  ")
    sections.append(f"**Records:** {len(df):,} rows × {len(df.columns)} columns\n")
    sections.append("---\n")

    # Column classification
    sections.append("## Column Classification\n")
    for ctype, cols in types.items():
        if cols:
            sections.append(f"- **{ctype.title()}** ({len(cols)}): {', '.join(cols)}")
    sections.append("")

    # Basic overview
    sections.append(basic_overview(df))
    sections.append(column_summary(df))

    # Numeric analysis
    if types['numeric']:
        sections.append(numeric_statistics(df, types['numeric']))
        if full:
            sections.append(outlier_analysis(df, types['numeric']))

    # Categorical analysis
    if types['categorical']:
        sections.append(categorical_statistics(df, types['categorical']))

    # Datetime analysis
    if types['datetime']:
        sections.append(datetime_statistics(df, types['datetime']))

    # Correlation
    if full and len(types['numeric']) >= 2:
        sections.append(correlation_analysis(df, types['numeric']))

    # Missing values
    sections.append(missing_value_analysis(df))

    # Sample data
    sections.append("## Sample Data (First 5 Rows)\n")
    try:
        from tabulate import tabulate
        sections.append(tabulate(df.head(), headers='keys', tablefmt='github', showindex=False))
    except ImportError:
        sections.append(df.head().to_markdown(index=False))
    sections.append("")

    return "\n".join(sections)


# ─── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="📊 Data Analysis Toolkit — Analyze any tabular dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze.py --input data.csv
  python analyze.py --input data.xlsx --full
  python analyze.py --input data.csv --columns revenue,category --output report.md
        """
    )
    parser.add_argument('--input', '-i', required=True, help='Input data file (CSV, Excel, JSON, Parquet)')
    parser.add_argument('--output', '-o', help='Save report to file (markdown)')
    parser.add_argument('--full', '-f', action='store_true', help='Full analysis with correlations and outliers')
    parser.add_argument('--columns', '-c', help='Comma-separated list of columns to analyze')
    parser.add_argument('--json', action='store_true', help='Output summary as JSON')

    args = parser.parse_args()

    # Load
    df = load_data(args.input)

    # Parse columns
    selected = args.columns.split(',') if args.columns else None

    if args.json:
        types = classify_columns(df)
        summary = {
            'file': args.input,
            'rows': len(df),
            'columns': len(df.columns),
            'column_types': types,
            'missing_total': int(df.isnull().sum().sum()),
            'duplicates': int(df.duplicated().sum()),
            'numeric_summary': df.describe().to_dict() if types['numeric'] else {},
        }
        output = json.dumps(summary, indent=2, default=str)
    else:
        output = generate_report(df, args.input, full=args.full, selected_columns=selected)

    # Output
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✓ Report saved to {args.output}")
    else:
        print("\n" + output)


if __name__ == '__main__':
    main()
