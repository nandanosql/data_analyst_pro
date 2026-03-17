#!/usr/bin/env python3
"""
visualize.py — Chart Generator
Creates publication-quality charts with a premium dark theme.

Usage:
    python visualize.py --input <file> --type <chart_type> [--x col] [--y col] [--output path.png]
    python visualize.py --input <file> --auto
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
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import seaborn as sns
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


# ─── Premium Dark Theme ────────────────────────────────────────────────────────

THEME = {
    'bg_primary': '#0d1117',
    'bg_secondary': '#161b22',
    'text_primary': '#e6edf3',
    'text_secondary': '#8b949e',
    'border': '#30363d',
    'grid': '#21262d',
    'accent': ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#bc8cff',
               '#79c0ff', '#56d364', '#e3b341', '#ff7b72', '#d2a8ff'],
}


def apply_theme():
    """Apply premium dark theme to matplotlib."""
    plt.rcParams.update({
        'figure.facecolor': THEME['bg_primary'],
        'axes.facecolor': THEME['bg_secondary'],
        'text.color': THEME['text_primary'],
        'axes.labelcolor': THEME['text_primary'],
        'xtick.color': THEME['text_secondary'],
        'ytick.color': THEME['text_secondary'],
        'axes.edgecolor': THEME['border'],
        'grid.color': THEME['grid'],
        'grid.alpha': 0.6,
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.titlepad': 15,
        'axes.grid': True,
        'grid.linewidth': 0.5,
        'figure.dpi': 150,
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
        'savefig.facecolor': THEME['bg_primary'],
        'savefig.edgecolor': 'none',
        'legend.facecolor': THEME['bg_secondary'],
        'legend.edgecolor': THEME['border'],
        'legend.fontsize': 10,
    })
    sns.set_palette(THEME['accent'])


# ─── Data Loading ──────────────────────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load data from file."""
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


# ─── Chart Functions ───────────────────────────────────────────────────────────

def chart_line(df, x, y, hue=None, title=None, output=None):
    """Line chart for trends over time."""
    fig, ax = plt.subplots(figsize=(12, 6))

    if hue and hue in df.columns:
        for i, group in enumerate(df[hue].unique()):
            mask = df[hue] == group
            color = THEME['accent'][i % len(THEME['accent'])]
            ax.plot(df.loc[mask, x], df.loc[mask, y], marker='o', markersize=4,
                    linewidth=2, color=color, label=str(group))
        ax.legend()
    else:
        color = THEME['accent'][0]
        ax.plot(df[x], df[y], marker='o', markersize=4, linewidth=2, color=color)
        ax.fill_between(df[x], df[y], alpha=0.08, color=color)

    ax.set_title(title or f'{y} over {x}')
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.xticks(rotation=45, ha='right')
    _save_or_show(fig, output, f'line_{y}_over_{x}')


def chart_bar(df, x, y, hue=None, title=None, output=None, horizontal=False):
    """Bar chart for category comparisons."""
    fig, ax = plt.subplots(figsize=(10, 6))

    if horizontal:
        sns.barplot(data=df, y=x, x=y, hue=hue, ax=ax, palette=THEME['accent'], edgecolor='none')
    else:
        sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax, palette=THEME['accent'], edgecolor='none')

    ax.set_title(title or f'{y} by {x}')

    if not horizontal:
        plt.xticks(rotation=45, ha='right')

    # Add value labels
    for container in ax.containers:
        labels = [f'{v.get_width():,.0f}' if horizontal else f'{v.get_height():,.0f}' for v in container]
        ax.bar_label(container, labels=labels, padding=3, color=THEME['text_secondary'], fontsize=9)

    _save_or_show(fig, output, f'bar_{y}_by_{x}')


