
#!/usr/bin/env python3
"""
TB Causal Inference - Publication-quality figures and tables.
遵循四大医学顶刊 (NEJM/Lancet/JAMA/BMJ) 图表规范。
A4 纵向, min 12pt Arial, ColorBrewer 色盲友好配色。
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# GLOBAL CONFIG - 四大顶刊标准
# ============================================================
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 14,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.15,
    'axes.linewidth': 1.0,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Color palette - ColorBrewer Set2 (色盲友好)
CB_PALETTE = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']
WHO_BLUE = '#1a3a6b'
GBD_RED = '#c0392b'
SDG_GREEN = '#1e8449'
AMBER = '#d4a017'
PURPLE = '#7b1fa2'

REGION_COLORS = {
    'AFR': '#e41a1c',  # African Region - red
    'AMR': '#377eb8',  # Region of the Americas - blue
    'EMR': '#4daf4a',  # Eastern Mediterranean - green
    'EUR': '#984ea3',  # European Region - purple
    'SEAR': '#ff7f00', # South-East Asia - orange
    'WPR': '#a65628',  # Western Pacific - brown
}

REGION_NAMES = {
    'AFR': 'African',
    'AMR': 'Americas',
    'EMR': 'Eastern Mediterranean',
    'EUR': 'European',
    'SEAR': 'South-East Asia',
    'WPR': 'Western Pacific',
}

OUTPUT_DIR = Path(r'E:\20260617 tuberculosis-causal-inference\04_图表')
DATA_PATH = Path(r'E:\20260617 tuberculosis-causal-inference\02_原始数据\who_gbd\master_data.csv')

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv(DATA_PATH)

# Filter invalid data (gbd_inc = 1.0 is a placeholder)
df_valid = df[df['gbd_inc'] > 1.5].copy()
print(f"Total records: {len(df)}, Valid: {len(df_valid)}")

# Compute additional metrics
df_valid['abs_diff'] = np.abs(df_valid['diff'])
df_valid['ratio_log'] = np.log2(df_valid['ratio'])
df_valid['mean_inc_log'] = np.log10(df_valid['mean_inc'])

# Regional summary
region_summary = df_valid.groupby('region').agg(
    n=('country', 'count'),
    who_mean=('who_inc', 'mean'),
    who_sd=('who_inc', 'std'),
    gbd_mean=('gbd_inc', 'mean'),
    gbd_sd=('gbd_inc', 'std'),
    ratio_mean=('ratio', 'mean'),
    ratio_sd=('ratio', 'std'),
    diff_mean=('diff', 'mean'),
    diff_sd=('diff', 'std'),
    diff_median=('diff', 'median'),
    ratio_gt1=('ratio', lambda x: (x > 1).sum()),
    ratio_lt1=('ratio', lambda x: (x < 1).sum()),
).reset_index()
region_summary['region_name'] = region_summary['region'].map(REGION_NAMES)
region_summary['ratio_gt1_pct'] = region_summary['ratio_gt1'] / region_summary['n'] * 100
region_summary['who_overestimates'] = region_summary['diff_mean'] > 0


def add_subplot_label(ax, label, x=-0.08, y=1.05, fontsize=14):
    """Add subplot label in top-left, no parentheses, no bold."""
    ax.text(x, y, label, transform=ax.transAxes, fontsize=fontsize,
            fontweight='regular', fontfamily='Arial', va='bottom', ha='left')


def add_rounded_border(fig, ax, color='#cccccc', lw=1.0, radius=8):
    """Add rounded rectangle border around subplot area."""
    bbox = ax.get_position()
    rect = FancyBboxPatch(
        (bbox.x0, bbox.y0), bbox.width, bbox.height,
        boxstyle=f"round,pad=0.005,rounding_size={radius/72}",
        transform=fig.transFigure, facecolor='none',
        edgecolor=color, linewidth=lw, zorder=0
    )
    fig.patches.append(rect)


def style_ax(ax, xlabel='', ylabel='', title=''):
    """Apply consistent styling: no top/right spine, light gray y-grid."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#aaaaaa')
    ax.set_axisbelow(True)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=14, fontfamily='Arial')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=14, fontfamily='Arial')
    if title:
        ax.set_title(title, fontsize=15, fontfamily='Arial', fontweight='normal', pad=10)


