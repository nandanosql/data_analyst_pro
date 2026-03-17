#!/usr/bin/env python3
"""
chart_templates.py — Reusable Chart Functions with Premium Dark Theme
Import and use these functions in your own analysis scripts.

Usage:
    from resources.chart_templates import create_line_chart, create_bar_chart, apply_dark_theme
"""

import sys

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import numpy as np
except ImportError:
    print("ERROR: matplotlib not installed. Run: pip install matplotlib")
    sys.exit(1)


# ─── Theme Configuration ──────────────────────────────────────────────────────

DARK_THEME = {
    'bg_primary': '#0d1117',
    'bg_secondary': '#161b22',
    'bg_tertiary': '#1c2128',
    'text_primary': '#e6edf3',
    'text_secondary': '#8b949e',
    'text_muted': '#484f58',
    'border': '#30363d',
    'grid': '#21262d',
    'accent_blue': '#58a6ff',
    'accent_green': '#3fb950',
    'accent_yellow': '#d29922',
    'accent_red': '#f85149',
    'accent_purple': '#bc8cff',
    'accent_cyan': '#79c0ff',
    'accent_teal': '#56d364',
    'accent_orange': '#e3b341',
    'accent_pink': '#ff7b72',
    'accent_lavender': '#d2a8ff',
}

LIGHT_THEME = {
    'bg_primary': '#ffffff',
    'bg_secondary': '#f6f8fa',
    'bg_tertiary': '#eaedf0',
    'text_primary': '#1f2328',
    'text_secondary': '#656d76',
    'text_muted': '#8b949e',
    'border': '#d0d7de',
    'grid': '#eaeef2',
    'accent_blue': '#0969da',
    'accent_green': '#1a7f37',
    'accent_yellow': '#9a6700',
    'accent_red': '#cf222e',
    'accent_purple': '#8250df',
    'accent_cyan': '#0550ae',
    'accent_teal': '#116329',
    'accent_orange': '#bc4c00',
    'accent_pink': '#bf3989',
    'accent_lavender': '#8250df',
}

PALETTES = {
    'default': ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#bc8cff',
                '#79c0ff', '#56d364', '#e3b341', '#ff7b72', '#d2a8ff'],
    'cool': ['#58a6ff', '#79c0ff', '#bc8cff', '#d2a8ff', '#56d364',
             '#3fb950', '#39d2c0', '#0ea5e9', '#818cf8', '#a78bfa'],
    'warm': ['#f85149', '#ff7b72', '#e3b341', '#d29922', '#f97316',
             '#ef4444', '#f59e0b', '#eab308', '#fb923c', '#fbbf24'],
    'earth': ['#3fb950', '#56d364', '#d29922', '#e3b341', '#8b949e',
              '#6e7681', '#79c0ff', '#58a6ff', '#bc8cff', '#d2a8ff'],
}


def apply_dark_theme():
    """Apply the premium dark theme to all subsequent plots."""
    theme = DARK_THEME
    plt.rcParams.update({
        'figure.facecolor': theme['bg_primary'],
        'axes.facecolor': theme['bg_secondary'],
        'text.color': theme['text_primary'],
        'axes.labelcolor': theme['text_primary'],
        'xtick.color': theme['text_secondary'],
        'ytick.color': theme['text_secondary'],
        'axes.edgecolor': theme['border'],
        'grid.color': theme['grid'],
        'grid.alpha': 0.6,
        'grid.linewidth': 0.5,
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.titlepad': 15,
        'axes.grid': True,
        'figure.dpi': 150,
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
        'savefig.facecolor': theme['bg_primary'],
        'savefig.edgecolor': 'none',
        'legend.facecolor': theme['bg_secondary'],
        'legend.edgecolor': theme['border'],
        'legend.fontsize': 10,
    })


def apply_light_theme():
    """Apply a clean light theme to all subsequent plots."""
    theme = LIGHT_THEME
    plt.rcParams.update({
        'figure.facecolor': theme['bg_primary'],
        'axes.facecolor': theme['bg_secondary'],
        'text.color': theme['text_primary'],
        'axes.labelcolor': theme['text_primary'],
        'xtick.color': theme['text_secondary'],
        'ytick.color': theme['text_secondary'],
        'axes.edgecolor': theme['border'],
        'grid.color': theme['grid'],
        'grid.alpha': 0.8,
        'grid.linewidth': 0.5,
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.titlepad': 15,
        'axes.grid': True,
        'figure.dpi': 150,
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
        'savefig.facecolor': theme['bg_primary'],
        'savefig.edgecolor': 'none',
        'legend.facecolor': theme['bg_primary'],
        'legend.edgecolor': theme['border'],
        'legend.fontsize': 10,
    })


def get_colors(palette='default', n=None):
    """Get a list of colors from a named palette."""
    colors = PALETTES.get(palette, PALETTES['default'])
    if n:
        return colors[:n]
    return colors


# ─── Chart Templates ──────────────────────────────────────────────────────────

