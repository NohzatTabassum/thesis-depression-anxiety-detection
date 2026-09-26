# AI-Assisted Early Risk Detection of Depression and Anxiety in University Students During Job Search

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 📌 Project Overview
This repository contains the official implementation, survey instruments, and machine learning pipeline for the undergraduate/graduate thesis:

> **"Early Risk Detection of Depression and Anxiety in University Students During Job Search Using Social, Behavioural and Self-Report Signals"**

The job transition phase represents a high-vulnerability period for graduating university students. This research aims to develop an interpretable machine learning framework to identify early behavioral and psychosocial risk factors contributing to clinically significant depression and anxiety.

---

## 🎯 Key Research Objectives
1. **Instrument Development:** Design a multi-dimensional primary survey capturing demographics, job-search behavior, perceived social support ([MSPSS](https://doi.org/10.1207/s15327752jpa5201_2)), depression ([PHQ-9](https://doi.org/10.1046/j.1525-1497.2001.016009606.x)), and anxiety ([GAD-7](https://doi.org/10.1001/archinte.166.10.1092)).
2. **Predictive Modeling:** Train and benchmark supervised classification models (Random Forest, XGBoost, LightGBM, Logistic Regression, SVM) to predict binary risk classifications (`PHQ-9 ≥ 10`, `GAD-7 ≥ 10`).
3. **Model Explainability:** Utilize **SHAP (SHapley Additive exPlanations)** to uncover critical job-search behavioral indicators (e.g., ghosting frequency, rejection rate, late-night application behavior) contributing to psychological distress.

---

## 🔬 Study Instruments & Scales
| Dimension | Instrument | Target Metric / Cutoff |
| :--- | :--- | :--- |
| **Depression (Primary Target)** | PHQ-9 (9 items) | Moderate-to-severe risk (Score $\ge 10$) |
| **Anxiety (Secondary Target)** | GAD-7 (7 items) | Moderate-to-severe anxiety (Score $\ge 10$) |
| **Social Support** | MSPSS (12 items) | Family, Friends, Significant Other subscales |
| **Job-Search Behaviors** | Custom Scale (14 items) | Application intensity, rejection/ghosting frequency, search platform usage |
| **Demographics** | Section B (8 items) | CGPA, university type, graduation status, financial pressure |

---

## 📂 Repository Structure
```text
thesis-depression-anxiety-detection/
├── 00_Master_Thesis_Draft.docx          # Complete master thesis document draft
├── thesis_content.txt                   # Chapters 1-3 source text & literature review
├── methodology_diagram.png              # System methodology visual workflow
├── literature_review_table.png          # Synthesis table of past literature
├── data/                                # Dataset storage (raw and preprocessed)
│   ├── raw/                             # Raw survey exports (Google Forms)
│   └── processed/                       # Cleaned, encoded, feature-engineered datasets
├── src/                                 # Production Python pipeline scripts
│   ├── data_loader.py                   # Ingestion and schema validation
│   ├── preprocessing.py                 # Missing value handling, scaling, encoding
│   ├── models.py                        # Model architectures & training routines
│   ├── evaluate.py                      # Metrics (ROC-AUC, F1, PR-AUC) calculation
│   └── shap_analysis.py                 # Feature attribution and SHAP summary plots
├── notebooks/                           # Interactive Jupyter notebooks for EDA & analysis
│   ├── 01_eda.ipynb                     # Exploratory Data Analysis & statistical tests
│   └── 02_modeling_and_shap.ipynb       # Model benchmarks and explainability
├── models/                              # Serialized model checkpoints (.pkl / .joblib)
├── figures/                             # Exported publication-ready plots and charts
├── requirements.txt                     # Python dependencies
└── README.md                            # Project documentation
```

---

## ⚙️ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/NohzatTabassum/thesis-depression-anxiety-detection.git
cd thesis-depression-anxiety-detection
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🛡️ Ethical Statement
All survey instruments are administered following informed participant consent. Responses are fully anonymized, with no personally identifying information (PII) such as student IDs, phone numbers, or email addresses retained in the analytic dataset. Immediate crisis support helpline resources are integrated directly into the survey completion message.

---

## 👥 Author & Research Supervision
- **Researcher:** Tabassum ([NohzatTabassum](https://github.com/NohzatTabassum))
- **Affiliation:** Department of Software Engineering / Computer Science, Daffodil International University (DIU)
