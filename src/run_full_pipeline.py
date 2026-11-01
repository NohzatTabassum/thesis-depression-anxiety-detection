"""
Full Production Pipeline — Phase 5, 6 & 7
==========================================
Thesis: AI-Assisted Early Risk Detection of Depression & Anxiety
        in University Students During Job Search

Pipeline Steps:
  1. Load clean dataset (data/processed/clean_df.csv)
  2. Phase 5: Stratified train/test split + Preprocessing + SMOTE
  3. Phase 6: 5-Fold StratifiedKFold CV for all 5 models (dep_risk & anx_risk)
  4. Phase 6: Final fit + held-out test set evaluation + Bootstrap CI
  5. Phase 6: ROC Curve comparison + Confusion Matrices
  6. Phase 6: Results CSV export + Best model serialization
  7. Phase 7: SHAP Global Bar + Beeswarm plots (best model)
  8. Phase 7: SHAP Case Study Waterfall plots (3 cases)
  9. Phase 7: Top-15 Feature Importance table export
"""

import sys, os
sys.stdout.reconfigure(encoding='utf-8')

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import (
    f1_score, accuracy_score, balanced_accuracy_score,
    precision_score, recall_score, roc_auc_score, confusion_matrix,
    average_precision_score
)

# Project modules
import config
from src.preprocessing import compute_clinical_targets_and_scores, prepare_train_test_data
from src.models import get_models
from src.evaluate import (
    compute_classification_metrics, compute_bootstrap_ci,
    plot_confusion_matrix, plot_roc_curves
)
from src.shap_analysis import (
    compute_shap_explanations, generate_shap_summary_plots,
    generate_case_study_waterfall, get_top_features_table
)

# -- Paths
CLEAN_CSV   = "data/processed/clean_df.csv"
MODELS_DIR  = Path("models"); MODELS_DIR.mkdir(exist_ok=True)
FIGS_DIR    = Path("figures"); FIGS_DIR.mkdir(exist_ok=True)
RESULTS_DIR = Path("results"); RESULTS_DIR.mkdir(exist_ok=True)

# -- Load Data
print("=" * 65)
print("THESIS PIPELINE -- Full Run  (n=85 clean responses)")
print("=" * 65)

df = pd.read_csv(CLEAN_CSV)
print(f"\n[OK] Loaded clean dataset: {df.shape[0]} rows x {df.shape[1]} cols")

if "dep_risk" not in df.columns or "anx_risk" not in df.columns:
    df = compute_clinical_targets_and_scores(df)

dep_pos = int(df["dep_risk"].sum())
anx_pos = int(df["anx_risk"].sum())
print(f"   Depression Risk (dep_risk=1): {dep_pos}/{len(df)} = {dep_pos/len(df)*100:.1f}%")
print(f"   Anxiety Risk    (anx_risk=1): {anx_pos}/{len(df)} = {anx_pos/len(df)*100:.1f}%")

# -- Settings
TARGETS      = ["dep_risk", "anx_risk"]
FEATURE_SET  = "full_multimodal"
CV_FOLDS     = 5
RANDOM_STATE = config.RANDOM_STATE
all_results  = []

