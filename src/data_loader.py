"""
Data loading and quality control module for Thesis Survey Responses.
Handles ingestion, anonymization, attention-check filtering, and straight-lining removal.
"""
from typing import Optional, Tuple
import pandas as pd
import numpy as np
import logging

import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_raw_survey_data(csv_path: Optional[str] = None) -> pd.DataFrame:
    """
    Loads raw Google Forms CSV export.
    Removes identifying columns (Timestamp, Email, Student ID) if present.
    """
    path = csv_path if csv_path else config.RAW_SURVEY_CSV
    logger.info(f"Loading survey dataset from: {path}")
    
    df = pd.read_csv(path)
    logger.info(f"Raw dataset shape: {df.shape}")
    
    # Strip whitespace from column headers
    df.columns = [c.strip() for c in df.columns]
    
    # Anonymization: Drop sensitive PII columns if found
    pii_keywords = ["timestamp", "email", "e-mail", "student id", "name", "phone"]
    cols_to_drop = [c for c in df.columns if any(k in c.lower() for k in pii_keywords)]
    if cols_to_drop:
        logger.info(f"Dropping PII / administrative columns: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)
        
    return df


def filter_quality_responses(
    df: pd.DataFrame,
    attention_check_col: str = config.ATTENTION_CHECK_COL,
    expected_value: int = config.ATTENTION_CHECK_EXPECTED
) -> Tuple[pd.DataFrame, dict]:
    """
    Applies data quality and validity filters:
    1. Attention check filter
    2. Straight-lining detection across Likert scales (MSPSS, PHQ-9, GAD-7)
    3. Missing value filter (>20% missing values removed)
    """
    initial_count = len(df)
    audit_stats = {"initial_responses": initial_count}
    
    # 1. Attention Check
    if attention_check_col in df.columns:
        valid_attention = df[attention_check_col] == expected_value
        failed_attn = (~valid_attention).sum()
        df = df[valid_attention].drop(columns=[attention_check_col])
        audit_stats["failed_attention_check"] = int(failed_attn)
        logger.info(f"Removed {failed_attn} respondents failing the attention check.")
    else:
        audit_stats["failed_attention_check"] = 0
        logger.warning(f"Attention check column '{attention_check_col}' not found. Skipping filter.")
        
    # 2. Missing Value Threshold
    missing_ratio = df.isnull().mean(axis=1)
    high_missing = missing_ratio > 0.20
    df = df[~high_missing]
    audit_stats["dropped_high_missing"] = int(high_missing.sum())
    
    # 3. Straight-lining Check (Zero variance across all MSPSS items)
    mspss_present = [c for c in config.MSPSS_ITEMS if c in df.columns]
    if len(mspss_present) >= 6:
        mspss_std = df[mspss_present].std(axis=1)
        straight_liners = mspss_std == 0
        df = df[~straight_liners]
        audit_stats["dropped_straight_liners"] = int(straight_liners.sum())
        logger.info(f"Removed {straight_liners.sum()} straight-lining responses.")
    else:
        audit_stats["dropped_straight_liners"] = 0
        
    audit_stats["final_valid_responses"] = len(df)
    logger.info(f"Quality filtering complete. Retained {len(df)} of {initial_count} responses.")
    return df.reset_index(drop=True), audit_stats


def map_survey_columns(df: pd.DataFrame, mapping_dict: dict) -> pd.DataFrame:
    """
    Renames raw Google Forms header strings into standardized short identifiers.
    """
    renamed_df = df.rename(columns=mapping_dict)
    logger.info(f"Renamed {len(mapping_dict)} survey columns according to project schema.")
    return renamed_df