def chart_scatter(df, x, y, hue=None, title=None, output=None):
    """Scatter plot for correlations."""
    fig, ax = plt.subplots(figsize=(10, 8))

    if hue and hue in df.columns:
        for i, group in enumerate(df[hue].unique()):
            mask = df[hue] == group
            color = THEME['accent'][i % len(THEME['accent'])]
            ax.scatter(df.loc[mask, x], df.loc[mask, y], alpha=0.7, s=50,
                      color=color, label=str(group), edgecolors='none')
        ax.legend()
    else:
        ax.scatter(df[x], df[y], alpha=0.7, s=50, color=THEME['accent'][0], edgecolors='none')

    # Add trend line
    try:
        z = np.polyfit(df[x].dropna(), df[y].dropna(), 1)
        p = np.poly1d(z)
        x_range = np.linspace(df[x].min(), df[x].max(), 100)
        ax.plot(x_range, p(x_range), '--', color=THEME['accent'][3], alpha=0.8, linewidth=1.5)
    except Exception:
        pass

    corr = df[x].corr(df[y])
    ax.set_title(title or f'{y} vs {x} (r={corr:.3f})')
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    _save_or_show(fig, output, f'scatter_{y}_vs_{x}')


def chart_histogram(df, x, title=None, output=None, bins=30):
    """Histogram for distributions."""
    fig, ax = plt.subplots(figsize=(10, 6))

    data = df[x].dropna()
    ax.hist(data, bins=bins, color=THEME['accent'][0], edgecolor=THEME['bg_primary'],
            alpha=0.8, linewidth=0.5)

    # Add mean and median lines
    mean_val = data.mean()
    median_val = data.median()
    ax.axvline(mean_val, color=THEME['accent'][3], linestyle='--', linewidth=1.5,
               label=f'Mean: {mean_val:,.2f}')
    ax.axvline(median_val, color=THEME['accent'][1], linestyle='--', linewidth=1.5,
               label=f'Median: {median_val:,.2f}')

    ax.legend()
    ax.set_title(title or f'Distribution of {x}')
    ax.set_xlabel(x)
    ax.set_ylabel('Frequency')
    _save_or_show(fig, output, f'hist_{x}')


def chart_box(df, x, y=None, title=None, output=None):
    """Box plot for spread and outliers."""
    fig, ax = plt.subplots(figsize=(10, 6))

    if y:
        sns.boxplot(data=df, x=x, y=y, ax=ax, palette=THEME['accent'],
                    flierprops={'markerfacecolor': THEME['accent'][3], 'markersize': 4})
    else:
        sns.boxplot(data=df, x=x, ax=ax, color=THEME['accent'][0],
                    flierprops={'markerfacecolor': THEME['accent'][3], 'markersize': 4})

    ax.set_title(title or f'Box Plot: {y or x}' + (f' by {x}' if y else ''))
    plt.xticks(rotation=45, ha='right')
    _save_or_show(fig, output, f'box_{y or x}')


def chart_heatmap(df, title=None, output=None):
    """Correlation heatmap."""
    fig, ax = plt.subplots(figsize=(10, 8))

    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) < 2:
        print("ERROR: Need at least 2 numeric columns for heatmap")
        return

    corr = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', center=0,
                ax=ax, linewidths=0.5, fmt='.2f', square=True,
                cbar_kws={'shrink': 0.8})

    ax.set_title(title or 'Correlation Heatmap')
    _save_or_show(fig, output, 'heatmap_correlation')


def chart_pie(df, x, y=None, title=None, output=None):
    """Pie chart for proportions."""
    fig, ax = plt.subplots(figsize=(8, 8))

    if y:
        data = df.groupby(x)[y].sum()
    else:
        data = df[x].value_counts()

    # Limit to top 6 + "Other"
    if len(data) > 6:
        top = data.head(5)
        top['Other'] = data[5:].sum()
        data = top

    colors = THEME['accent'][:len(data)]
    wedges, texts, autotexts = ax.pie(
        data.values, labels=data.index, autopct='%1.1f%%',
        colors=colors, startangle=90, pctdistance=0.85,
        textprops={'color': THEME['text_primary'], 'fontsize': 10}
    )

    # Donut style
    centre_circle = plt.Circle((0, 0), 0.65, fc=THEME['bg_primary'])
    ax.add_artist(centre_circle)

    ax.set_title(title or f'Distribution of {x}')
    _save_or_show(fig, output, f'pie_{x}')


