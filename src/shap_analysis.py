"""
Explainable AI (XAI) module using SHAP (SHapley Additive exPlanations).
Generates global feature attributions, beeswarm distributions, and case-study waterfalls.
"""
from typing import List, Optional
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap

import config


def compute_shap_explanations(
    model,
    X_train: np.ndarray,
    X_test: np.ndarray,
    feature_names: List[str]
) -> shap.Explanation:
    """
    Initializes SHAP TreeExplainer or standard Explainer and computes SHAP values.
    """
    try:
        # Preferred explainer for Tree-based models (XGBoost, LightGBM, RF)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X_test)
    except Exception:
        # Fallback for linear / kernel models
        explainer = shap.Explainer(model.predict_proba, X_train)
        shap_values = explainer(X_test)

    # If binary classification returns 3D shape (samples, features, 2), extract positive class (class 1)
    if len(shap_values.shape) == 3:
        shap_values = shap_values[:, :, 1]

    shap_values.feature_names = feature_names
    return shap_values


def generate_shap_summary_plots(
    shap_values: shap.Explanation,
    output_dir: Optional[Path] = None,
    prefix: str = "best_model"
):
    """
    Saves SHAP Global Summary Bar Plot and Beeswarm Distribution Plot.
    """
    save_dir = output_dir if output_dir else config.FIGURES_DIR
    save_dir.mkdir(parents=True, exist_ok=True)

    # 1. Bar Plot (Mean |SHAP value|)
    plt.figure(figsize=(9, 6), dpi=300)
    shap.plots.bar(shap_values, max_display=15, show=False)
    plt.title(f"Global Feature Importance Ranking ({prefix})", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / f"{prefix}_shap_bar_summary.png", dpi=300, bbox_inches="tight")
    plt.close()

    # 2. Beeswarm Plot (Feature impact and directionality)
    plt.figure(figsize=(10, 7), dpi=300)
    shap.plots.beeswarm(shap_values, max_display=15, show=False)
    plt.title(f"SHAP Summary Beeswarm Plot ({prefix})", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / f"{prefix}_shap_beeswarm.png", dpi=300, bbox_inches="tight")
    plt.close()


def generate_case_study_waterfall(
    shap_values: shap.Explanation,
    sample_index: int,
    case_label: str,
    output_dir: Optional[Path] = None
):
    """
    Generates a localized waterfall plot for a specific participant case study.
    """
    save_dir = output_dir if output_dir else config.FIGURES_DIR
    save_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(9, 6), dpi=300)
    shap.plots.waterfall(shap_values[sample_index], max_display=10, show=False)
    plt.title(f"SHAP Case Study: {case_label}", fontsize=12, fontweight="bold")
    plt.tight_layout()
    plt.savefig(save_dir / f"case_study_{case_label.lower().replace(' ', '_')}.png", dpi=300, bbox_inches="tight")
    plt.close()


def get_top_features_table(
    shap_values: shap.Explanation,
    feature_names: List[str],
    top_n: int = 15
) -> pd.DataFrame:
    """
    Returns a pandas DataFrame of top N features ranked by mean absolute SHAP value.
    """
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    ranking_df = pd.DataFrame({
        "Feature": feature_names,
        "Mean_Absolute_SHAP": mean_abs_shap
    }).sort_values(by="Mean_Absolute_SHAP", ascending=False).reset_index(drop=True)
    
    return ranking_df.head(top_n)