# ============================================================
# FIGURE 1: Global Divergence Map (scatter)
# ============================================================
def fig1_global_map():
    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Color by ratio
    norm = plt.Normalize(vmin=0.3, vmax=3.0)
    cmap = plt.cm.RdYlBu_r  # Red = WHO > GBD, Blue = GBD > WHO

    scatter = ax.scatter(
        df_valid['lon'], df_valid['lat'],
        c=df_valid['ratio'], cmap=cmap, norm=norm,
        s=np.clip(df_valid['mean_inc'] / 5, 8, 200),
        alpha=0.75, edgecolors='white', linewidth=0.3
    )

    cbar = plt.colorbar(scatter, ax=ax, shrink=0.75, pad=0.02)
    cbar.set_label('WHO / GBD Incidence Ratio', fontsize=11, fontfamily='Arial')
    cbar.ax.tick_params(labelsize=10)

    ax.set_xlabel('Longitude', fontsize=13, fontfamily='Arial')
    ax.set_ylabel('Latitude', fontsize=13, fontfamily='Arial')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-60, 85)
    style_ax(ax)
    ax.set_title('Global Divergence in TB Incidence Estimates', fontsize=15, fontfamily='Arial', pad=12)

    # Legend for size
    for size, label in [(20, 'Low burden'), (80, 'Medium'), (200, 'High burden')]:
        ax.scatter([], [], s=size, c='gray', alpha=0.5, edgecolors='white', linewidth=0.5, label=label)
    ax.legend(title='Mean Incidence', loc='lower left', fontsize=9, title_fontsize=10, frameon=True, facecolor='white')

    add_subplot_label(ax, 'A')
    fig.savefig(OUTPUT_DIR / 'Fig1_Global_Divergence.png', dpi=300, facecolor='white')
    fig.savefig(OUTPUT_DIR / 'Fig1_Global_Divergence.svg', facecolor='white')
    plt.close(fig)
    print("  Fig1 saved.")


# ============================================================
# FIGURE 2: Bland-Altman Decomposition
# ============================================================
def fig2_bland_altman():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.subplots_adjust(wspace=0.35)

    # Panel A: Bland-Altman
    ax = axes[0]
    mean_diff = df_valid['diff'].mean()
    sd_diff = df_valid['diff'].std()

    for region, color in REGION_COLORS.items():
        mask = df_valid['region'] == region
        ax.scatter(df_valid.loc[mask, 'mean_inc'], df_valid.loc[mask, 'diff'],
                   c=color, alpha=0.6, s=25, edgecolors='white', linewidth=0.3,
                   label=REGION_NAMES[region], zorder=3)

    ax.axhline(mean_diff, color='#333333', linestyle='-', linewidth=1.2, zorder=2)
    ax.axhline(mean_diff + 1.96 * sd_diff, color='#999999', linestyle='--', linewidth=0.8)
    ax.axhline(mean_diff - 1.96 * sd_diff, color='#999999', linestyle='--', linewidth=0.8)
    ax.axhline(0, color='#cccccc', linestyle=':', linewidth=0.8, zorder=1)

    ax.set_xlabel('Mean Incidence (WHO & GBD)', fontsize=13)
    ax.set_ylabel('Difference (WHO − GBD)', fontsize=13)
    style_ax(ax)
    add_subplot_label(ax, 'A')

    # Annotation
    ax.text(0.95, 0.08, f'Mean diff: {mean_diff:.1f}\n±1.96 SD: [{mean_diff-1.96*sd_diff:.0f}, {mean_diff+1.96*sd_diff:.0f}]',
            transform=ax.transAxes, fontsize=9, fontfamily='Arial', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    # Panel B: Ratio distribution by region
    ax = axes[1]
    region_order = ['AFR', 'AMR', 'EMR', 'EUR', 'SEAR', 'WPR']
    region_data = [df_valid[df_valid['region'] == r]['ratio'] for r in region_order]
    colors = [REGION_COLORS[r] for r in region_order]
    labels = [REGION_NAMES[r] for r in region_order]

    bp = ax.boxplot(region_data, patch_artist=True, widths=0.6,
                    medianprops={'color': '#333333', 'linewidth': 1.5},
                    flierprops={'marker': 'o', 'markerfacecolor': '#999999', 'markersize': 3, 'alpha': 0.5})
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.axhline(1.0, color='#333333', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=11)
    ax.set_ylabel('WHO / GBD Incidence Ratio', fontsize=13)
    ax.set_ylim(0, 4.5)
    style_ax(ax)
    add_subplot_label(ax, 'B')

    fig.savefig(OUTPUT_DIR / 'Fig2_Bland_Altman.png', dpi=300, facecolor='white')
    fig.savefig(OUTPUT_DIR / 'Fig2_Bland_Altman.svg', facecolor='white')
    plt.close(fig)
    print("  Fig2 saved.")


# ============================================================
# FIGURE 3: Regional Summary Forest Plot
# ============================================================
def fig3_regional_forest():
    fig, ax = plt.subplots(figsize=(10, 5))

    summary = region_summary.sort_values('ratio_mean', ascending=True)
    y_positions = range(len(summary))

    # Forest plot style
    for i, (_, row) in enumerate(summary.iterrows()):
        color = REGION_COLORS[row['region']]
        ax.errorbar(row['ratio_mean'], i, xerr=row['ratio_sd'],
                    fmt='o', color=color, capsize=5, capthick=2,
                    markersize=10, markeredgecolor='white', markeredgewidth=1.2,
                    elinewidth=2, label=REGION_NAMES[row['region']] if i == 0 else "")

        # Add n and ratio text
        ax.text(row['ratio_mean'] + row['ratio_sd'] + 0.05, i,
                f"n={row['n']}, ratio={row['ratio_mean']:.2f}",
                fontsize=9, fontfamily='Arial', va='center')

    # Rebuild legend
    handles = []
    for region in summary['region'].unique():
        color = REGION_COLORS[region]
        handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                                   markersize=10, markeredgecolor='white', markeredgewidth=0.5,
                                   label=REGION_NAMES[region]))

    ax.axvline(1.0, color='#333333', linestyle='--', linewidth=1.0, alpha=0.6)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f"{REGION_NAMES[row['region']]}" for _, row in summary.iterrows()], fontsize=12)
    ax.set_xlabel('WHO / GBD Incidence Ratio (mean ± SD)', fontsize=13)
    ax.legend(handles=handles, loc='lower right', fontsize=9, frameon=True, facecolor='white',
              edgecolor='#cccccc', ncol=2)
    style_ax(ax)
    ax.set_title('Regional Heterogeneity in TB Incidence Divergence', fontsize=15, pad=12)

    fig.savefig(OUTPUT_DIR / 'Fig3_Regional_Forest.png', dpi=300, facecolor='white')
    fig.savefig(OUTPUT_DIR / 'Fig3_Regional_Forest.svg', facecolor='white')
    plt.close(fig)
    print("  Fig3 saved.")