def create_line_chart(x, y, title='', xlabel='', ylabel='',
                      color=None, fill=True, markers=True,
                      figsize=(12, 6), output=None):
    """Create a styled line chart.
    
    Args:
        x: X-axis data
        y: Y-axis data (or list of y-series for multiple lines)
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        color: Line color(s)
        fill: Whether to fill under the line
        markers: Whether to show data point markers
        figsize: Figure size tuple
        output: Path to save the chart (None = return fig, ax)
    """
    colors = get_colors()
    fig, ax = plt.subplots(figsize=figsize)

    c = color or colors[0]
    ax.plot(x, y, color=c, linewidth=2,
            marker='o' if markers else None, markersize=4)
    if fill:
        ax.fill_between(x, y, alpha=0.08, color=c)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if output:
        fig.savefig(output)
        plt.close(fig)
        return output
    return fig, ax


def create_bar_chart(categories, values, title='', xlabel='', ylabel='',
                     colors=None, horizontal=False, show_values=True,
                     figsize=(10, 6), output=None):
    """Create a styled bar chart.
    
    Args:
        categories: Category labels
        values: Bar values
        title: Chart title
        colors: Bar colors (list or single color)
        horizontal: Horizontal bars if True
        show_values: Show value labels on bars
        output: Path to save
    """
    palette = colors or get_colors(n=len(categories))
    fig, ax = plt.subplots(figsize=figsize)

    if horizontal:
        bars = ax.barh(categories, values, color=palette, edgecolor='none', height=0.6)
        if show_values:
            for bar, val in zip(bars, values):
                ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                        f'{val:,.0f}', va='center', fontsize=9,
                        color=DARK_THEME['text_secondary'])
    else:
        bars = ax.bar(categories, values, color=palette, edgecolor='none', width=0.6)
        if show_values:
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.01,
                        f'{val:,.0f}', ha='center', va='bottom', fontsize=9,
                        color=DARK_THEME['text_secondary'])

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if not horizontal:
        plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    if output:
        fig.savefig(output)
        plt.close(fig)
        return output
    return fig, ax


def create_donut_chart(labels, values, title='', colors=None,
                       figsize=(8, 8), output=None):
    """Create a styled donut chart.
    
    Args:
        labels: Slice labels
        values: Slice values
        title: Chart title
        colors: Slice colors
        output: Path to save
    """
    palette = colors or get_colors(n=len(labels))
    fig, ax = plt.subplots(figsize=figsize)

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%',
        colors=palette, startangle=90, pctdistance=0.85,
        textprops={'color': DARK_THEME['text_primary'], 'fontsize': 10}
    )

    # Donut hole
    centre = plt.Circle((0, 0), 0.65, fc=DARK_THEME['bg_primary'])
    ax.add_artist(centre)

    # Center text
    total = sum(values)
    ax.text(0, 0, f'{total:,.0f}\nTotal', ha='center', va='center',
            fontsize=14, fontweight='bold', color=DARK_THEME['text_primary'])

    ax.set_title(title)

    if output:
        fig.savefig(output)
        plt.close(fig)
        return output
    return fig, ax


def create_metric_card(value, label, delta=None, delta_label='vs prev',
                       figsize=(3, 2), output=None):
    """Create a single metric card visualization.
    
    Args:
        value: Main metric value
        label: Metric label
        delta: Change from previous (e.g., 0.12 for +12%)
        delta_label: Label for the delta
        output: Path to save
    """
    theme = DARK_THEME
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Background card
    from matplotlib.patches import FancyBboxPatch
    card = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                          boxstyle="round,pad=0.05",
                          facecolor=theme['bg_tertiary'],
                          edgecolor=theme['border'], linewidth=1)
    ax.add_patch(card)

    # Value
    if isinstance(value, (int, float)):
        value_str = f'{value:,.0f}' if value > 100 else f'{value:,.2f}'
    else:
        value_str = str(value)

    ax.text(0.5, 0.55, value_str, ha='center', va='center',
            fontsize=28, fontweight='bold', color=theme['text_primary'])

    # Label
    ax.text(0.5, 0.25, label, ha='center', va='center',
            fontsize=11, color=theme['text_secondary'])

    # Delta
    if delta is not None:
        delta_color = theme['accent_green'] if delta >= 0 else theme['accent_red']
        arrow = '▲' if delta >= 0 else '▼'
        ax.text(0.5, 0.82, f'{arrow} {abs(delta)*100:.1f}% {delta_label}',
                ha='center', va='center', fontsize=9, color=delta_color)

    if output:
        fig.savefig(output)
        plt.close(fig)
        return output
    return fig, ax


# ─── Convenience Exports ──────────────────────────────────────────────────────

__all__ = [
    'DARK_THEME', 'LIGHT_THEME', 'PALETTES',
    'apply_dark_theme', 'apply_light_theme', 'get_colors',
    'create_line_chart', 'create_bar_chart', 'create_donut_chart',
    'create_metric_card',
]
