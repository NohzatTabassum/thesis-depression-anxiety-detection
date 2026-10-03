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
| [Phase 3](#phase-3-data-collection--google-form-deployment) | Data Collection (Google Form Deployment) | 👤 | 🟡 IN PROGRESS (Pilot n=67 Done) |
| [Phase 4](#phase-4-data-ingestion--eda) | Data Ingestion, Quality Audit & EDA | 🤖 | ✅ DONE |
| [Phase 5](#phase-5-preprocessing-pipeline) | Preprocessing Pipeline & Stratified Split | 🤖 | 📋 UP NEXT |
| [Phase 6](#phase-6-ml-modeling--cv) | ML Modeling & Cross-Validation | 🤖 | 📋 TODO |
| [Phase 7](#phase-7-shap-explainability--error-analysis) | SHAP Explainability & Error Analysis | 🤖 | 📋 TODO |
| [Phase 8](#phase-8-results-documentation--thesis-figures) | Results Documentation & Thesis Figures | 🤖 | 📋 TODO |

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
**Status:** 🟡 IN PROGRESS (Pilot n=67 Collected, Main survey active)

> **Live Survey Link:** [Google Form URL](https://docs.google.com/forms/d/e/1FAIpQLSe4NH1NZNCcIBUWQcyzowVXBe8gpynHXB833jLdZdFnl9-hgw/viewform)  
> **Edit/Responses URL:** [Edit Form URL](https://docs.google.com/forms/d/1wstOB3-JVECSQfNWOc3LlqUmE9EStvNeYrKnz_mebGs/edit)

### Checklist
- [x] Google Form তৈরি ও বাইলিঙ্গুয়াল স্কেল কনফিগার সম্পন্ন
- [x] Pilot study রেসপন্স গ্রহণ (n=67 responses collected)
- [x] Pilot feedback ও schema validation
- [x] CSV export → `data/raw/survey_responses.csv`
- [ ] Main data collection expansion (Target: n ≥ 150–250+ for thesis defense)

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
**Status:** 📋 UP NEXT

### Tasks
- [ ] Target variables: `dep_risk` (PHQ-9 ≥ 10), `anx_risk` (GAD-7 ≥ 10)
- [ ] Train/test stratified split (80/20) with zero data-leakage
- [ ] Feature transformations (One-hot encoding for categorical, Robust/Standard scaling for continuous)
- [ ] Outlier winsorization (5th–95th percentile)
- [ ] SMOTE balance on training set only
- [ ] 3 Ablation Configurations (Clinical only, + Social Support, + Job Behavioral)
- [ ] Pipeline verification & dry-run

---

## Phase 6: ML Modeling & Cross-Validation
**Who:** 🤖  
**Status:** 📋 TODO

### Tasks
- [ ] Baseline models: Logistic Regression, SVM, Random Forest, XGBoost
- [ ] Stratified 5-fold cross-validation
- [ ] Hyperparameter tuning via GridSearchCV
- [ ] Evaluation metrics: Macro-F1, Precision, Recall, Specificity, ROC-AUC with 95% CIs
- [ ] Model artifacts export (`models/`)

---

## Phase 7: SHAP Explainability & Error Analysis
**Who:** 🤖  
**Status:** 📋 TODO

### Tasks
- [ ] SHAP TreeExplainer & KernelExplainer initialization
- [ ] Global feature importance (summary bar + beeswarm plots)
- [ ] Localized case studies (Waterfall plots for high-risk, low-risk, borderline)
- [ ] False Negative analysis for clinical safety

---

## Phase 8: Results Documentation & Thesis Figures
**Who:** 🤖  
**Status:** 📋 TODO

### Tasks
- [ ] 300 DPI publication figures compilation
- [ ] TRIPOD-aligned results summary table
- [ ] Chapter 4 (Methodology & Preprocessing) & Chapter 5 (Results) documentation skeletons
- [ ] Final thesis summary package

---

*Last updated: 2026-10-03 (Post-Phase 4 Audit)*
