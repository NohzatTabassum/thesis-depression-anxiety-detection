"""
Evaluation module for Thesis Classification Models.
Computes clinically rigorous metrics, bootstrap 95% confidence intervals, and visualization plots.
"""
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
)

import config


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray
) -> Dict[str, float]:
    """
    Computes standard diagnostic evaluation metrics.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "sensitivity_recall": recall_score(y_true, y_pred, zero_division=0),
        "specificity": specificity,
        "precision_ppv": precision_score(y_true, y_pred, zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "f1_binary": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
        "pr_auc": average_precision_score(y_true, y_prob),
    }


def compute_bootstrap_ci(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bootstraps: int = config.N_BOOTSTRAP,
    alpha: float = 0.05,
    random_state: int = config.RANDOM_STATE
) -> Tuple[float, float]:
    """
    Calculates non-parametric 95% bootstrap confidence intervals for ROC-AUC.
    """
    rng = np.random.RandomState(random_state)
    bootstrapped_scores = []

    for _ in range(n_bootstraps):
        indices = rng.randint(0, len(y_true), len(y_true))
        if len(np.unique(y_true[indices])) < 2:
            continue
        score = roc_auc_score(y_true[indices], y_prob[indices])
        bootstrapped_scores.append(score)

    ci_lower = np.percentile(bootstrapped_scores, 100 * (alpha / 2))
    ci_upper = np.percentile(bootstrapped_scores, 100 * (1 - alpha / 2))
    return float(ci_lower), float(ci_upper)


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str,
    target_name: str = "Depression Risk",
    save_path: str = None
):
    """
    Plots styled confusion matrix with counts and percentages.
    """
    cm = confusion_matrix(y_true, y_pred)
    cm_perc = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    labels = [f"{v1}\n({v2:.1%})" for v1, v2 in zip(cm.flatten(), cm_perc.flatten())]
    labels = np.asarray(labels).reshape(2, 2)

    fig, ax = plt.subplots(figsize=(5, 4), dpi=300)
    sns.heatmap(
        cm,
        annot=labels,
        fmt="",
        cmap="Blues",
        cbar=False,
        xticklabels=["Low/No Risk", "High Risk"],
        yticklabels=["Low/No Risk", "High Risk"],
        ax=ax
    )
    ax.set_title(f"Confusion Matrix: {model_name} ({target_name})", fontsize=12, fontweight="bold")
    ax.set_xlabel("Predicted Label", fontsize=10)
    ax.set_ylabel("True Ground Truth", fontsize=10)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_roc_curves(
    results_dict: Dict[str, Tuple[np.ndarray, np.ndarray]],
    save_path: str = None
):
    """
    Plots multi-model ROC curves on a single high-resolution figure.
    results_dict format: {model_name: (y_true, y_prob)}
    """
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

    for model_name, (y_true, y_prob) in results_dict.items():
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob)
        ax.plot(fpr, tpr, lw=2, label=f"{model_name} (AUC = {auc:.3f})")

    ax.plot([0, 1], [0, 1], color="grey", linestyle="--", lw=1.5, label="Chance")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    ax.set_ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=11)
    ax.set_title("Receiver Operating Characteristic (ROC) Comparison", fontsize=13, fontweight="bold")
    ax.legend(loc="lower right", frameon=True)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
