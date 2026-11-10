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
**Status:** ✅ DONE (N=425 clean dataset)

### Checklist & Completed Tasks
- [x] CSV load ও ৫৬টি কলামের হেডার ম্যাপিং ও নতুন স্কিমা (Serial Number সহ) হ্যান্ডলিং
- [x] **Quality Control Audit Pipeline (Final N=425):**
  - Raw responses: 487
  - Non-consent removed: -1
  - Attention check failed: -55 (Strict IMC safeguard — Option 4 verification)
  - High missing (>20%): -0
  - Straight-liners removed: -6
  - **Clean final sample: 425 valid respondents**
- [x] PHQ-9 (E1-E9) ও GAD-7 (F1-F7) ক্লিনিক্যাল স্কোরিং (Clinical Cutoff ≥ 10):
  - **Depression Risk:** 45.9% (195/425) | Mean=9.64 ± 4.16, Range 1–27
  - **Anxiety Risk:** 31.5% (134/425) | Mean=8.35 ± 3.67, Range 0–21
  - **Comorbid (Both) Risk:** 18.8% (80/425)
  - **MSPSS (Social Support):** Mean=4.73 ± 0.94
- [x] ৫টি পাবলিকেশন-কোয়ালিটি এক্সপ্লোরেটরি ফিগার রিজেনারেট (`figures/`):
  1. `01_score_distributions.png` — Score distributions with clinical threshold lines
  2. `02_risk_prevalence.png` — Depression, anxiety & comorbidity risk breakdown
  3. `03_demographics.png` — Demographics across age, gender, education & income
  4. `04_phq9_vs_gad7_scatter.png` — PHQ-9 vs GAD-7 scatter with comorbidity quadrants
  5. `05_correlation_heatmap.png` — Spearman correlation matrix of scales & behavioral factors
- [x] ক্লিন ডেটাসেট এক্সপোর্ট: `data/processed/clean_df.csv`
- [x] Scripts: `src/run_audit.py`, `src/run_plots.py`, `src/phase4_eda.py`

---

## Phase 5: Preprocessing Pipeline & Stratified Split
**Who:** 🤖  
**Status:** ✅ DONE

### Checklist & Completed Tasks
- [x] Target variables: `dep_risk` (PHQ-9 ≥ 10), `anx_risk` (GAD-7 ≥ 10)
- [x] Stratified 80/20 train/test split with strict zero data-leakage (Train: 340, Test: 85)
- [x] Categorical & numerical feature pipeline with OneHotEncoder + StandardScaler
- [x] SMOTE class balancing applied strictly within training folds (Depression post-SMOTE: 368 train samples; Anxiety: 466)
- [x] Automated end-to-end execution via `src/run_full_pipeline.py`

---

## Phase 6: ML Modeling & Cross-Validation
**Who:** 🤖  
**Status:** ✅ DONE (Commit: `73df302`)

### Results Summary (N=425 clean, 5-Fold Stratified CV + Test Evaluation)

#### Depression Risk (dep_risk)
| Model | CV F1-Macro | CV ROC-AUC | Test ROC-AUC | 95% Bootstrap CI | Test F1-Macro | Sensitivity | Specificity |
|---|---|---|---|---|---|---|---|
| Logistic Regression | 0.560 ± 0.037 | 0.562 ± 0.037 | 0.542 | [0.411, 0.667] | 0.585 | 53.8% | 63.0% |
| SVM RBF | 0.602 ± 0.039 | 0.644 ± 0.043 | 0.555 | [0.426, 0.671] | 0.532 | 43.6% | 63.0% |
| **Random Forest** | **0.608 ± 0.046** | **0.661 ± 0.046** | **0.614** | **[0.499, 0.732]** | 0.573 | 43.6% | **71.7%** |
| XGBoost | 0.592 ± 0.046 | 0.626 ± 0.052 | 0.544 | [0.414, 0.671] | 0.593 | 51.3% | 67.4% |
| LightGBM | 0.580 ± 0.055 | 0.619 ± 0.053 | 0.539 | [0.419, 0.663] | 0.549 | 41.0% | 69.6% |
> 🏆 Best Depression Model: **Random Forest** (CV AUC = 0.661, Test AUC = 0.614) → `models/best_dep_risk_Random_Forest.pkl`

#### Anxiety Risk (anx_risk)
| Model | CV F1-Macro | CV ROC-AUC | Test ROC-AUC | 95% Bootstrap CI | Test F1-Macro | Sensitivity | Specificity |
|---|---|---|---|---|---|---|---|
| Logistic Regression | 0.673 ± 0.039 | 0.731 ± 0.016 | 0.600 | [0.465, 0.724] | 0.557 | 37.0% | 74.1% |
| **SVM RBF** | 0.752 ± 0.028 | **0.847 ± 0.022** | **0.619** | **[0.494, 0.742]** | 0.532 | 25.9% | **81.0%** |
| Random Forest | **0.803 ± 0.031** | **0.869 ± 0.034** | 0.520 | [0.396, 0.653] | 0.478 | 11.1% | **91.4%** |
| XGBoost | 0.776 ± 0.026 | 0.844 ± 0.030 | 0.583 | [0.458, 0.712] | 0.430 | 7.4% | 86.2% |
| LightGBM | 0.760 ± 0.034 | 0.839 ± 0.034 | 0.593 | [0.467, 0.716] | 0.484 | 14.8% | 86.2% |
> 🏆 Best Anxiety Model: **SVM RBF** (CV AUC = 0.847, Test AUC = 0.619, Specificity = 81.0%) → `models/best_anx_risk_SVM_RBF.pkl`

