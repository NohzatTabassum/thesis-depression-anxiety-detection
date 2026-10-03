"""
Phase 4: Full Data Audit, Quality Control & Exploratory Data Analysis
----------------------------------------------------------------------
Run:  python src/phase4_eda.py
Output: figures/ directory (PNG plots), data/processed/clean_df.csv
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # headless — no display needed
import matplotlib.pyplot as plt
import seaborn as sns

# ── Paths ──────────────────────────────────────────────────────────────
RAW_CSV     = "data/raw/survey_responses.csv"
CLEAN_CSV   = "data/processed/clean_df.csv"
FIGURES_DIR = "figures"
os.makedirs("data/processed", exist_ok=True)
os.makedirs(FIGURES_DIR,       exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")

# ══════════════════════════════════════════════════════════════════════
# 1. LOAD
# ══════════════════════════════════════════════════════════════════════
print("=" * 60)
print("PHASE 4 — DATA AUDIT & EDA")
print("=" * 60)

df_raw = pd.read_csv(RAW_CSV, encoding="utf-8-sig")
print(f"\n[1] Raw shape: {df_raw.shape}  ({df_raw.shape[0]} responses, {df_raw.shape[1]} columns)")

# ══════════════════════════════════════════════════════════════════════
# 2. COLUMN RENAMING — short machine-friendly names
# ══════════════════════════════════════════════════════════════════════
col_map = {
    df_raw.columns[0]:  "timestamp",
    df_raw.columns[1]:  "consent",
    df_raw.columns[2]:  "b1_gender",
    df_raw.columns[3]:  "b2_age",
    df_raw.columns[4]:  "b3_university_type",
    df_raw.columns[5]:  "b4_discipline",
    df_raw.columns[6]:  "b5_cgpa",
    df_raw.columns[7]:  "b6_graduation_status",
    df_raw.columns[8]:  "b7_income",
    df_raw.columns[9]:  "b8_financial_pressure",
    df_raw.columns[10]: "c1_search_duration",
    df_raw.columns[11]: "c2_apps_per_week",
    df_raw.columns[12]: "c3_hrs_per_week",
    df_raw.columns[13]: "c4_late_night",
    df_raw.columns[14]: "c5_platforms",
    df_raw.columns[15]: "c6_rejections",
    df_raw.columns[16]: "c7_ghosting_rate",
    df_raw.columns[17]: "c8_interview_invites",
    df_raw.columns[18]: "c9_cv_customization",
    df_raw.columns[19]: "c10_peer_comparison",
    df_raw.columns[20]: "c11_family_pressure",
    df_raw.columns[21]: "c12_stigma_fear",
    df_raw.columns[22]: "c13_hopelessness",
    df_raw.columns[23]: "c14_screen_time",
    df_raw.columns[24]: "d1_mspss",
    df_raw.columns[25]: "d2_mspss",
    df_raw.columns[26]: "d3_mspss",
    df_raw.columns[27]: "d4_mspss",
    df_raw.columns[28]: "d5_mspss",
    df_raw.columns[29]: "d6_mspss",
    df_raw.columns[30]: "d7_mspss",
    df_raw.columns[31]: "d8_mspss",
    df_raw.columns[32]: "d9_mspss",
    df_raw.columns[33]: "d10_mspss",
    df_raw.columns[34]: "d11_mspss",
    df_raw.columns[35]: "d12_mspss",
    df_raw.columns[36]: "e1_phq9",
    df_raw.columns[37]: "e2_phq9",
    df_raw.columns[38]: "e3_phq9",
    df_raw.columns[39]: "e4_phq9",
    df_raw.columns[40]: "e5_phq9",
    df_raw.columns[41]: "e6_phq9",
    df_raw.columns[42]: "e7_phq9",
    df_raw.columns[43]: "e8_phq9",
    df_raw.columns[44]: "e9_phq9",
    df_raw.columns[45]: "f1_gad7",
    df_raw.columns[46]: "f2_gad7",
    df_raw.columns[47]: "f3_gad7",
    df_raw.columns[48]: "f4_gad7",
    df_raw.columns[49]: "f5_gad7",
    df_raw.columns[50]: "f6_gad7",
    df_raw.columns[51]: "f7_gad7",
    df_raw.columns[52]: "g1_attention",
}
df = df_raw.rename(columns=col_map).drop(columns=["timestamp"], errors="ignore")
print(f"    Renamed {len(col_map)} columns to short IDs.\n")

# ══════════════════════════════════════════════════════════════════════
# 3. QUALITY CONTROL — Step by step
# ══════════════════════════════════════════════════════════════════════
audit = {"start": len(df)}

# 3a. Keep only consenting respondents
df = df[df["consent"].str.contains("সম্মতি|consent|Yes|হ্যাঁ", case=False, na=False)]
audit["non_consent_removed"] = audit["start"] - len(df)
print(f"[3a] Non-consent removed : {audit['non_consent_removed']}  → Remaining: {len(df)}")

# 3b. Attention Check — correct answer is option 4
# The value should contain "4" or "Somewhat Agree"
attn_pass = df["g1_attention"].astype(str).str.contains("4|Somewhat", case=False, na=False)
audit["attention_fail"] = (~attn_pass).sum()
df = df[attn_pass]
print(f"[3b] Attention check fail: {audit['attention_fail']}  → Remaining: {len(df)}")

# 3c. PHQ-9 & GAD-7: parse numeric scores from text options
# Options look like: "0 = Not at all (একেবারেই না)" → extract leading digit
phq_cols = [f"e{i}_phq9" for i in range(1, 10)]
gad_cols = [f"f{i}_gad7" for i in range(1, 8)]
mspss_cols = [f"d{i}_mspss" for i in range(1, 13)]
likert5_cols = [f"c{i}" for i in [9, 10, 11, 12, 13]]
likert5_full = [f"c{i}_{s}" for i, s in zip(
    [9, 10, 11, 12, 13],
    ["cv_customization", "peer_comparison", "family_pressure", "stigma_fear", "hopelessness"]
)]

def extract_leading_int(series):
    """Extract the leading digit from text like '2 = More than half the days'"""
    return pd.to_numeric(series.astype(str).str.extract(r"^(\d)")[0], errors="coerce")

for col in phq_cols + gad_cols:
    df[col] = extract_leading_int(df[col])

# MSPSS is already numeric (scale 1-7)
for col in mspss_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# C9-C13 Likert 1-5
for col in likert5_full:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 3d. Missing value check after parsing
missing_pct = df[phq_cols + gad_cols].isnull().mean(axis=1)
high_missing = missing_pct > 0.20
audit["high_missing_removed"] = high_missing.sum()
df = df[~high_missing].reset_index(drop=True)
print(f"[3c] High-missing (>20%) : {audit['high_missing_removed']}  → Remaining: {len(df)}")

# 3e. Straight-lining: zero variance across all PHQ-9 items
phq_std = df[phq_cols].std(axis=1)
gad_std = df[gad_cols].std(axis=1)
straight_liners = (phq_std == 0) & (gad_std == 0)
audit["straight_liners_removed"] = straight_liners.sum()
df = df[~straight_liners].reset_index(drop=True)
print(f"[3d] Straight-liners     : {audit['straight_liners_removed']}  → Remaining: {len(df)}")

audit["final_clean"] = len(df)
print(f"\n✅ QUALITY AUDIT SUMMARY")
print(f"   Started with       : {audit['start']}")
print(f"   Non-consent        : -{audit['non_consent_removed']}")
print(f"   Attention fail     : -{audit['attention_fail']}")
print(f"   High missing       : -{audit['high_missing_removed']}")
print(f"   Straight-liners    : -{audit['straight_liners_removed']}")
print(f"   ─────────────────────")
print(f"   FINAL CLEAN SAMPLE : {audit['final_clean']} respondents")

# ══════════════════════════════════════════════════════════════════════
# 4. COMPUTE CLINICAL SCORES & RISK TARGETS
# ══════════════════════════════════════════════════════════════════════
df["phq9_total"] = df[phq_cols].sum(axis=1)
df["gad7_total"] = df[gad_cols].sum(axis=1)
df["mspss_total"] = df[mspss_cols].mean(axis=1)

df["dep_risk"] = (df["phq9_total"] >= 10).astype(int)
df["anx_risk"] = (df["gad7_total"] >= 10).astype(int)

dep_prev  = df["dep_risk"].mean() * 100
anx_prev  = df["anx_risk"].mean() * 100
both_prev = ((df["dep_risk"] == 1) & (df["anx_risk"] == 1)).mean() * 100

print(f"\n[4] CLINICAL SCORE SUMMARY")
print(f"   PHQ-9 range  : {df['phq9_total'].min():.0f} – {df['phq9_total'].max():.0f}  |  Mean: {df['phq9_total'].mean():.2f}  |  SD: {df['phq9_total'].std():.2f}")
print(f"   GAD-7 range  : {df['gad7_total'].min():.0f} – {df['gad7_total'].max():.0f}  |  Mean: {df['gad7_total'].mean():.2f}  |  SD: {df['gad7_total'].std():.2f}")
print(f"   MSPSS mean   : {df['mspss_total'].mean():.2f}  |  SD: {df['mspss_total'].std():.2f}")
print(f"\n   Depression risk (PHQ-9 ≥ 10) : {df['dep_risk'].sum()} / {len(df)}  ({dep_prev:.1f}%)")
print(f"   Anxiety risk   (GAD-7 ≥ 10) : {df['anx_risk'].sum()} / {len(df)}  ({anx_prev:.1f}%)")
print(f"   Both depression & anxiety    : {((df['dep_risk']==1)&(df['anx_risk']==1)).sum()} / {len(df)}  ({both_prev:.1f}%)")

# ══════════════════════════════════════════════════════════════════════
# 5. SAVE CLEAN DATASET
# ══════════════════════════════════════════════════════════════════════
df.to_csv(CLEAN_CSV, index=False, encoding="utf-8-sig")
print(f"\n[5] Clean dataset saved → {CLEAN_CSV}")

# ══════════════════════════════════════════════════════════════════════
# 6. PLOTS
# ══════════════════════════════════════════════════════════════════════
print("\n[6] Generating plots...")

# ── Plot 1: PHQ-9 & GAD-7 Score Distributions ──────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=150)

for ax, col, label, cutoff, color in [
    (axes[0], "phq9_total", "PHQ-9 Depression Score",  10, "#e05c5c"),
    (axes[1], "gad7_total", "GAD-7 Anxiety Score",     10, "#4a90d9"),
]:
    ax.hist(df[col], bins=range(0, df[col].max()+2), color=color, alpha=0.82, edgecolor="white", linewidth=0.6)
    ax.axvline(cutoff, color="#222", linestyle="--", linewidth=1.8, label=f"Clinical cutoff (≥{cutoff})")
    ax.set_title(f"{label} Distribution", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Score", fontsize=11)
    ax.set_ylabel("Number of Respondents", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.4)

plt.suptitle(f"Clinical Score Distributions  (n = {len(df)})", fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/01_score_distributions.png", dpi=200, bbox_inches="tight")
plt.close()
print("   ✔ 01_score_distributions.png")

# ── Plot 2: Risk Prevalence Bar Chart ──────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
categories = ["Depression Risk\n(PHQ-9 ≥ 10)", "Anxiety Risk\n(GAD-7 ≥ 10)", "Both Conditions\nComorbid"]
values     = [dep_prev, anx_prev, both_prev]
colors     = ["#e05c5c", "#4a90d9", "#9b59b6"]
bars = ax.bar(categories, values, color=colors, alpha=0.88, edgecolor="white", linewidth=0.7, width=0.55)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"{v:.1f}%",
            ha="center", va="bottom", fontsize=12, fontweight="bold")
ax.set_ylim(0, max(values) + 14)
ax.set_ylabel("Prevalence (%)", fontsize=12)
ax.set_title(f"Mental Health Risk Prevalence  (n = {len(df)})", fontsize=13, fontweight="bold")
ax.grid(axis="y", alpha=0.35)
plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/02_risk_prevalence.png", dpi=200, bbox_inches="tight")
plt.close()
print("   ✔ 02_risk_prevalence.png")

# ── Plot 3: Demographics ───────────────────────────────────────────
demo_cols = {
    "b1_gender":            "Gender",
    "b3_university_type":   "University Type",
    "b4_discipline":        "Discipline",
    "b5_cgpa":              "CGPA Bracket",
    "b6_graduation_status": "Graduation Status",
}

fig, axes = plt.subplots(2, 3, figsize=(16, 9), dpi=150)
axes = axes.flatten()

for idx, (col, title) in enumerate(demo_cols.items()):
    if col not in df.columns:
        continue
    counts = df[col].value_counts()
    labels = [l[:30] for l in counts.index]  # truncate long labels
    axes[idx].barh(labels, counts.values, color=sns.color_palette("Set2", len(counts)))
    axes[idx].set_title(title, fontsize=11, fontweight="bold")
    axes[idx].set_xlabel("Count", fontsize=9)
    for i, v in enumerate(counts.values):
        axes[idx].text(v + 0.2, i, str(v), va="center", fontsize=9)

# Financial pressure distribution in last subplot
if "b8_financial_pressure" in df.columns:
    fp = pd.to_numeric(df["b8_financial_pressure"], errors="coerce").dropna()
    axes[5].bar(fp.value_counts().sort_index().index.astype(str),
                fp.value_counts().sort_index().values,
                color=sns.color_palette("OrRd", 5))
    axes[5].set_title("Financial Pressure (1-5)", fontsize=11, fontweight="bold")
    axes[5].set_xlabel("Scale", fontsize=9)

plt.suptitle(f"Demographic Profile of Sample  (n = {len(df)})", fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/03_demographics.png", dpi=200, bbox_inches="tight")
plt.close()
print("   ✔ 03_demographics.png")

# ── Plot 4: Correlation Heatmap ────────────────────────────────────
numeric_cols = phq_cols + gad_cols + mspss_cols[:6]  # subset for readability
corr_df = df[numeric_cols + ["phq9_total", "gad7_total"]].corr()

fig, ax = plt.subplots(figsize=(14, 11), dpi=150)
mask = np.triu(np.ones_like(corr_df, dtype=bool))
sns.heatmap(corr_df, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, linewidths=0.4, ax=ax, annot_kws={"size": 7},
            cbar_kws={"shrink": 0.8})
ax.set_title("Correlation Heatmap — PHQ-9, GAD-7, MSPSS Items", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/04_correlation_heatmap.png", dpi=200, bbox_inches="tight")
plt.close()
print("   ✔ 04_correlation_heatmap.png")

# ── Plot 5: PHQ-9 vs GAD-7 Scatter ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
risk_labels = df.apply(lambda r: "Both Risk" if r.dep_risk==1 and r.anx_risk==1
                        else ("Dep Risk" if r.dep_risk==1
                        else ("Anx Risk" if r.anx_risk==1 else "No Risk")), axis=1)
palette = {"Both Risk": "#9b59b6", "Dep Risk": "#e05c5c", "Anx Risk": "#4a90d9", "No Risk": "#95a5a6"}
for label, grp in df.groupby(risk_labels):
    ax.scatter(grp["phq9_total"], grp["gad7_total"], label=label,
               color=palette[label], alpha=0.75, s=55, edgecolors="white", linewidths=0.4)
ax.axvline(10, color="#e05c5c", linestyle="--", linewidth=1.5, alpha=0.7, label="PHQ-9 cutoff=10")
ax.axhline(10, color="#4a90d9", linestyle="--", linewidth=1.5, alpha=0.7, label="GAD-7 cutoff=10")
ax.set_xlabel("PHQ-9 Total Score (Depression)", fontsize=12)
ax.set_ylabel("GAD-7 Total Score (Anxiety)", fontsize=12)
ax.set_title("PHQ-9 vs GAD-7 Score Distribution by Risk Class", fontsize=13, fontweight="bold")
ax.legend(fontsize=10, frameon=True)
ax.grid(alpha=0.35)
plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/05_phq9_vs_gad7_scatter.png", dpi=200, bbox_inches="tight")
plt.close()
print("   ✔ 05_phq9_vs_gad7_scatter.png")

print("\n" + "="*60)
print("PHASE 4 COMPLETE ✅")
print(f"Clean CSV  → data/processed/clean_df.csv")
print(f"Figures    → figures/ (5 plots saved)")
print("="*60)