# -- PHASE 5 + 6 -- Per-Target Loop
for target in TARGETS:
    target_label = "Depression" if target == "dep_risk" else "Anxiety"
    print(f"\n{'='*65}")
    print(f"  TARGET: {target_label} Risk  [{target}]")
    print(f"{'='*65}")

    # Phase 5: Split + Preprocess + SMOTE
    X_train, X_test, y_train, y_test, preprocessor, feat_names = \
        prepare_train_test_data(df, FEATURE_SET, target_col=target, apply_smote=True)

    print(f"\n[Phase 5] Train set after SMOTE : {X_train.shape}")
    print(f"[Phase 5] Test  set (held-out)  : {X_test.shape}")

    models        = get_models(RANDOM_STATE)
    roc_data      = {}
    best_auc      = -1
    best_name     = ""
    best_model    = None
    best_shap_data = None

    # Phase 6: CV + Final Test Evaluation
    for model_name, clf in models.items():
        skf = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

        cv_res = cross_validate(
            clf, X_train, y_train,
            cv=skf,
            scoring=["f1_macro", "balanced_accuracy", "roc_auc"],
            return_train_score=False,
            n_jobs=-1
        )

        cv_f1     = cv_res["test_f1_macro"].mean()
        cv_auc    = cv_res["test_roc_auc"].mean()
        cv_f1_std = cv_res["test_f1_macro"].std()
        cv_auc_std= cv_res["test_roc_auc"].std()

        # Final fit on full training split
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]

        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        specificity  = tn / (tn + fp) if (tn + fp) > 0 else 0.0

        ci_lo, ci_hi = compute_bootstrap_ci(y_test, y_prob)

        test_metrics = {
            "target":                   target_label,
            "model":                    model_name,
            "cv_f1_macro_mean":         round(cv_f1, 4),
            "cv_f1_macro_std":          round(cv_f1_std, 4),
            "cv_auc_mean":              round(cv_auc, 4),
            "cv_auc_std":               round(cv_auc_std, 4),
            "test_accuracy":            round(accuracy_score(y_test, y_pred), 4),
            "test_balanced_acc":        round(balanced_accuracy_score(y_test, y_pred), 4),
            "test_f1_macro":            round(f1_score(y_test, y_pred, average="macro"), 4),
            "test_precision":           round(precision_score(y_test, y_pred, zero_division=0), 4),
            "test_recall_sensitivity":  round(recall_score(y_test, y_pred, zero_division=0), 4),
            "test_specificity":         round(specificity, 4),
            "test_roc_auc":             round(roc_auc_score(y_test, y_prob), 4),
            "test_pr_auc":              round(average_precision_score(y_test, y_prob), 4),
            "roc_auc_ci_lower":         round(ci_lo, 4),
            "roc_auc_ci_upper":         round(ci_hi, 4),
        }

        all_results.append(test_metrics)
        roc_data[model_name] = (y_test, y_prob)

        print(f"\n  [{model_name}]")
        print(f"    CV  F1-Macro : {cv_f1:.4f} +/- {cv_f1_std:.4f}")
        print(f"    CV  ROC-AUC  : {cv_auc:.4f} +/- {cv_auc_std:.4f}")
        print(f"    Test F1-Macro: {test_metrics['test_f1_macro']:.4f}")
        print(f"    Test ROC-AUC : {test_metrics['test_roc_auc']:.4f}  "
              f"95% CI [{ci_lo:.4f}, {ci_hi:.4f}]")
        print(f"    Sensitivity  : {test_metrics['test_recall_sensitivity']:.4f}  "
              f"Specificity: {test_metrics['test_specificity']:.4f}")

        # Confusion Matrix
        cm_path = FIGS_DIR / f"{target}_{model_name}_confusion_matrix.png"
        plot_confusion_matrix(y_test, y_pred, model_name, target_label, str(cm_path))

        if test_metrics["test_roc_auc"] > best_auc:
            best_auc        = test_metrics["test_roc_auc"]
            best_name       = model_name
            best_model      = clf
            best_shap_data  = (X_train, X_test, feat_names)

    # ROC Curve
    roc_path = FIGS_DIR / f"{target}_roc_curves.png"
    plot_roc_curves(roc_data, str(roc_path))
    print(f"\n  [OK] ROC Curve saved -> {roc_path}")

    # Save best model
    model_path = MODELS_DIR / f"best_{target}_{best_name}.pkl"
    joblib.dump(best_model, model_path)
    print(f"  [OK] Best model saved: {model_path}  (AUC={best_auc:.4f})")

    # -- Phase 7: SHAP Explainability
    print(f"\n[Phase 7] SHAP analysis -- Best model: {best_name}")
    X_tr_shap, X_te_shap, fnames = best_shap_data
    shap_prefix = f"{target}_{best_name}"

    try:
        shap_vals = compute_shap_explanations(best_model, X_tr_shap, X_te_shap, fnames)
        generate_shap_summary_plots(shap_vals, FIGS_DIR, prefix=shap_prefix)
        print(f"  [OK] SHAP Bar + Beeswarm saved -> figures/{shap_prefix}_shap_*.png")

        top_feat_df   = get_top_features_table(shap_vals, fnames, top_n=15)
        feat_csv_path = RESULTS_DIR / f"{target}_top15_shap_features.csv"
        top_feat_df.to_csv(feat_csv_path, index=False)
        print(f"  [OK] Top-15 Feature Table saved -> {feat_csv_path}")
        print(f"\n  Top-5 Features ({target_label}):")
        print(top_feat_df.head(5).to_string(index=False))

        # Waterfall case studies
        y_probs_all = best_model.predict_proba(X_te_shap)[:, 1]
        sorted_idx  = np.argsort(y_probs_all)
        cases = {
            "High_Risk":  sorted_idx[-1],
            "Low_Risk":   sorted_idx[0],
            "Borderline": sorted_idx[len(sorted_idx) // 2],
        }
        for case_name, idx in cases.items():
            generate_case_study_waterfall(shap_vals, int(idx), f"{target_label}_{case_name}", FIGS_DIR)
        print(f"  [OK] Waterfall case studies saved -> figures/case_study_*.png")

    except Exception as e:
        print(f"  [WARN] SHAP error: {e}")

# -- Save Master Results Table
results_df  = pd.DataFrame(all_results)
results_csv = RESULTS_DIR / "model_comparison_results.csv"
results_df.to_csv(results_csv, index=False)

print(f"\n{'='*65}")
print("  RESULTS SUMMARY TABLE")
print(f"{'='*65}")
cols_show = ["target", "model", "cv_auc_mean", "test_roc_auc",
             "roc_auc_ci_lower", "roc_auc_ci_upper",
             "test_f1_macro", "test_recall_sensitivity", "test_specificity"]
print(results_df[cols_show].to_string(index=False))

print(f"\n[OK] Full results saved -> {results_csv}")
print("\n*** PIPELINE COMPLETE -- All phases done! ***")
print(f"    Figures  -> figures/")
print(f"    Models   -> models/")
print(f"    Results  -> results/")