# ============================================================
# FIGURE 4: Top 20 Countries by Divergence
# ============================================================
def fig4_top_countries():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.subplots_adjust(wspace=0.35)

    # Panel A: Top 20 WHO overestimates
    ax = axes[0]
    top_over = df_valid.nlargest(20, 'diff')
    colors = [WHO_BLUE if v > 0 else GBD_RED for v in top_over['diff']]
    bars = ax.barh(range(20), top_over['diff'].values[::-1], color=colors[::-1], height=0.7,
                   edgecolor='white', linewidth=0.5)
    ax.set_yticks(range(20))
    ax.set_yticklabels(top_over['country'].values[::-1], fontsize=10)
    ax.set_xlabel('Difference (WHO − GBD)', fontsize=13)
    ax.axvline(0, color='#333333', linewidth=0.8)
    style_ax(ax)
    ax.set_title('WHO > GBD (Top 20)', fontsize=13, pad=10)
    add_subplot_label(ax, 'A')

    # Panel B: Top 20 GBD overestimates
    ax = axes[1]
    top_under = df_valid.nsmallest(20, 'diff')
    colors = [GBD_RED if v < 0 else WHO_BLUE for v in top_under['diff']]
    bars = ax.barh(range(20), top_under['diff'].values, color=colors, height=0.7,
                   edgecolor='white', linewidth=0.5)
    ax.set_yticks(range(20))
    ax.set_yticklabels(top_under['country'].values, fontsize=10)
    ax.set_xlabel('Difference (WHO − GBD)', fontsize=13)
    ax.axvline(0, color='#333333', linewidth=0.8)
    style_ax(ax)
    ax.set_title('GBD > WHO (Top 20)', fontsize=13, pad=10)
    add_subplot_label(ax, 'B')

    fig.savefig(OUTPUT_DIR / 'Fig4_Top_Countries.png', dpi=300, facecolor='white')
    fig.savefig(OUTPUT_DIR / 'Fig4_Top_Countries.svg', facecolor='white')
    plt.close(fig)
    print("  Fig4 saved.")


