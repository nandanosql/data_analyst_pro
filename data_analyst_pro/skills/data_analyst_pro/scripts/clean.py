#!/usr/bin/env python3
"""
clean.py — Data Cleaning & Validation Utility
Detects and fixes data quality issues automatically.

Usage:
    python clean.py --input <file> [--output <file>] [--audit] [--report]
    python clean.py --input <file> --fix-types --drop-dupes --fill-nulls median
"""

import argparse
import sys
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


# ─── Quality Scoring ──────────────────────────────────────────────────────────

def calculate_quality_score(df: pd.DataFrame) -> dict:
    """Calculate a data quality score (0-100)."""
    total_cells = df.shape[0] * df.shape[1]
    if total_cells == 0:
        return {'score': 0, 'breakdown': {}}

    # Completeness (40 points) — % non-null
    completeness = (1 - df.isnull().sum().sum() / total_cells) * 40

    # Uniqueness (20 points) — no duplicate rows
    dup_pct = df.duplicated().mean()
    uniqueness = (1 - dup_pct) * 20

    # Consistency (20 points) — type uniformity per column
    consistency_scores = []
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if numeric strings are mixed with text
            try:
                numeric = pd.to_numeric(df[col], errors='coerce')
                non_null = df[col].notna().sum()
                if non_null > 0:
                    numeric_pct = numeric.notna().sum() / non_null
                    if 0.1 < numeric_pct < 0.9:
                        consistency_scores.append(0.5)  # Mixed types
                    else:
                        consistency_scores.append(1.0)
                else:
                    consistency_scores.append(1.0)
            except Exception:
                consistency_scores.append(1.0)
        else:
            consistency_scores.append(1.0)
    consistency = (sum(consistency_scores) / max(len(consistency_scores), 1)) * 20

    # Validity (20 points) — no outliers beyond extreme thresholds
    outlier_scores = []
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        s = df[col].dropna()
        if len(s) > 10:
            Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
            IQR = Q3 - Q1
            outlier_count = ((s < Q1 - 3 * IQR) | (s > Q3 + 3 * IQR)).sum()
            outlier_pct = outlier_count / len(s)
            outlier_scores.append(1 - min(outlier_pct * 10, 1))  # Penalize heavily
        else:
            outlier_scores.append(1.0)
    validity = (sum(outlier_scores) / max(len(outlier_scores), 1)) * 20 if outlier_scores else 20

    total = completeness + uniqueness + consistency + validity

    return {
        'score': round(total, 1),
        'breakdown': {
            'Completeness (40)': round(completeness, 1),
            'Uniqueness (20)': round(uniqueness, 1),
            'Consistency (20)': round(consistency, 1),
            'Validity (20)': round(validity, 1),
        }
    }


# ─── Audit Functions ──────────────────────────────────────────────────────────

