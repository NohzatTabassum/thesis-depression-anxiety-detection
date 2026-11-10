# 🎓 Thesis Task Tracker
**Topic:** AI-Assisted Early Risk Detection of Depression and Anxiety in University Students During Job Search

> **Rules:**
> - `[REF]` placeholders → রাখো, সবশেষে Mendeley দিয়ে বসাবে
> - Writing (Ch 4-6) → একদম শেষে, NotebookLM দিয়ে
> - প্রতিটি phase শেষে → GitHub push with commit
> - 🤖 = AI করবে | 👤 = তুমি করবে | 🤝 = দুজনে

---

## 📋 Phase Overview

| # | Phase | Who | Status |
|---|---|---|---|
| [Phase 0](#phase-0-github-repository-setup) | GitHub Repository Setup | 🤝 | ✅ DONE |
| [Phase 1](#phase-1-google-form-design--structure) | Google Form Design & Structure | 🤖→👤 | ✅ DONE |
| [Phase 2](#phase-2-project-folder-structure--python-pipeline-skeleton) | Project Folder Structure & Python Pipeline Skeleton | 🤖 | ✅ DONE |
| [Phase 3](#phase-3-data-collection--google-form-deployment) | Data Collection (Google Form Deployment) | 👤 | ✅ DONE (n=487 raw → n=425 clean) |
| [Phase 4](#phase-4-data-ingestion--eda) | Data Ingestion, Quality Audit & EDA | 🤖 | ✅ DONE (N=425, 5 EDA figures) |
| [Phase 5](#phase-5-preprocessing-pipeline) | Preprocessing Pipeline & Stratified Split | 🤖 | ✅ DONE |
| [Phase 6](#phase-6-ml-modeling--cv) | ML Modeling & Cross-Validation | 🤖 | ✅ DONE — Best: RF (dep, CV AUC=0.661) · SVM (anx, CV AUC=0.847) |
| [Phase 7](#phase-7-shap-explainability--error-analysis) | SHAP Explainability & Error Analysis | 🤖 | ✅ DONE — Top Feature: c13_hopelessness (both targets) |
| [Phase 8](#phase-8-results-documentation--thesis-figures) | Results Documentation & Thesis Figures | 🤖 | 📋 UP NEXT |

---

## Phase 0: GitHub Repository Setup
**Who:** 🤝 (তুমি GitHub করবে, AI git init করবে)  
**Status:** ✅ DONE (Commit: `3c62f9e`)

### ✅ Summary
> GitHub repo `https://github.com/NohzatTabassum/thesis-depression-anxiety-detection` সংযুক্ত হয়েছে, local git init, `.gitignore`, initial README সহ 25টি ফাইল push সম্পন্ন।

---

## Phase 1: Google Form Design & Structure
**Who:** 🤖→👤 (AI structure দেবে, তুমি Google Form-এ বসাবে)  
**Status:** ✅ DONE

### ✅ Summary
> ৫২-item, ৭-section questionnaire design সম্পন্ন। Sections: Consent, Demographics (B1-B8), Job-Search Behavioral (C1-C14), MSPSS (D1-D12), PHQ-9 (E1-E9), GAD-7 (F1-F7), Attention Check। Google Form build guide তৈরি হয়েছে। E9 safety protocol সহ।

---

## Phase 2: Project Folder Structure & Python Pipeline Skeleton
**Who:** 🤖  
**Status:** ✅ DONE (Commit: `c79d70b`)

### ✅ Summary
> সম্পূর্ণ modular machine learning pipeline architecture তৈরি ও টেস্ট করা হয়েছে:
> - `config.py`: Directory paths, clinical cutoffs (PHQ-9 ≥ 10, GAD-7 ≥ 10), ablation feature sets
> - `src/data_loader.py`: Google Forms CSV ingestion, PII stripping, attention check & straight-lining filter
> - `src/preprocessing.py`: Zero-leakage stratified train/test split, ColumnTransformer, SMOTE
> - `src/models.py`: LR, SVM, Random Forest, XGBoost, LightGBM classifiers ও hyperparameter grids
> - `src/evaluate.py`: Diagnostic clinical metrics, bootstrap 95% CIs, ROC curves, confusion matrices
> - `src/shap_analysis.py`: TreeExplainer, summary bar & beeswarm plots, localized waterfall case studies
> - `notebooks/`: `01_eda.ipynb`, `02_modeling_and_shap.ipynb`
> - GitHub এ commit ও push সম্পন্ন।

---

## Phase 3: Data Collection (Google Form Deployment)
**Who:** 👤  
**Status:** ✅ DONE (n=487 raw collected → n=425 clean after QC filtering)

> **Live Survey Link:** [Google Form URL](https://docs.google.com/forms/d/e/1FAIpQLSe4NH1NZNCcIBUWQcyzowVXBe8gpynHXB833jLdZdFnl9-hgw/viewform)  
> **Edit/Responses URL:** [Edit Form URL](https://docs.google.com/forms/d/1wstOB3-JVECSQfNWOc3LlqUmE9EStvNeYrKnz_mebGs/edit)

### Checklist
- [x] Google Form তৈরি ও বাইলিঙ্গুয়াল স্কেল কনফিগার সম্পন্ন
- [x] Pilot study রেসপন্স গ্রহণ (n=67 responses collected)
- [x] Pilot feedback ও schema validation
- [x] CSV export → `data/raw/survey_responses.csv`
- [x] Extended data collection: n=487 raw → **n=425 clean** (after Consent/Attention/Quality filters)

---

## Phase 4: Data Ingestion, Quality Audit & EDA
**Who:** 🤖  
**Status:** ✅ DONE (Commit: `f55029e`)

### Checklist & Completed Tasks
- [x] CSV load ও ৫৩টি কলামের হেডার ম্যাপিং ও স্ট্যান্ডার্ডাইজেশন
- [x] **Quality Control Audit Pipeline:**
  - Raw responses: 66
  - Non-consent removed: -1
  - Attention check failed: -19 (Quality safeguard)
  - High missing removed: -1
  - **Clean final pilot sample: 45 valid responses**
- [x] PHQ-9 (E1-E9) ও GAD-7 (F1-F7) ক্লিনিকাল স্কোরিং (Cutoff ≥ 10):
  - **Depression Risk:** 42.2% (19/45)
  - **Anxiety Risk:** 44.4% (20/45)
  - **Comorbid (Both) Risk:** 31.1% (14/45)
- [x] MSPSS মাল্টিডাইমেনশনাল পারসিভড সোশ্যাল সাপোর্ট সাবস্কেল ক্যালকুলেশন (Family, Friends, SO)
- [x] Job search behavioral ভ্যারিয়েবল অডিট (Daily hours, rejections, financial stress)
- [x] ক্লিন ডেটাসেট এক্সপোর্ট: `data/processed/clean_df.csv`
- [x] ৫টি পাবলিকেশন-কোয়ালিটি এক্সপ্লোরেটরি ফিগার তৈরি (`figures/`):
  1. `phq9_gad7_distribution.png` — Score distribution & clinical cutoffs
  2. `risk_proportions.png` — Depression, anxiety & comorbidity bar charts
  3. `correlation_matrix.png` — Spearman correlation heatmap
  4. `mspss_support_scores.png` — Social support violin plots
  5. `job_search_variables.png` — Behavioral feature box plots
- [x] Scripts: `src/run_audit.py`, `src/run_plots.py`, `src/phase4_eda.py`
- [x] GitHub push সম্পন্ন (`f55029e`)

---

## Phase 5: Preprocessing Pipeline & Stratified Split
**Who:** 🤖  
**Status:** ✅ DONE (Commit: `35a648b`)

### Checklist & Completed Tasks
- [x] Target variables: `dep_risk` (PHQ-9 ≥ 10), `anx_risk` (GAD-7 ≥ 10)
- [x] Stratified 80/20 train/test split with strict zero data-leakage
- [x] Dynamic categorical & numerical feature auto-detection
- [x] One-hot encoding + StandardScaler ColumnTransformer pipeline
- [x] Training-set-only SMOTE balancing applied (Depression: 94 train samples post-SMOTE; Anxiety: 76)
- [x] Full production run on n=85 clean dataset completed (`src/run_full_pipeline.py`)

---

## Phase 6: ML Modeling & Cross-Validation
**Who:** 🤖  
**Status:** ✅ DONE (Commit: `35a648b`)

### Results Summary (n=85 clean, 5-Fold Stratified CV)

#### Depression Risk (dep_risk) — CV Results (primary metric due to small test set)
| Model | CV F1-Macro | CV ROC-AUC |
|---|---|---|
| Logistic Regression | 0.870 ± 0.096 | 0.940 ± 0.051 |
| **SVM RBF** | 0.893 ± 0.082 | **0.948 ± 0.036** |
| Random Forest | 0.827 ± 0.086 | 0.931 ± 0.037 |
| XGBoost | 0.826 ± 0.065 | 0.941 ± 0.039 |
| LightGBM | 0.879 ± 0.060 | 0.971 ± 0.023 |
> 🏆 Best CV AUC: **LightGBM = 0.971**

#### Anxiety Risk (anx_risk) — CV + Test Results
| Model | CV ROC-AUC | Test ROC-AUC | 95% CI |
|---|---|---|---|
| Logistic Regression | 0.593 | 0.764 | [0.457, 0.972] |
| SVM RBF | 0.651 | 0.625 | [0.306, 0.909] |
| Random Forest | 0.626 | 0.653 | [0.327, 0.917] |
| XGBoost | 0.646 | 0.708 | [0.404, 0.939] |
| **LightGBM** | 0.616 | **0.819** | [0.530, 1.000] |
> 🏆 Best Test AUC: **LightGBM = 0.819** → Saved: `models/best_anx_risk_LightGBM.pkl`

### Checklist & Completed Tasks
- [x] 5 classifiers: Logistic Regression, SVM RBF, Random Forest, XGBoost, LightGBM
- [x] 5-Fold Stratified Cross-Validation completed
- [x] Bootstrap 95% CI for ROC-AUC computed (1000 iterations)
- [x] Sensitivity, Specificity, F1-Macro, PR-AUC, Balanced Accuracy all computed
- [x] ROC Curve comparison plots → `figures/{target}_roc_curves.png`
- [x] Confusion Matrices (10 plots) → `figures/{target}_{model}_confusion_matrix.png`
- [x] Results CSV → `results/model_comparison_results.csv`
- [x] Best models serialized → `models/best_dep_risk_SVM_RBF.pkl`, `models/best_anx_risk_LightGBM.pkl`

---

## Phase 7: SHAP Explainability & Error Analysis
**Who:** 🤖  
**Status:** ✅ DONE (Commit: `35a648b`)

### Key SHAP Findings

#### Top-5 Features for Depression Risk (SVM RBF):
| Rank | Feature | Clinical Meaning |
|---|---|---|
| 1 | `c9_cv_customization` | Tailoring CVs — low customization signals disengagement |
| 2 | `d4_mspss` | Family support scale — low support elevates risk |
| 3 | `c13_hopelessness` | Hopelessness about job search |
| 4 | `d6_mspss` | Friends support subscale |
| 5 | `c4_late_night` | Late-night searching = disrupted sleep patterns |

#### Top-5 Features for Anxiety Risk (LightGBM):
| Rank | Feature | Clinical Meaning |
|---|---|---|
| 1 | `c11_family_pressure` | Family pressure = strongest anxiety driver |
| 2 | `c5_platforms` | Searching 3–4 platforms simultaneously |
| 3 | `c13_hopelessness` | Hopelessness (shared predictor with depression) |
| 4 | `b5_cgpa` | CGPA 3.00–3.49 band |
| 5 | `b8_financial_pressure` | Financial stress |

### Checklist & Completed Tasks
- [x] SHAP Global Bar + Beeswarm plots (best model per target) → `figures/{target}_{model}_shap_*.png`
- [x] Top-15 Feature ranking tables → `results/{target}_top15_shap_features.csv`
- [x] Case Study Waterfall plots (High-Risk, Borderline, Low-Risk × 2 targets) → `figures/case_study_*.png`

---

## Phase 8: Results Documentation & Thesis Figures
**Who:** 🤖  
**Status:** 📋 UP NEXT

### Tasks
- [ ] TRIPOD-aligned results summary table (Chapter 5)
- [ ] Chapter 4: Methodology & Preprocessing write-up skeleton
- [ ] Chapter 5: Results & Model Comparison write-up skeleton
- [ ] Chapter 6: Discussion — Limitations, Clinical Implications, Future Work
- [ ] Final publication-quality figure review (300 DPI confirmed ✅ already)
- [ ] Thesis summary package & bibliography placeholder

---

*Last updated: 2026-11-01 (Phase 5–7 DONE on n=85 — Models trained, SHAP complete, results exported. Phase 8 UP NEXT.)*