def chart_violin(df, x, y, title=None, output=None):
    """Violin plot for distribution shape."""
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.violinplot(data=df, x=x, y=y, ax=ax, palette=THEME['accent'],
                   inner='box', linewidth=1)

    ax.set_title(title or f'{y} Distribution by {x}')
    plt.xticks(rotation=45, ha='right')
    _save_or_show(fig, output, f'violin_{y}_by_{x}')


def chart_pair(df, title=None, output=None):
    """Pair plot for multi-variable overview."""
    numeric_cols = df.select_dtypes(include='number').columns[:5]  # Limit to 5
    if len(numeric_cols) < 2:
        print("ERROR: Need at least 2 numeric columns for pair plot")
        return

    g = sns.pairplot(df[numeric_cols], diag_kind='kde',
                     plot_kws={'alpha': 0.6, 's': 30, 'edgecolors': 'none'},
                     diag_kws={'alpha': 0.7})

    g.figure.suptitle(title or 'Pair Plot', y=1.02, fontsize=16, fontweight='bold',
                      color=THEME['text_primary'])
    g.figure.set_facecolor(THEME['bg_primary'])

    for ax_row in g.axes:
        for ax in ax_row:
            ax.set_facecolor(THEME['bg_secondary'])
            ax.tick_params(colors=THEME['text_secondary'])
            ax.xaxis.label.set_color(THEME['text_primary'])
            ax.yaxis.label.set_color(THEME['text_primary'])

    output_path = output or _default_output('pair_plot')
    g.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=THEME['bg_primary'])
    print(f"✓ Saved pair plot → {output_path}")
    plt.close()


# ─── Auto Mode ─────────────────────────────────────────────────────────────────

def auto_visualize(df, output_dir=None):
    """Automatically generate the most useful charts based on data types."""
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = []

    # Detect datetime columns
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                pd.to_datetime(df[col].head(10))
                datetime_cols.append(col)
            except (ValueError, TypeError):
                pass

    out_dir = Path(output_dir) if output_dir else Path('output/charts')
    out_dir.mkdir(parents=True, exist_ok=True)

    charts_created = []

    # 1. Distribution of numeric columns (top 3)
    for col in numeric_cols[:3]:
        output = str(out_dir / f'hist_{col}.png')
        chart_histogram(df, col, output=output)
        charts_created.append(output)

    # 2. Top categorical bar charts
    for col in categorical_cols[:2]:
        if df[col].nunique() <= 15:
            for num_col in numeric_cols[:1]:
                output = str(out_dir / f'bar_{num_col}_by_{col}.png')
                chart_bar(df, col, num_col, output=output)
                charts_created.append(output)

    # 3. Time series if datetime found
    for dt_col in datetime_cols[:1]:
        for num_col in numeric_cols[:1]:
            try:
                df_sorted = df.sort_values(dt_col)
                output = str(out_dir / f'line_{num_col}_over_{dt_col}.png')
                chart_line(df_sorted, dt_col, num_col, output=output)
                charts_created.append(output)
            except Exception:
                pass

    # 4. Correlation heatmap
    if len(numeric_cols) >= 2:
        output = str(out_dir / 'heatmap_correlation.png')
        chart_heatmap(df, output=output)
        charts_created.append(output)

    # 5. Scatter of top correlated pair
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().abs()
        np.fill_diagonal(corr.values, 0)
        max_corr = corr.max().max()
        if max_corr > 0.3:
            idx = np.unravel_index(corr.values.argmax(), corr.shape)
            col1, col2 = numeric_cols[idx[0]], numeric_cols[idx[1]]
            output = str(out_dir / f'scatter_{col2}_vs_{col1}.png')
            chart_scatter(df, col1, col2, output=output)
            charts_created.append(output)

    print(f"\n✓ Auto mode generated {len(charts_created)} charts:")
    for c in charts_created:
        print(f"  → {c}")

    return charts_created


