import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np

CLEAN_CSV   = 'data/processed/clean_df.csv'
FIGURES_DIR = 'figures'
os.makedirs(FIGURES_DIR, exist_ok=True)

df = pd.read_csv(CLEAN_CSV, encoding='utf-8-sig')
phq_cols  = [f'e{i}_phq9' for i in range(1, 10)]
gad_cols  = [f'f{i}_gad7' for i in range(1, 8)]
mspss_cols = [f'd{i}_mspss' for i in range(1, 13)]

sns.set_theme(style='whitegrid', palette='deep')
n = len(df)

# ── Plot 1: Score Distributions ──────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=150)
for ax, col, label, cutoff, color in [
    (axes[0], 'phq9_total', 'PHQ-9 Depression Score', 10, '#e05c5c'),
    (axes[1], 'gad7_total', 'GAD-7 Anxiety Score',    10, '#4a90d9'),
]:
    ax.hist(df[col].dropna(), bins=range(0, int(df[col].max())+2),
            color=color, alpha=0.82, edgecolor='white', linewidth=0.6)
    ax.axvline(cutoff, color='#222', linestyle='--', linewidth=1.8,
               label=f'Clinical cutoff (>={cutoff})')
    ax.set_title(f'{label} Distribution', fontsize=13, fontweight='bold', pad=10)
    ax.set_xlabel('Score', fontsize=11)
    ax.set_ylabel('Number of Respondents', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.4)
plt.suptitle(f'Clinical Score Distributions  (n = {n})', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/01_score_distributions.png', dpi=200, bbox_inches='tight')
plt.close()
print('Saved: 01_score_distributions.png')

# ── Plot 2: Risk Prevalence ───────────────────────────────────────────
dep_pct  = df['dep_risk'].mean() * 100
anx_pct  = df['anx_risk'].mean() * 100
both_pct = ((df['dep_risk'] == 1) & (df['anx_risk'] == 1)).mean() * 100

fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
categories = ['Depression Risk\n(PHQ-9 >= 10)', 'Anxiety Risk\n(GAD-7 >= 10)', 'Both Conditions\nComorbid']
values     = [dep_pct, anx_pct, both_pct]
colors     = ['#e05c5c', '#4a90d9', '#9b59b6']
bars = ax.bar(categories, values, color=colors, alpha=0.88, edgecolor='white', linewidth=0.7, width=0.55)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{v:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_ylim(0, max(values) + 16)
ax.set_ylabel('Prevalence (%)', fontsize=12)
ax.set_title(f'Mental Health Risk Prevalence  (n = {n})', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.35)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/02_risk_prevalence.png', dpi=200, bbox_inches='tight')
plt.close()
print('Saved: 02_risk_prevalence.png')

# ── Plot 3: Demographics ──────────────────────────────────────────────
demo_info = {
    'b1_gender':            'Gender',
    'b3_university_type':   'University Type',
    'b4_discipline':        'Discipline',
    'b5_cgpa':              'CGPA Bracket',
    'b6_graduation_status': 'Graduation Status',
    'b2_age':               'Age Group',
}
fig, axes = plt.subplots(2, 3, figsize=(16, 9), dpi=150)
axes = axes.flatten()
palette = sns.color_palette('Set2', 8)
for idx, (col, title) in enumerate(demo_info.items()):
    if col not in df.columns:
        continue
    counts = df[col].value_counts()
    labels = [str(l)[:32] for l in counts.index]
    axes[idx].barh(labels, counts.values, color=palette[:len(counts)])
    axes[idx].set_title(title, fontsize=11, fontweight='bold')
    axes[idx].set_xlabel('Count', fontsize=9)
    for i, v in enumerate(counts.values):
        axes[idx].text(v + 0.15, i, str(v), va='center', fontsize=9)
plt.suptitle(f'Demographic Profile of Sample  (n = {n})', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/03_demographics.png', dpi=200, bbox_inches='tight')
plt.close()
print('Saved: 03_demographics.png')

# ── Plot 4: PHQ-9 vs GAD-7 Scatter ───────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
palette_risk = {'Both Risk': '#9b59b6', 'Dep Only': '#e05c5c',
                'Anx Only': '#4a90d9', 'No Risk': '#95a5a6'}
def risk_label(row):
    if row['dep_risk'] == 1 and row['anx_risk'] == 1: return 'Both Risk'
    if row['dep_risk'] == 1: return 'Dep Only'
    if row['anx_risk'] == 1: return 'Anx Only'
    return 'No Risk'
df['risk_group'] = df.apply(risk_label, axis=1)
for label, grp in df.groupby('risk_group'):
    ax.scatter(grp['phq9_total'], grp['gad7_total'],
               label=f'{label} (n={len(grp)})', color=palette_risk[label],
               alpha=0.75, s=60, edgecolors='white', linewidths=0.5)
ax.axvline(10, color='#e05c5c', linestyle='--', linewidth=1.5, alpha=0.65)
ax.axhline(10, color='#4a90d9', linestyle='--', linewidth=1.5, alpha=0.65)
ax.set_xlabel('PHQ-9 Total Score (Depression)', fontsize=12)
ax.set_ylabel('GAD-7 Total Score (Anxiety)', fontsize=12)
ax.set_title(f'PHQ-9 vs GAD-7 by Risk Class  (n = {n})', fontsize=13, fontweight='bold')
ax.legend(fontsize=10, frameon=True)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/04_phq9_vs_gad7_scatter.png', dpi=200, bbox_inches='tight')
plt.close()
print('Saved: 04_phq9_vs_gad7_scatter.png')

# ── Plot 5: Correlation Heatmap ───────────────────────────────────────
corr_subset = df[phq_cols + gad_cols + ['phq9_total', 'gad7_total', 'mspss_total']].corr()
fig, ax = plt.subplots(figsize=(13, 10), dpi=150)
mask = np.triu(np.ones_like(corr_subset, dtype=bool))
sns.heatmap(corr_subset, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, linewidths=0.3, ax=ax, annot_kws={'size': 7},
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Heatmap — PHQ-9, GAD-7 Items + Totals + MSPSS',
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{FIGURES_DIR}/05_correlation_heatmap.png', dpi=200, bbox_inches='tight')
plt.close()
print('Saved: 05_correlation_heatmap.png')

print('\nAll 5 plots saved to figures/')
print('DONE.')