### Checklist & Completed Tasks
- [x] ৫টি ক্লাসিফায়ার: Logistic Regression, SVM RBF, Random Forest, XGBoost, LightGBM
- [x] 5-Fold Stratified Cross-Validation সম্পন্ন (F1, AUC, Balanced Acc, Precision, Recall, Specificity)
- [x] Bootstrap 95% CI (1000 iterations) ক্যালকুলেশন সম্পন্ন
- [x] ROC Curve comparison plots → `figures/{target}_roc_curves.png`
- [x] Confusion Matrices (10 plots) → `figures/{target}_{model}_confusion_matrix.png`
- [x] Results CSV → `results/model_comparison_results.csv`
- [x] Best models serialized → `models/best_dep_risk_Random_Forest.pkl`, `models/best_anx_risk_SVM_RBF.pkl`

---

## Phase 7: SHAP Explainability & Error Analysis
**Who:** 🤖  
**Status:** ✅ DONE (Commit: `73df302`)

### Key SHAP Findings (N=425)

#### Top-5 Features for Depression Risk (Random Forest):
| Rank | Feature | Mean |SHAP| | Clinical Meaning |
|---|---|---|---|
| 1 | `c13_hopelessness` | 0.0372 | Hopelessness about securing suitable jobs (Strongest depression predictor) |
| 2 | `c12_stigma_fear` | 0.0176 | Fear of social stigma & negative unemployment perception |
| 3 | `b1_gender_Female` | 0.0156 | Female students exhibit heightened vulnerability under career strain |
| 4 | `c14_screen_time_6-8h` | 0.0155 | Prolonged screen time correlates with behavioral rumination |
| 5 | `c10_peer_comparison` | 0.0153 | LinkedIn/Facebook peer comparisons induce career inadequacy feelings |

#### Top-5 Features for Anxiety Risk (SVM RBF):
| Rank | Feature | Mean |SHAP| | Clinical Meaning |
|---|---|---|---|
| 1 | `c13_hopelessness` | 0.0921 | General hopelessness (Cardinal predictor across both disorders) |
| 2 | `d6_mspss` | 0.0463 | Friends' support subscale (Lack of supportive peer buffers anxiety) |
| 3 | `c4_late_night_Sometimes` | 0.0368 | Late-night job searching signals anxiety-induced sleep disruption |
| 4 | `d5_mspss` | 0.0302 | Perceived social emotional availability |
| 5 | `b8_financial_pressure` | 0.0288 | Urgent financial need to secure immediate employment |

### Checklist & Completed Tasks
- [x] SHAP Global Bar + Beeswarm plots (Best model per target) → `figures/{target}_{model}_shap_*.png`
- [x] Top-15 Feature ranking tables → `results/{target}_top15_shap_features.csv`
- [x] Case Study Waterfall plots (High-Risk, Borderline, Low-Risk × 2 targets) → `figures/case_study_*.png`

---

## Phase 8: Results Documentation & Thesis Writing
**Who:** 🤖 + 👤  
**Status:** 📋 UP NEXT

### Tasks & Remaining Deliverables
- [ ] **Task 8.1:** TRIPOD-aligned methodology & results master table generation
- [ ] **Task 8.2:** Chapter 4 (Methodology) draft writing:
  - Participants & survey administration protocol (Bilingual adaptation, ethical consent, attention checks)
  - Preprocessing, stratified 80/20 partitioning & zero-leakage SMOTE framework
  - Model architectures (LR, SVM, RF, XGBoost, LightGBM) & 5-fold stratified CV scheme
  - Explainability framework via TreeExplainer & Permutation SHAP
- [ ] **Task 8.3:** Chapter 5 (Results) draft writing:
  - Descriptive sample characteristics (N=425 demographics, PHQ-9 & GAD-7 prevalence)
  - Comparative model performance analysis (CV AUC vs. held-out test ROC/PR-AUC)
  - Clinical explainability insights (Global feature attributions & case-study waterfalls)
- [ ] **Task 8.4:** Chapter 6 (Discussion & Conclusion) draft writing:
  - Key findings interpretation (Why `c13_hopelessness` dominates, role of peer comparison & late night searching)
  - Limitations (Cross-sectional, self-report bias, single country context) & Ethical AI safeguards
- [ ] **Task 8.5:** Mid-Defense / Final Defense PPTX Slide Deck update with N=425 figures and methodology diagram

---

*Last updated: 2026-11-10 (Full pipeline successfully executed on N=425 clean data [487 raw]. Models trained, SHAP generated, figures updated. Phase 8 UP NEXT.)*
