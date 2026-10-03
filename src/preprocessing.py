"""
Preprocessing pipeline for Thesis Survey Data.
Adheres strictly to clinical ML standards:
- Stratified train-test split BEFORE transformation (zero data leakage)
- Feature scaling & one-hot encoding
- SMOTE oversampling applied ONLY to the training set
"""
from typing import Tuple, List, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

import config


def compute_clinical_targets_and_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes instrument aggregate scores and clinical risk binary targets.
    - PHQ-9: Sum of 9 items (0-27). Risk >= 10.
    - GAD-7: Sum of 7 items (0-21). Risk >= 10.
    - MSPSS: Subscale means (Family, Friends, Significant Other, Total).
    """
    df = df.copy()

    # 1. PHQ-9 Depression Score
    phq_present = [c for c in config.PHQ9_ITEMS if c in df.columns]
    if len(phq_present) == 9:
        df["phq9_total"] = df[phq_present].sum(axis=1)
        df["dep_risk"] = (df["phq9_total"] >= config.PHQ9_CUTOFF).astype(int)
    else:
        raise ValueError(f"Expected 9 PHQ-9 items, found: {phq_present}")

    # 2. GAD-7 Anxiety Score
    gad_present = [c for c in config.GAD7_ITEMS if c in df.columns]
    if len(gad_present) == 7:
        df["gad7_total"] = df[gad_present].sum(axis=1)
        df["anx_risk"] = (df["gad7_total"] >= config.GAD7_CUTOFF).astype(int)
    else:
        raise ValueError(f"Expected 7 GAD-7 items, found: {gad_present}")

    # 3. MSPSS Social Support Subscales
    if all(c in df.columns for c in config.MSPSS_ITEMS):
        df["mspss_significant_other"] = df[config.MSPSS_SUBSCALE_SO].mean(axis=1)
        df["mspss_family"] = df[config.MSPSS_SUBSCALE_FAMILY].mean(axis=1)
        df["mspss_friends"] = df[config.MSPSS_SUBSCALE_FRIENDS].mean(axis=1)
        df["mspss_total"] = df[config.MSPSS_ITEMS].mean(axis=1)

    return df


def build_preprocessor(
    numerical_cols: List[str],
    categorical_cols: List[str]
) -> ColumnTransformer:
    """
    Creates a scikit-learn ColumnTransformer pipeline for continuous and categorical features.
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_cols),
            ("cat", cat_pipeline, categorical_cols),
        ],
        remainder="drop"
    )
    return preprocessor


def prepare_train_test_data(
    df: pd.DataFrame,
    feature_set_name: str = "full_multimodal",
    target_col: str = "dep_risk",
    apply_smote: bool = True,
    test_size: float = config.TEST_SIZE,
    random_state: int = config.RANDOM_STATE
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, ColumnTransformer, List[str]]:
    """
    Splits data into train and test sets, fits preprocessing pipeline on train set only,
    and optionally applies SMOTE oversampling to the training set.
    """
    feature_cols = config.FEATURE_SETS[feature_set_name]
    
    # Auto-detect numerical vs categorical columns based on dataframe types
    categorical_cols = []
    numerical_cols = []
    for c in feature_cols:
        if pd.api.types.is_numeric_dtype(df[c]):
            # Optional: Some numeric columns with few unique values could be categorical, 
            # but for now we trust the dtype. 
            numerical_cols.append(c)
        else:
            categorical_cols.append(c)

    X = df[feature_cols]
    y = df[target_col].values

    # Step 1: Stratified train/test split BEFORE any scaling/transformations
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )

    # Step 2: Fit preprocessor on X_train ONLY, then transform both
    preprocessor = build_preprocessor(numerical_cols, categorical_cols)
    X_train_proc = preprocessor.fit_transform(X_train_raw)
    X_test_proc = preprocessor.transform(X_test_raw)

    # Extract transformed feature names
    cat_encoder = preprocessor.named_transformers_["cat"].named_steps["encoder"]
    encoded_cat_names = cat_encoder.get_feature_names_out(categorical_cols).tolist()
    all_feature_names = numerical_cols + encoded_cat_names

    # Step 3: Apply SMOTE on training set only (if requested and imbalanced)
    if apply_smote:
        smote = SMOTE(random_state=random_state)
        X_train_proc, y_train = smote.fit_resample(X_train_proc, y_train)

    return X_train_proc, X_test_proc, y_train, y_test, preprocessor, all_feature_names