# ─── Helpers ───────────────────────────────────────────────────────────────────

def _default_output(name):
    """Generate default output path."""
    out_dir = Path('output/charts')
    out_dir.mkdir(parents=True, exist_ok=True)
    return str(out_dir / f'{name}.png')


def _save_or_show(fig, output, default_name):
    """Save figure to file or show."""
    output_path = output or _default_output(default_name)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=THEME['bg_primary'])
    print(f"✓ Saved chart → {output_path}")
    plt.close(fig)


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="📈 Chart Generator — Create publication-quality visualizations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Chart Types:
  line      Line chart (trends over time)
  bar       Vertical bar chart (category comparison)
  hbar      Horizontal bar chart (rankings)
  scatter   Scatter plot (correlations)
  hist      Histogram (distributions)
  box       Box plot (spread & outliers)
  heatmap   Correlation heatmap
  pie       Pie/donut chart (proportions)
  violin    Violin plot (distribution shape)
  pair      Pair plot (multi-variable overview)

Examples:
  python visualize.py --input data.csv --auto
  python visualize.py --input data.csv --type bar --x category --y revenue
  python visualize.py --input data.csv --type line --x date --y sales --hue region
  python visualize.py --input data.csv --type hist --x amount --output dist.png
        """
    )
    parser.add_argument('--input', '-i', required=True, help='Input data file')
    parser.add_argument('--type', '-t', choices=['line', 'bar', 'hbar', 'scatter', 'hist',
                        'box', 'heatmap', 'pie', 'violin', 'pair'],
                        help='Chart type')
    parser.add_argument('--x', help='X-axis column')
    parser.add_argument('--y', help='Y-axis column')
    parser.add_argument('--hue', help='Color grouping column')
    parser.add_argument('--title', help='Chart title')
    parser.add_argument('--output', '-o', help='Output file path (default: output/charts/)')
    parser.add_argument('--auto', action='store_true', help='Auto-generate recommended charts')
    parser.add_argument('--output-dir', help='Output directory for auto mode')

    args = parser.parse_args()
    apply_theme()

    df = load_data(args.input)
    print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns")

    if args.auto:
        auto_visualize(df, args.output_dir)
        return

    if not args.type:
        print("ERROR: Specify --type or use --auto")
        parser.print_help()
        sys.exit(1)

    chart_map = {
        'line': lambda: chart_line(df, args.x, args.y, args.hue, args.title, args.output),
        'bar': lambda: chart_bar(df, args.x, args.y, args.hue, args.title, args.output),
        'hbar': lambda: chart_bar(df, args.x, args.y, args.hue, args.title, args.output, horizontal=True),
        'scatter': lambda: chart_scatter(df, args.x, args.y, args.hue, args.title, args.output),
        'hist': lambda: chart_histogram(df, args.x, args.title, args.output),
        'box': lambda: chart_box(df, args.x, args.y, args.title, args.output),
        'heatmap': lambda: chart_heatmap(df, args.title, args.output),
        'pie': lambda: chart_pie(df, args.x, args.y, args.title, args.output),
        'violin': lambda: chart_violin(df, args.x, args.y, args.title, args.output),
        'pair': lambda: chart_pair(df, args.title, args.output),
    }

    # Validate required args
    needs_x = {'line', 'bar', 'hbar', 'scatter', 'hist', 'box', 'pie', 'violin'}
    needs_y = {'line', 'bar', 'hbar', 'scatter', 'violin'}

    if args.type in needs_x and not args.x:
        print(f"ERROR: --x is required for {args.type} chart")
        sys.exit(1)
    if args.type in needs_y and not args.y:
        print(f"ERROR: --y is required for {args.type} chart")
        sys.exit(1)

    chart_map[args.type]()


if __name__ == '__main__':
    main()