def audit_data(df: pd.DataFrame, filepath: str) -> str:
    """Generate comprehensive data quality audit report."""
    lines = []
    lines.append(f"# Data Quality Audit Report\n")
    lines.append(f"**Source:** `{Path(filepath).name}`  ")
    lines.append(f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}  ")
    lines.append(f"**Records:** {len(df):,} rows × {len(df.columns)} columns\n")
    lines.append("---\n")

    # Quality Score
    quality = calculate_quality_score(df)
    score = quality['score']
    grade = '🟢 Excellent' if score >= 90 else '🟡 Good' if score >= 75 else '🟠 Fair' if score >= 60 else '🔴 Poor'

    lines.append(f"## Quality Score: {score}/100 — {grade}\n")
    lines.append("| Dimension | Score |")
    lines.append("|-----------|-------|")
    for dim, val in quality['breakdown'].items():
        bar = "█" * int(val) + "░" * (int(dim.split('(')[1].rstrip(')')) - int(val))
        lines.append(f"| {dim} | {val} {bar} |")
    lines.append("")

    # Row-Level Checks
    lines.append("## Row-Level Checks\n")
    lines.append(f"| Check | Count | % |")
    lines.append(f"|-------|-------|---|")
    lines.append(f"| Total rows | {len(df):,} | 100% |")
    lines.append(f"| Duplicate rows | {df.duplicated().sum():,} | {df.duplicated().mean()*100:.1f}% |")
    lines.append(f"| Rows with any null | {df.isnull().any(axis=1).sum():,} | {df.isnull().any(axis=1).mean()*100:.1f}% |")
    lines.append(f"| Complete rows | {df.dropna().shape[0]:,} | {(1-df.isnull().any(axis=1).mean())*100:.1f}% |")
    lines.append("")

    # Column-Level Checks
    lines.append("## Column-Level Checks\n")
    lines.append("| Column | Type | Non-Null | Nulls % | Unique | Min | Max | Issues |")
    lines.append("|--------|------|----------|---------|--------|-----|-----|--------|")

    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        null_pct = df[col].isnull().mean() * 100
        unique = df[col].nunique()

        issues = []
        if null_pct > 50:
            issues.append("⚠️ >50% null")
        elif null_pct > 20:
            issues.append("⚠️ >20% null")

        if unique == 1:
            issues.append("⚠️ Single value")
        if unique == len(df) and dtype == 'object':
            issues.append("Possibly ID")

        if df[col].dtype in ['int64', 'float64']:
            min_val = f"{df[col].min():,.2f}"
            max_val = f"{df[col].max():,.2f}"

            # Check outliers
            s = df[col].dropna()
            if len(s) > 10:
                Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((s < Q1 - 1.5 * IQR) | (s > Q3 + 1.5 * IQR)).sum()
                if outliers > 0:
                    issues.append(f"📊 {outliers} outliers")
        else:
            min_val = str(df[col].dropna().min())[:15] if non_null > 0 else "—"
            max_val = str(df[col].dropna().max())[:15] if non_null > 0 else "—"

        # Check whitespace issues in string columns
        if dtype == 'object':
            ws_count = df[col].dropna().apply(lambda x: str(x) != str(x).strip()).sum()
            if ws_count > 0:
                issues.append(f"✂️ {ws_count} whitespace")

        issue_str = ", ".join(issues) if issues else "✅"
        lines.append(f"| {col} | {dtype} | {non_null:,} | {null_pct:.1f}% | {unique:,} | {min_val} | {max_val} | {issue_str} |")

    lines.append("")

    # Outlier Details
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) > 0:
        lines.append("## Outlier Analysis (IQR Method)\n")
        lines.append("| Column | Q1 | Q3 | IQR | Lower | Upper | Outliers | % |")
        lines.append("|--------|----|----|-----|-------|-------|----------|---|")

        any_outliers = False
        for col in numeric_cols:
            s = df[col].dropna()
            if len(s) < 10:
                continue
            Q1 = s.quantile(0.25)
            Q3 = s.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outlier_count = ((s < lower) | (s > upper)).sum()
            if outlier_count > 0:
                any_outliers = True
                lines.append(
                    f"| {col} | {Q1:,.2f} | {Q3:,.2f} | {IQR:,.2f} "
                    f"| {lower:,.2f} | {upper:,.2f} "
                    f"| {outlier_count:,} | {outlier_count/len(s)*100:.1f}% |"
                )

        if not any_outliers:
            lines.append("✅ No significant outliers detected.\n")
        lines.append("")

    # Suggested Actions
    lines.append("## Suggested Actions\n")
    action_num = 1

    null_cols = df.isnull().sum()
    for col in null_cols[null_cols > 0].index:
        pct = null_cols[col] / len(df) * 100
        dtype = str(df[col].dtype)
        if pct > 50:
            lines.append(f"{action_num}. **Drop column `{col}`** — {pct:.1f}% missing values")
        elif dtype in ['int64', 'float64']:
            lines.append(f"{action_num}. **Fill `{col}` nulls with median** — {pct:.1f}% missing")
        else:
            lines.append(f"{action_num}. **Fill `{col}` nulls with mode or 'Unknown'** — {pct:.1f}% missing")
        action_num += 1

    if df.duplicated().sum() > 0:
        lines.append(f"{action_num}. **Remove {df.duplicated().sum():,} duplicate rows**")
        action_num += 1

    for col in df.select_dtypes('object').columns:
        ws = df[col].dropna().apply(lambda x: str(x) != str(x).strip()).sum()
        if ws > 0:
            lines.append(f"{action_num}. **Trim whitespace in `{col}`** — {ws} values affected")
            action_num += 1

    if action_num == 1:
        lines.append("✅ No immediate actions needed — data looks clean!\n")

    lines.append("")
    return "\n".join(lines)


# ─── Cleaning Functions ───────────────────────────────────────────────────────

