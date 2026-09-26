"""
Configuration module for Thesis Research:
'AI-Assisted Early Risk Detection of Depression and Anxiety in University Students During Job Search'
"""
from pathlib import Path

# ==========================================
# 1. DIRECTORY PATHS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

MODELS_DIR = BASE_DIR / "models"
FIGURES_DIR = BASE_DIR / "figures"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SRC_DIR = BASE_DIR / "src"

# Default raw survey data filename
RAW_SURVEY_CSV = DATA_RAW_DIR / "survey_responses.csv"

# ==========================================
# 2. EXPERIMENT PARAMETERS & RANDOM STATE
# ==========================================
RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_FOLDS = 5
N_BOOTSTRAP = 1000

# ==========================================
# 3. CLINICAL CUTOFF THRESHOLDS
# ==========================================
# PHQ-9 (Patient Health Questionnaire-9)
# Score >= 10 indicates moderate-to-severe depression risk (Standard Clinical Cutoff)
PHQ9_CUTOFF = 10

# GAD-7 (Generalized Anxiety Disorder-7)
# Score >= 10 indicates moderate-to-severe anxiety risk (Standard Clinical Cutoff)
GAD7_CUTOFF = 10

# ==========================================
# 4. QUESTIONNAIRE ITEM IDENTIFIERS & DOMAINS
# ==========================================
# Section B: Demographics
DEMOGRAPHIC_COLS = [
    "gender",
    "age_group",
    "university_type",
    "academic_discipline",
    "cgpa_bracket",
    "graduation_timeline",
    "family_monthly_income",
    "financial_pressure",
]

# Section C: Job-Search Behavioral Signals (14 Items)
JOB_SEARCH_COLS = [
    "c1_search_duration_months",
    "c2_applications_per_week",
    "c3_weekly_hours_spent",
    "c4_late_night_search_freq",
    "c5_platform_count",
    "c6_rejection_count_est",
    "c7_ghosting_rate_perc",
    "c8_interview_invites_count",
    "c9_cv_customization_freq",
    "c10_peer_comparison_freq",
    "c11_family_expectation_pressure",
    "c12_unemployment_stigma_fear",
    "c13_future_career_hopelessness",
    "c14_daily_screen_time_hours",
]

# Section D: Multidimensional Scale of Perceived Social Support (MSPSS, 12 Items)
# Rated 1 (Very Strongly Disagree) to 7 (Very Strongly Agree)
MSPSS_ITEMS = [f"d{i}_mspss" for i in range(1, 13)]
MSPSS_SUBSCALE_SO = ["d1_mspss", "d2_mspss", "d5_mspss", "d10_mspss"]      # Significant Other
MSPSS_SUBSCALE_FAMILY = ["d3_mspss", "d4_mspss", "d8_mspss", "d11_mspss"]  # Family
MSPSS_SUBSCALE_FRIENDS = ["d6_mspss", "d7_mspss", "d9_mspss", "d12_mspss"] # Friends

# Section E: PHQ-9 (9 Items, Rated 0-3)
PHQ9_ITEMS = [f"e{i}_phq9" for i in range(1, 10)]

# Section F: GAD-7 (7 Items, Rated 0-3)
GAD7_ITEMS = [f"f{i}_gad7" for i in range(1, 8)]

# Attention check item
ATTENTION_CHECK_COL = "g1_attention_check"
ATTENTION_CHECK_EXPECTED = 4  # e.g., 'Please select "Somewhat Agree" (Option 4)'

# ==========================================
# 5. ABLATION STUDY FEATURE SET CONFIGURATIONS
# ==========================================
FEATURE_SETS = {
    # Set 1: Standard Demographics + Self-Report (MSPSS)
    "baseline_self_report": DEMOGRAPHIC_COLS + MSPSS_ITEMS,
    
    # Set 2: Demographics + Job-Search Behavioral Features
    "behavioral_only": DEMOGRAPHIC_COLS + JOB_SEARCH_COLS,
    
    # Set 3: Full Multi-Modal (Demographics + Behavioral + Social Support)
    "full_multimodal": DEMOGRAPHIC_COLS + JOB_SEARCH_COLS + MSPSS_ITEMS,
}
