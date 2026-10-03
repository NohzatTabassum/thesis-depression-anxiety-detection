import sys, os
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

import config
from src.preprocessing import compute_clinical_targets_and_scores, prepare_train_test_data
from src.models import get_models
from src.evaluate import compute_classification_metrics
from src.shap_analysis import compute_shap_explanations, generate_shap_summary_plots

def main():
    print("=========================================================")
    print("   PHASE 5 & 6: PIPELINE DRY-RUN / SANITY CHECK (n=45)   ")
    print("=========================================================")
    
    # 1. Load data
    clean_csv = "data/processed/clean_df.csv"
    if not os.path.exists(clean_csv):
        print(f"Error: {clean_csv} not found.")
        return
        
    df = pd.read_csv(clean_csv)
    print(f"Loaded {len(df)} samples.")
    
    # 2. Compute targets
    df = compute_clinical_targets_and_scores(df)
    
    # 3. Test on Depression Risk (dep_risk)
    target = "dep_risk"
    print(f"\n[Testing Target: {target}]")
    print(f"Class distribution: 0={sum(df[target]==0)}, 1={sum(df[target]==1)}")
    
    # 4. Preprocessing & SMOTE
    print("\nRunning Preprocessing Pipeline (Split, Scale, Encode, SMOTE)...")
    try:
        X_train, X_test, y_train, y_test, preprocessor, feature_names = prepare_train_test_data(
            df, 
            feature_set_name="full_multimodal",
            target_col=target,
            apply_smote=True
        )
        print(f"-> Train shape: {X_train.shape} (SMOTE balanced)")
        print(f"-> Test shape: {X_test.shape}")
        print(f"-> Test set target counts: {np.bincount(y_test) if len(y_test)>0 else 'Empty'}")
    except Exception as e:
        print(f"ERROR in Preprocessing: {e}")
        return

    # If test set is pure due to small n, roc_auc will fail. Handle it gracefully.
    if len(np.unique(y_test)) < 2:
        print("\n[WARNING] Test set has only one class due to tiny sample size (n=45).")
        print("This is normal for a small split. The pipeline will still run to check for code bugs.")
    
    # 5. Train all models
    models = get_models()
    best_model_name = "Random_Forest"
    best_model = None
    
    print("\nTraining Baseline Models...")
    for name, model in models.items():
        print(f" - {name:<20}", end="")
        try:
            model.fit(X_train, y_train)
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)[:, 1]
            else:
                y_prob = model.predict(X_test)
            y_pred = model.predict(X_test)
            
            # Evaluate (wrapped in try-except for AUC error on uniform test set)
            try:
                metrics = compute_classification_metrics(y_test, y_pred, y_prob)
                print(f"| Acc: {metrics['accuracy']:.2f}, F1: {metrics['f1_macro']:.2f}, AUC: {metrics['roc_auc']:.2f}")
            except ValueError:
                print(f"| Acc: {np.mean(y_pred==y_test):.2f} (AUC skipped due to 1-class test set)")
                
            if name == best_model_name:
                best_model = model
        except Exception as e:
            print(f"| ERROR: {e}")

    # 6. SHAP Explainer Sanity Check
    if best_model is not None:
        print(f"\nRunning SHAP Explainer Sanity Check on {best_model_name}...")
        try:
            shap_vals = compute_shap_explanations(best_model, X_train, X_test, feature_names)
            generate_shap_summary_plots(shap_vals, prefix=f"sanity_{target}_{best_model_name}")
            print("-> SHAP plots successfully generated in 'figures/' folder.")
        except Exception as e:
            print(f"-> ERROR in SHAP generation: {e}")

    print("\n=========================================================")
    print("   SANITY CHECK COMPLETED: No blocking pipeline errors!  ")
    print("=========================================================")

if __name__ == "__main__":
    main()