def clean_data(df: pd.DataFrame, fix_types=False, drop_dupes=False,
               fill_nulls=None, trim_strings=True) -> tuple:
    """Clean data and return (cleaned_df, changes_log)."""
    changes = []
    original_rows = len(df)
    original_nulls = df.isnull().sum().sum()

    # 1. Trim whitespace in string columns
    if trim_strings:
        for col in df.select_dtypes('object').columns:
            trimmed = df[col].dropna().apply(lambda x: str(x) != str(x).strip()).sum()
            if trimmed > 0:
                df[col] = df[col].str.strip()
                changes.append(f"Trimmed whitespace in `{col}` ({trimmed} values)")

    # 2. Fix data types
    if fix_types:
        for col in df.select_dtypes('object').columns:
            # Try numeric
            numeric = pd.to_numeric(df[col], errors='coerce')
            if numeric.notna().sum() > df[col].notna().sum() * 0.8:
                df[col] = numeric
                changes.append(f"Converted `{col}` to numeric")
                continue

            # Try datetime
            try:
                dt = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
                if dt.notna().sum() > df[col].notna().sum() * 0.8:
                    df[col] = dt
                    changes.append(f"Converted `{col}` to datetime")
            except Exception:
                pass

    # 3. Drop duplicates
    if drop_dupes:
        dupes = df.duplicated().sum()
        if dupes > 0:
            df = df.drop_duplicates().reset_index(drop=True)
            changes.append(f"Removed {dupes:,} duplicate rows")

    # 4. Fill nulls
    if fill_nulls:
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count == 0:
                continue

            if fill_nulls == 'drop':
                df = df.dropna(subset=[col])
                changes.append(f"Dropped {null_count} rows with null `{col}`")
            elif fill_nulls == 'mean' and df[col].dtype in ['int64', 'float64']:
                fill_val = df[col].mean()
                df[col] = df[col].fillna(fill_val)
                changes.append(f"Filled `{col}` nulls with mean ({fill_val:.2f})")
            elif fill_nulls == 'median' and df[col].dtype in ['int64', 'float64']:
                fill_val = df[col].median()
                df[col] = df[col].fillna(fill_val)
                changes.append(f"Filled `{col}` nulls with median ({fill_val:.2f})")
            elif fill_nulls == 'mode':
                fill_val = df[col].mode()[0] if len(df[col].mode()) > 0 else None
                if fill_val is not None:
                    df[col] = df[col].fillna(fill_val)
                    changes.append(f"Filled `{col}` nulls with mode ({fill_val})")
            elif fill_nulls == 'forward':
                df[col] = df[col].ffill()
                changes.append(f"Forward-filled `{col}` nulls")
            elif fill_nulls == 'zero':
                df[col] = df[col].fillna(0)
                changes.append(f"Filled `{col}` nulls with 0")

    # Summary
    final_rows = len(df)
    final_nulls = df.isnull().sum().sum()

    if not changes:
        changes.append("No cleaning actions required — data was already clean")

    summary = {
        'rows_before': original_rows,
        'rows_after': final_rows,
        'rows_removed': original_rows - final_rows,
        'nulls_before': original_nulls,
        'nulls_after': final_nulls,
        'nulls_fixed': original_nulls - final_nulls,
        'changes': changes,
    }

    return df, summary


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="🧹 Data Cleaning & Validation — Detect and fix data quality issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Null Fill Strategies:
  mean      Fill with column mean (numeric only)
  median    Fill with column median (numeric only)
  mode      Fill with most frequent value
  forward   Forward fill (time-series)
  zero      Fill with 0
  drop      Drop rows with nulls

Examples:
  python clean.py --input data.csv --audit
  python clean.py --input data.csv --output clean.csv --drop-dupes --fill-nulls median
  python clean.py --input data.csv --output clean.csv --fix-types --audit --report
        """
    )
    parser.add_argument('--input', '-i', required=True, help='Input data file')
    parser.add_argument('--output', '-o', help='Save cleaned data to file')
    parser.add_argument('--audit', '-a', action='store_true', help='Generate data quality audit')
    parser.add_argument('--report', '-r', help='Save audit report to file (markdown)')
    parser.add_argument('--fix-types', action='store_true', help='Auto-fix column data types')
    parser.add_argument('--drop-dupes', action='store_true', help='Remove duplicate rows')
    parser.add_argument('--fill-nulls', choices=['mean', 'median', 'mode', 'forward', 'zero', 'drop'],
                        help='Strategy for filling null values')
    parser.add_argument('--no-trim', action='store_true', help='Skip whitespace trimming')

    args = parser.parse_args()

    df = load_data(args.input)
    print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns")

    # Audit
    if args.audit or args.report:
        audit = audit_data(df, args.input)
        if args.report:
            report_path = args.report
            Path(report_path).parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(audit)
            print(f"✓ Audit report saved → {report_path}")
        else:
            print("\n" + audit)

    # Clean
    do_clean = args.output or args.fix_types or args.drop_dupes or args.fill_nulls
    if do_clean:
        df_clean, summary = clean_data(
            df,
            fix_types=args.fix_types,
            drop_dupes=args.drop_dupes,
            fill_nulls=args.fill_nulls,
            trim_strings=not args.no_trim
        )

        print(f"\n── Cleaning Summary ──")
        print(f"  Rows: {summary['rows_before']:,} → {summary['rows_after']:,} ({summary['rows_removed']:,} removed)")
        print(f"  Nulls: {summary['nulls_before']:,} → {summary['nulls_after']:,} ({summary['nulls_fixed']:,} fixed)")
        print(f"  Changes:")
        for change in summary['changes']:
            print(f"    • {change}")

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            ext = out_path.suffix.lower()
            if ext == '.csv':
                df_clean.to_csv(args.output, index=False)
            elif ext in ('.xlsx', '.xls'):
                df_clean.to_excel(args.output, index=False)
            elif ext == '.json':
                df_clean.to_json(args.output, orient='records', indent=2)
            elif ext == '.parquet':
                df_clean.to_parquet(args.output, index=False)
            else:
                df_clean.to_csv(args.output, index=False)
            print(f"✓ Cleaned data saved → {args.output}")


if __name__ == '__main__':
    main()