# ============================================================
# FIGURE 5: Funnel / Scatter - Mean vs Ratio
# ============================================================
def fig5_mean_vs_ratio():
    fig, ax = plt.subplots(figsize=(8, 6))

    for region, color in REGION_COLORS.items():
        mask = df_valid['region'] == region
        ax.scatter(df_valid.loc[mask, 'mean_inc'], df_valid.loc[mask, 'ratio'],
                   c=color, alpha=0.55, s=35, edgecolors='white', linewidth=0.3,
                   label=REGION_NAMES[region], zorder=3)

    ax.axhline(1.0, color='#333333', linestyle='--', linewidth=0.8, alpha=0.6, zorder=1)
    ax.set_xscale('log')
    ax.set_xlabel('Mean TB Incidence per 100,000 (log scale)', fontsize=13)
    ax.set_ylabel('WHO / GBD Incidence Ratio', fontsize=13)
    ax.legend(fontsize=9, frameon=True, facecolor='white', edgecolor='#cccccc', ncol=2,
              loc='upper right')

    # Add correlation annotation
    corr = df_valid['mean_inc_log'].corr(df_valid['ratio_log'])
    ax.text(0.95, 0.05, f'Spearman ρ = {corr:.3f}', transform=ax.transAxes,
            fontsize=10, fontfamily='Arial', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#cccccc', alpha=0.9))

    style_ax(ax)
    ax.set_title('Burden-Dependent Divergence Pattern', fontsize=15, pad=12)

    fig.savefig(OUTPUT_DIR / 'Fig5_Mean_vs_Ratio.png', dpi=300, facecolor='white')
    fig.savefig(OUTPUT_DIR / 'Fig5_Mean_vs_Ratio.svg', facecolor='white')
    plt.close(fig)
    print("  Fig5 saved.")


# ============================================================
# FIGURE 6: Graphical Abstract - Summary Dashboard
# ============================================================
def fig6_dashboard():
    fig = plt.figure(figsize=(14, 10))

    # ---- A: World map mini ----
    ax1 = fig.add_subplot(2, 3, 1)
    norm = plt.Normalize(vmin=0.3, vmax=3.0)
    cmap = plt.cm.RdYlBu_r
    ax1.scatter(df_valid['lon'], df_valid['lat'], c=df_valid['ratio'], cmap=cmap, norm=norm,
                s=np.clip(df_valid['mean_inc'] / 10, 3, 100), alpha=0.6, edgecolors='white', linewidth=0.2)
    ax1.set_xlim(-180, 180); ax1.set_ylim(-60, 85)
    ax1.set_title('Global Divergence Map', fontsize=12)
    style_ax(ax1)
    add_subplot_label(ax1, 'A')

    # ---- B: Regional bar chart ----
    ax2 = fig.add_subplot(2, 3, 2)
    summary = region_summary.sort_values('ratio_mean')
    colors = [REGION_COLORS[r] for r in summary['region']]
    ax2.barh(range(len(summary)), summary['ratio_mean'], color=colors, height=0.6, edgecolor='white')
    for i, (_, row) in enumerate(summary.iterrows()):
        ax2.text(row['ratio_mean'] + 0.02, i, f"{row['ratio_mean']:.2f}", fontsize=10, va='center')
    ax2.axvline(1.0, color='#333333', linestyle='--', linewidth=0.8)
    ax2.set_yticks(range(len(summary)))
    ax2.set_yticklabels([REGION_NAMES[r] for r in summary['region']], fontsize=10)
    ax2.set_xlabel('WHO/GBD Ratio', fontsize=11)
    style_ax(ax2)
    ax2.set_title('Regional Mean Ratio', fontsize=12)
    add_subplot_label(ax2, 'B')

    # ---- C: Bland-Altman mini ----
    ax3 = fig.add_subplot(2, 3, 3)
    for region, color in REGION_COLORS.items():
        mask = df_valid['region'] == region
        ax3.scatter(df_valid.loc[mask, 'mean_inc'], df_valid.loc[mask, 'diff'],
                    c=color, alpha=0.4, s=12, edgecolors='none')
    ax3.axhline(0, color='#333333', linewidth=0.8)
    ax3.set_xlabel('Mean Incidence', fontsize=11)
    ax3.set_ylabel('WHO − GBD', fontsize=11)
    style_ax(ax3)
    ax3.set_title('Bland-Altman Plot', fontsize=12)
    add_subplot_label(ax3, 'C')

    # ---- D: Ratio histogram ----
    ax4 = fig.add_subplot(2, 3, 4)
    ax4.hist(df_valid['ratio'], bins=40, color=WHO_BLUE, alpha=0.7, edgecolor='white', linewidth=0.5)
    ax4.axvline(1.0, color=GBD_RED, linestyle='--', linewidth=1.5)
    ax4.set_xlabel('WHO / GBD Ratio', fontsize=11)
    ax4.set_ylabel('Number of Countries', fontsize=11)
    ax4.text(0.95, 0.92, f'Median: {df_valid["ratio"].median():.2f}', transform=ax4.transAxes,
             fontsize=10, ha='right', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#cccccc'))
    style_ax(ax4)
    ax4.set_title('Distribution of WHO/GBD Ratio', fontsize=12)
    add_subplot_label(ax4, 'D')

    # ---- E: Top 10 ----
    ax5 = fig.add_subplot(2, 3, 5)
    top10 = df_valid.nlargest(10, 'abs_diff').nsmallest(10, 'abs_diff')  # mixed
    top_pos = df_valid.nlargest(5, 'diff')
    top_neg = df_valid.nsmallest(5, 'diff')
    top_all = pd.concat([top_pos, top_neg])
    colors_top = [WHO_BLUE if v > 0 else GBD_RED for v in top_all['diff']]
    ax5.barh(range(10), top_all['diff'].values, color=colors_top, height=0.6, edgecolor='white')
    ax5.set_yticks(range(10))
    ax5.set_yticklabels(top_all['country'].values, fontsize=9)
    ax5.axvline(0, color='#333333', linewidth=0.8)
    ax5.set_xlabel('WHO − GBD Difference', fontsize=11)
    style_ax(ax5)
    ax5.set_title('Largest Absolute Divergence', fontsize=12)
    add_subplot_label(ax5, 'E')

    # ---- F: Summary statistics text panel ----
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    n_total = len(df_valid)
    pct_who_higher = (df_valid['ratio'] > 1).sum() / n_total * 100
    text = (
        f"Summary Statistics\n"
        f"{'─' * 35}\n"
        f"Countries analyzed: {n_total}\n"
        f"{'─' * 35}\n"
        f"Mean WHO incidence: {df_valid['who_inc'].mean():.1f}\n"
        f"Mean GBD incidence:  {df_valid['gbd_inc'].mean():.1f}\n"
        f"{'─' * 35}\n"
        f"Median WHO/GBD ratio: {df_valid['ratio'].median():.2f}\n"
        f"WHO > GBD: {df_valid['ratio'].gt(1).sum()} ({pct_who_higher:.0f}%)\n"
        f"GBD > WHO: {df_valid['ratio'].lt(1).sum()} ({100-pct_who_higher:.0f}%)\n"
        f"{'─' * 35}\n"
        f"Mean difference: {df_valid['diff'].mean():.1f}\n"
        f"SD of difference:  {df_valid['diff'].std():.1f}\n"
        f"Range: [{df_valid['diff'].min():.0f}, {df_valid['diff'].max():.0f}]\n"
        f"{'─' * 35}\n"
        f"Largest WHO excess: {df_valid.loc[df_valid['diff'].idxmax(), 'country']}\n"
        f"  ({df_valid['diff'].max():.0f} per 100k)\n"
        f"Largest GBD excess: {df_valid.loc[df_valid['diff'].idxmin(), 'country']}\n"
        f"  ({abs(df_valid['diff'].min()):.0f} per 100k)"
    )
    ax6.text(0.05, 0.95, text, transform=ax6.transAxes, fontsize=10, fontfamily='Arial',
             va='top', linespacing=1.5)
    add_subplot_label(ax6, 'F')

    fig.suptitle('TB Incidence Divergence: WHO vs GBD Estimates', fontsize=18, fontfamily='Arial',
                 fontweight='normal', y=0.99)

    fig.savefig(OUTPUT_DIR / 'Fig6_Dashboard.png', dpi=300, facecolor='white')
    fig.savefig(OUTPUT_DIR / 'Fig6_Dashboard.svg', facecolor='white')
    plt.close(fig)
    print("  Fig6 saved.")


# ============================================================
# RUN ALL FIGURES
# ============================================================
if __name__ == '__main__':
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating publication-quality figures...")
    fig1_global_map()
    fig2_bland_altman()
    fig3_regional_forest()
    fig4_top_countries()
    fig5_mean_vs_ratio()
    fig6_dashboard()
    print("\nAll figures generated successfully.")
