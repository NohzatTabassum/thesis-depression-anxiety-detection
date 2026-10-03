import sys, os
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import numpy as np

RAW_CSV   = 'data/raw/survey_responses.csv'
CLEAN_CSV = 'data/processed/clean_df.csv'
os.makedirs('data/processed', exist_ok=True)

df_raw = pd.read_csv(RAW_CSV, encoding='utf-8-sig')
print(f'Raw shape: {df_raw.shape}')

col_map = {
    df_raw.columns[0]:  'timestamp',
    df_raw.columns[1]:  'consent',
    df_raw.columns[2]:  'b1_gender',
    df_raw.columns[3]:  'b2_age',
    df_raw.columns[4]:  'b3_university_type',
    df_raw.columns[5]:  'b4_discipline',
    df_raw.columns[6]:  'b5_cgpa',
    df_raw.columns[7]:  'b6_graduation_status',
    df_raw.columns[8]:  'b7_income',
    df_raw.columns[9]:  'b8_financial_pressure',
    df_raw.columns[10]: 'c1_search_duration',
    df_raw.columns[11]: 'c2_apps_per_week',
    df_raw.columns[12]: 'c3_hrs_per_week',
    df_raw.columns[13]: 'c4_late_night',
    df_raw.columns[14]: 'c5_platforms',
    df_raw.columns[15]: 'c6_rejections',
    df_raw.columns[16]: 'c7_ghosting_rate',
    df_raw.columns[17]: 'c8_interview_invites',
    df_raw.columns[18]: 'c9_cv_customization',
    df_raw.columns[19]: 'c10_peer_comparison',
    df_raw.columns[20]: 'c11_family_pressure',
    df_raw.columns[21]: 'c12_stigma_fear',
    df_raw.columns[22]: 'c13_hopelessness',
    df_raw.columns[23]: 'c14_screen_time',
    df_raw.columns[24]: 'd1_mspss', df_raw.columns[25]: 'd2_mspss',
    df_raw.columns[26]: 'd3_mspss', df_raw.columns[27]: 'd4_mspss',
    df_raw.columns[28]: 'd5_mspss', df_raw.columns[29]: 'd6_mspss',
    df_raw.columns[30]: 'd7_mspss', df_raw.columns[31]: 'd8_mspss',
    df_raw.columns[32]: 'd9_mspss', df_raw.columns[33]: 'd10_mspss',
    df_raw.columns[34]: 'd11_mspss', df_raw.columns[35]: 'd12_mspss',
    df_raw.columns[36]: 'e1_phq9',  df_raw.columns[37]: 'e2_phq9',
    df_raw.columns[38]: 'e3_phq9',  df_raw.columns[39]: 'e4_phq9',
    df_raw.columns[40]: 'e5_phq9',  df_raw.columns[41]: 'e6_phq9',
    df_raw.columns[42]: 'e7_phq9',  df_raw.columns[43]: 'e8_phq9',
    df_raw.columns[44]: 'e9_phq9',
    df_raw.columns[45]: 'f1_gad7',  df_raw.columns[46]: 'f2_gad7',
    df_raw.columns[47]: 'f3_gad7',  df_raw.columns[48]: 'f4_gad7',
    df_raw.columns[49]: 'f5_gad7',  df_raw.columns[50]: 'f6_gad7',
    df_raw.columns[51]: 'f7_gad7',
    df_raw.columns[52]: 'g1_attention',
}

df = df_raw.rename(columns=col_map).drop(columns=['timestamp'], errors='ignore')

# ----- QUALITY FILTERS -----
n0 = len(df)

# Consent
df = df[df['consent'].str.contains('consent|Yes', case=False, na=False)]
n_consent = n0 - len(df)
print(f'Non-consent removed: {n_consent}, remaining: {len(df)}')

# Attention check
attn_pass = df['g1_attention'].astype(str).str.contains('4|Somewhat', case=False, na=False)
n_attn = int((~attn_pass).sum())
df = df[attn_pass]
print(f'Attention fail: {n_attn}, remaining: {len(df)}')

# Parse scores
phq_cols  = [f'e{i}_phq9' for i in range(1, 10)]
gad_cols  = [f'f{i}_gad7' for i in range(1, 8)]
mspss_cols = [f'd{i}_mspss' for i in range(1, 13)]

for col in phq_cols + gad_cols:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.extract(r'^(\d)')[0], errors='coerce'
    )
for col in mspss_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Missing value filter
miss = df[phq_cols + gad_cols].isnull().mean(axis=1)
n_miss = int((miss > 0.20).sum())
df = df[miss <= 0.20].reset_index(drop=True)
print(f'High-missing removed: {n_miss}, remaining: {len(df)}')

# Straight-lining
sl = (df[phq_cols].std(axis=1) == 0) & (df[gad_cols].std(axis=1) == 0)
n_sl = int(sl.sum())
df = df[~sl].reset_index(drop=True)
print(f'Straight-liners: {n_sl}, FINAL CLEAN: {len(df)}')

# ----- SCORES & TARGETS -----
df['phq9_total']  = df[phq_cols].sum(axis=1)
df['gad7_total']  = df[gad_cols].sum(axis=1)
df['mspss_total'] = df[mspss_cols].mean(axis=1)
df['dep_risk'] = (df['phq9_total'] >= 10).astype(int)
df['anx_risk'] = (df['gad7_total'] >= 10).astype(int)

p_mean = df['phq9_total'].mean()
p_std  = df['phq9_total'].std()
p_min  = df['phq9_total'].min()
p_max  = df['phq9_total'].max()
g_mean = df['gad7_total'].mean()
g_std  = df['gad7_total'].std()
g_min  = df['gad7_total'].min()
g_max  = df['gad7_total'].max()
m_mean = df['mspss_total'].mean()
m_std  = df['mspss_total'].std()

dep_n   = int(df['dep_risk'].sum())
dep_pct = df['dep_risk'].mean() * 100
anx_n   = int(df['anx_risk'].sum())
anx_pct = df['anx_risk'].mean() * 100
both_n  = int(((df['dep_risk'] == 1) & (df['anx_risk'] == 1)).sum())
both_pct = ((df['dep_risk'] == 1) & (df['anx_risk'] == 1)).mean() * 100

print()
print(f'PHQ-9  | Mean={p_mean:.2f}  SD={p_std:.2f}  Range={p_min:.0f}-{p_max:.0f}')
print(f'GAD-7  | Mean={g_mean:.2f}  SD={g_std:.2f}  Range={g_min:.0f}-{g_max:.0f}')
print(f'MSPSS  | Mean={m_mean:.2f}  SD={m_std:.2f}')
print()
print(f'Depression risk (PHQ9>=10): {dep_n} / {len(df)} = {dep_pct:.1f}%')
print(f'Anxiety risk   (GAD7>=10): {anx_n} / {len(df)} = {anx_pct:.1f}%')
print(f'Both conditions comorbid : {both_n} / {len(df)} = {both_pct:.1f}%')
print()
print('dep_risk distribution:', df['dep_risk'].value_counts().to_dict())
print('anx_risk distribution:', df['anx_risk'].value_counts().to_dict())

df.to_csv(CLEAN_CSV, index=False, encoding='utf-8-sig')
print(f'\nSaved clean CSV -> {CLEAN_CSV}')
print('DONE.')
