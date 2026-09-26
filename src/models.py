"""
Machine Learning Model Architectures and Training Routines.
Defines baseline classifiers, hyperparameter grids, and stratified cross-validation routines.
"""
from typing import Dict, Any
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

import config


def get_models(random_state: int = config.RANDOM_STATE) -> Dict[str, Any]:
    """
    Returns the standard suite of supervised classifiers for benchmark comparison.
    """
    return {
        "Logistic_Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=random_state
        ),
        "SVM_RBF": SVC(
            kernel="rbf",
            probability=True,
            class_weight="balanced",
            random_state=random_state
        ),
        "Random_Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=6,
            class_weight="balanced",
            random_state=random_state
        ),
        "XGBoost": XGBClassifier(
            n_estimators=150,
            max_depth=4,
            learning_rate=0.05,
            eval_metric="logloss",
            random_state=random_state
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=150,
            max_depth=4,
            learning_rate=0.05,
            random_state=random_state,
            verbose=-1
        )
    }


def get_hyperparameter_grids() -> Dict[str, Dict[str, list]]:
    """
    Returns search spaces for model hyperparameter optimization.
    """
    return {
        "Logistic_Regression": {
            "C": [0.01, 0.1, 1.0, 10.0],
            "penalty": ["l2"],
            "solver": ["lbfgs", "liblinear"]
        },
        "SVM_RBF": {
            "C": [0.1, 1.0, 5.0, 10.0],
            "gamma": ["scale", "auto", 0.01, 0.1]
        },
        "Random_Forest": {
            "n_estimators": [100, 200, 300],
            "max_depth": [4, 6, 8, None],
            "min_samples_split": [2, 5, 10]
        },
        "XGBoost": {
            "n_estimators": [100, 200],
            "max_depth": [3, 4, 6],
            "learning_rate": [0.01, 0.05, 0.1],
            "subsample": [0.8, 1.0]
        },
        "LightGBM": {
            "n_estimators": [100, 200],
            "max_depth": [3, 5, -1],
            "learning_rate": [0.01, 0.05, 0.1],
            "num_leaves": [15, 31]
        }
    }
