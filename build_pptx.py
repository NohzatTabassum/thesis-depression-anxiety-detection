"""
Simple Mid-Defense PPTX builder.
Strategy: Load template as-is, add plain textboxes on top of each slide.
Do NOT touch existing shapes. Just add new textboxes with content.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

TEMPLATE = 'Slide Template (PPTX) fo Mid_Defense.pptx'
OUTPUT   = 'Mid_Defense_FINAL.pptx'

WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
YELLOW = RGBColor(0xFF, 0xD7, 0x00)
CYAN   = RGBColor(0x00, 0xD4, 0xFF)
BLACK  = RGBColor(0x00, 0x00, 0x00)

prs = Presentation(TEMPLATE)
slides = list(prs.slides)

# ------------------------------------------------------------------
# Helper: add a multiline textbox
# ------------------------------------------------------------------
def tb(slide, left, top, w, h, lines, sizes=None, bolds=None,
        colors=None, aligns=None):
    """
    lines  : list of str  (each str = one paragraph)
    sizes  : list of int  (font size per line; default 14)
    bolds  : list of bool (default False)
    colors : list of RGBColor (default WHITE)
    aligns : list of PP_ALIGN (default LEFT)
    """
    box = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True

    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size  = Pt((sizes  or [])[i] if sizes  and i < len(sizes)  else 14)
        run.font.bold  = (bolds  or [])[i]     if bolds  and i < len(bolds)  else False
        run.font.color.rgb = (colors or [])[i] if colors and i < len(colors) else WHITE
        if aligns and i < len(aligns) and aligns[i]:
            p.alignment = aligns[i]


# ==================================================================
# SLIDE 1 — Title
# ==================================================================
s = slides[0]
tb(s, 0.5, 1.3, 12.2, 1.8,
   ["AI-Assisted Early Risk Detection of Depression and Anxiety",
    "in University Students During Job Search",
    "Using Social, Behavioral, and Self-Report Signals"],
   sizes=[24, 22, 18],
   bolds=[True, True, False],
   colors=[YELLOW, WHITE, CYAN],
   aligns=[PP_ALIGN.CENTER]*3)

tb(s, 0.5, 3.4, 12.0, 2.2,
   ["Presented By:",
    "[Your Full Name]  |  ID: [Student ID]",
    "",
    "Supervisor:",
    "[Supervisor Name]",
    "[Title], Department of Software Engineering",
    "Daffodil International University"],
   sizes=[13, 15, 8, 13, 15, 13, 13],
   bolds=[True, True, False, True, True, False, False],
   colors=[YELLOW, WHITE, WHITE, YELLOW, WHITE, WHITE, CYAN],
   aligns=[PP_ALIGN.CENTER]*7)


# ==================================================================
# SLIDE 2 — Outlines
# ==================================================================
s = slides[1]
tb(s, 0.5, 1.3, 12.0, 5.5,
   ["01  |  Problem Statement",
    "02  |  Research Gap",
    "03  |  Objectives",
    "04  |  Research Questions & Scope",
    "05  |  Literature Review",
    "06  |  Methodology",
    "07  |  Feature Space & Instruments",
    "08  |  Evaluation & Explainability (SHAP)",
    "09  |  My Contributions",
    "10  |  References"],
   sizes=[16]*10,
   bolds=[False]*10,
   colors=[WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE])


# ==================================================================
# SLIDE 3 — Problem Statement
# ==================================================================
s = slides[2]
tb(s, 0.4, 1.3, 12.2, 5.8,
   ["1. Students face severe psychological strain during the school-to-work transition.",
    "   Labour market uncertainty creates distress comparable to actual unemployment.",
    "",
    "2. Standard screening tools (PHQ-9, GAD-7) are used in isolation.",
    "   They ignore behavioral and social signals — missing many at-risk students.",
    "",
    "3. Most AI/ML models use single-modality data (e.g., social media only).",
    "   They are opaque, lack explainability, and are not reproducible.",
    "",
    "4. Severe class imbalance in existing datasets.",
    "   High-risk minority groups are systematically under-detected."],
   sizes=[14, 13, 6, 14, 13, 6, 14, 13, 6, 14, 13],
   bolds=[True, False, False, True, False, False, True, False, False, True, False],
   colors=[YELLOW, WHITE, WHITE, YELLOW, WHITE, WHITE, YELLOW, WHITE, WHITE, YELLOW, WHITE])


# ==================================================================
# SLIDE 4 — Objectives  (template slide index 3)
# ==================================================================
s = slides[3]
tb(s, 0.4, 1.3, 12.2, 5.5,
   ["O1.  Construct an integrated feature space combining PHQ-9, GAD-7, MSPSS",
    "       with quantified job-search behavioral indicators.",
    "",
    "O2.  Develop and compare supervised ML baselines (LR, SVM, RF, XGBoost)",
    "       for joint depression-anxiety risk classification.",
    "",
    "O3.  Apply SHAP to generate interpretable feature-level explanations",
    "       for non-clinical decision support.",
    "",
    "O4.  Operationalize behavioral variables (search intensity, planfulness,",
    "       rejection load) with consistent measurement definitions.",
    "",
    "O5.  Implement a TRIPOD-aligned evaluation workflow using stratified CV",
    "       and macro-F1 with class-imbalance-aware analysis."],
   sizes=[14, 13, 6, 14, 13, 6, 14, 13, 6, 14, 13, 6, 14, 13],
   bolds=[True]*14,
   colors=([CYAN, WHITE, WHITE] * 5)[:14])


# ==================================================================
# SLIDE 5 — Research Gap  (template slide index 4)
# ==================================================================
s = slides[4]
tb(s, 0.4, 1.3, 12.2, 5.6,
   ["Gap 1:  Models rely on single-modality data — social media OR clinical records. Not fused.",
    "Gap 2:  Perceived social support (MSPSS) is omitted from most computational models.",
    "Gap 3:  No joint depression-anxiety pipeline for student job-search context exists.",
    "Gap 4:  Deep learning models are opaque — no SHAP or interpretability for practitioners.",
    "Gap 5:  Behavioral signals (search intensity, planfulness) are inconsistently defined.",
    "Gap 6:  TRIPOD & PROBAST violations are widespread — reproducibility is lacking.",
    "Gap 7:  Class imbalance causes high-risk minority groups to be under-detected."],
   sizes=[14, 14, 14, 14, 14, 14, 14],
   bolds=[False]*7,
   colors=[WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE])


# ==================================================================
# SLIDE 5b — Research Questions & Scope  (add new slide after index 4)
# ==================================================================
# Use blank layout (index 6 in slide_layouts)
blank_layout = prs.slide_layouts[6]
rq_slide = prs.slides.add_slide(blank_layout)

tb(rq_slide, 0.4, 0.2, 12.0, 0.7,
   ["Research Questions & Scope"],
   sizes=[28], bolds=[True], colors=[YELLOW])

tb(rq_slide, 0.4, 1.1, 12.2, 3.8,
   ["RQ1:  Does multi-source integration improve joint depression-anxiety classification",
    "       vs. single-source baselines?",
    "RQ2:  Which features are most predictive according to SHAP analysis?",
    "RQ3:  How do 4 ML baselines compare on macro-F1 under stratified evaluation?",
    "RQ4:  How does consistent behavioral operationalization affect model stability?",
    "RQ5:  To what extent does TRIPOD-aligned reporting improve reproducibility?"],
   sizes=[14, 13, 14, 14, 14, 14],
   bolds=[True, False, True, True, True, True],
   colors=[CYAN, WHITE, CYAN, CYAN, CYAN, CYAN])

tb(rq_slide, 0.4, 5.1, 5.8, 2.0,
   ["IN SCOPE",
    "- Final-year undergrads / recent graduates",
    "- PHQ-9, GAD-7, MSPSS instruments",
    "- 4 ML baselines + SHAP + TRIPOD"],
   sizes=[15, 13, 13, 13],
   bolds=[True, False, False, False],
   colors=[YELLOW, WHITE, WHITE, WHITE])

tb(rq_slide, 6.8, 5.1, 6.0, 2.0,
   ["OUT OF SCOPE",
    "- Clinical diagnosis or therapy",
    "- Neuroimaging / physiological sensors",
    "- Causal inference claims"],
   sizes=[15, 13, 13, 13],
   bolds=[True, False, False, False],
   colors=[YELLOW, WHITE, WHITE, WHITE])


# ==================================================================
# SLIDE 6 — Literature Review  (template slide index 5)
# ==================================================================
s = slides[5]
tb(s, 0.4, 1.2, 12.2, 5.8,
   ["Topic                       Key Finding                                      Research Gap",
    "─────────────────────────────────────────────────────────────────────────────────────────",
    "PHQ-9 / GAD-7               88% sensitivity at cutoff >= 10                  Used in isolation only",
    "Job Insecurity & MH         29% elevated depression risk (meta-analysis)     Ignored in ML models",
    "Search Intensity            rc = -0.11 with mental well-being                No behavioral ML feature",
    "Social Support (MSPSS)      Inverse correlation with distress                Omitted from pipelines",
    "ML for Depression           SVM/RF/BERT; AUC up to 0.89                     Opaque, non-reproducible",
    "SHAP Explainability         Improves trust and decision support              Rarely applied in student MH",
    "TRIPOD / PROBAST            Guidelines for prediction model reporting        Widely violated in AI-MH"],
   sizes=[12, 10, 12, 12, 12, 12, 12, 12, 12],
   bolds=[True, False, False, False, False, False, False, False, False],
   colors=[YELLOW] + [WHITE]*8)


# ==================================================================
# SLIDE 7 — Methodology  (template slide index 6)
# ==================================================================
s = slides[6]
tb(s, 0.4, 1.1, 12.2, 5.9,
   ["Phase 1 — Data Collection",
    "  • Survey via secure web platform (informed consent + anonymization)",
    "  • Instruments: PHQ-9, GAD-7, MSPSS + behavioral + demographics",
    "",
    "Phase 2 — Preprocessing",
    "  • Median imputation | Z-score standardization | One-hot encoding",
    "  • Winsorize outliers (5th–95th %ile) | SMOTE / cost-sensitive weights",
    "",
    "Phase 3 — Modeling",
    "  • Baselines: Logistic Regression, SVM, Random Forest, XGBoost",
    "  • Joint multi-label target: [dep_risk, anx_risk]",
    "  • Stratified k-fold CV + grid search hyperparameter tuning",
    "",
    "Phase 4 — Explainability & Evaluation",
    "  • SHAP (global + local) | Confusion matrix | FN analysis",
    "  • Metrics: Macro-F1, Precision, Recall, ROC-AUC with 95% CI"],
   sizes=[15, 13, 13, 6, 15, 13, 13, 6, 15, 13, 13, 13, 6, 15, 13, 13],
   bolds=[True,False,False,False,True,False,False,False,True,False,False,False,False,True,False,False],
   colors=([CYAN,WHITE,WHITE,WHITE]*4)[:16])


# ==================================================================
# SLIDE 7b — Feature Space  (new blank slide)
# ==================================================================
feat_slide = prs.slides.add_slide(blank_layout)

tb(feat_slide, 0.4, 0.2, 12.0, 0.7,
   ["Feature Space & Measurement Instruments"],
   sizes=[26], bolds=[True], colors=[YELLOW])

tb(feat_slide, 0.4, 1.1, 3.8, 5.8,
   ["SELF-REPORT (Psychometric)",
    "",
    "PHQ-9",
    "  9 items, score 0-27",
    "  dep_risk if score >= 10",
    "",
    "GAD-7",
    "  7 items, score 0-21",
    "  anx_risk if score >= 10",
    "",
    "Individual Likert items",
    "  used as ordinal features"],
   sizes=[14,6,14,12,12,6,14,12,12,6,14,12],
   bolds=[True]+[False]*11,
   colors=[YELLOW]+[WHITE]*11)

tb(feat_slide, 4.5, 1.1, 3.8, 5.8,
   ["SOCIAL SUPPORT (MSPSS)",
    "",
    "12-item scale, 3 subscales:",
    "",
    "  Family subscale",
    "  Friends subscale",
    "  Significant Other subscale",
    "",
    "Items: 1-7 Likert scale",
    "Subscale totals as",
    "  continuous predictors"],
   sizes=[14,6,13,6,13,13,13,6,13,13,13],
   bolds=[True]+[False]*10,
   colors=[CYAN]+[WHITE]*10)

tb(feat_slide, 8.6, 1.1, 4.5, 5.8,
   ["BEHAVIORAL (Job-Search)",
    "",
    "Search Intensity",
    "  applications per week",
    "",
    "Search Planfulness",
    "  Focused vs. Haphazard",
    "",
    "Rejection Load",
    "  total negative responses",
    "",
    "Demographics",
    "  age, gender, degree type"],
   sizes=[14,6,14,12,6,14,12,6,14,12,6,14,12],
   bolds=[True]+[False]*12,
   colors=[CYAN]+[WHITE]*12)


# ==================================================================
# SLIDE 7c — Evaluation & SHAP  (new blank slide)
# ==================================================================
eval_slide = prs.slides.add_slide(blank_layout)

tb(eval_slide, 0.4, 0.2, 12.0, 0.7,
   ["Evaluation Protocol & SHAP Explainability"],
   sizes=[24], bolds=[True], colors=[YELLOW])

tb(eval_slide, 0.4, 1.1, 6.0, 3.0,
   ["Evaluation Metrics",
    "",
    "  Primary:   Macro-F1 (imbalance-aware)",
    "  Secondary: Precision, Recall, Specificity",
    "  Also:      ROC-AUC with 95% CI",
    "             Confusion matrix per model"],
   sizes=[15,6,13,13,13,13],
   bolds=[True]+[False]*5,
   colors=[CYAN]+[WHITE]*5)

tb(eval_slide, 6.6, 1.1, 6.5, 3.0,
   ["Validation Strategy",
    "",
    "  Stratified k-fold cross-validation",
    "  Separate held-out test set (stratified)",
    "  Train/test split BEFORE scaling/imputation",
    "  Ablation: single-source vs. multi-source"],
   sizes=[15,6,13,13,13,13],
   bolds=[True]+[False]*5,
   colors=[CYAN]+[WHITE]*5)

tb(eval_slide, 0.4, 4.3, 12.2, 3.1,
   ["SHAP Explainability Plan",
    "",
    "  Global SHAP:  Bar/beeswarm plots — which features drive risk across all students",
    "  Local SHAP:   Per-student waterfall — why THIS student was flagged as high-risk",
    "  FN Analysis:  Feature distributions of missed high-risk students (False Negatives)",
    "                Identifies systematic signal deficiencies for next model iteration"],
   sizes=[15,6,13,13,13,13],
   bolds=[True]+[False]*5,
   colors=[CYAN]+[WHITE]*5)


# ==================================================================
# SLIDE 7d — My Contributions  (new blank slide)
# ==================================================================
contrib_slide = prs.slides.add_slide(blank_layout)

tb(contrib_slide, 0.4, 0.2, 12.0, 0.7,
   ["My Contributions"],
   sizes=[28], bolds=[True], colors=[YELLOW])

tb(contrib_slide, 0.4, 1.1, 12.2, 5.8,
   ["#1   Multi-Source Feature Fusion",
    "      First pipeline integrating PHQ-9 + GAD-7 + MSPSS + behavioral job-search signals.",
    "",
    "#2   Joint Depression-Anxiety Classification",
    "      Multi-label target treating depression & anxiety as comorbid but distinct dimensions.",
    "",
    "#3   SHAP-Driven Interpretability",
    "      Global + local explanations make risk outputs actionable for university career centers.",
    "",
    "#4   TRIPOD-Aligned Reproducibility",
    "      Strict reporting + stratified validation + open pipeline — closes replication gap.",
    "",
    "#5   Behavioral Variable Operationalization",
    "      Consistent metrics for search intensity, planfulness, rejection load."],
   sizes=[15,13,6,15,13,6,15,13,6,15,13,6,15,13],
   bolds=[True,False,False]*5,
   colors=([CYAN,WHITE,WHITE]*5)[:14])


# ==================================================================
# SLIDE 8 — References  (template slide index 7)
# ==================================================================
s = slides[7]
tb(s, 0.4, 1.3, 12.2, 5.8,
   ["[1]  Kroenke et al. (2001). The PHQ-9. J General Internal Medicine, 16(9), 606-613.",
    "[2]  Spitzer et al. (2006). GAD-7 brief measure. Archives of Internal Medicine, 166, 1092-1097.",
    "[3]  Zimet et al. (1988). Multidimensional Scale of Perceived Social Support. J Personality Assessment.",
    "[4]  Paul & Moser (2009). Unemployment impairs mental health: Meta-analyses. J Vocational Behavior.",
    "[5]  Collins et al. (2015). Transparent Reporting of prediction models (TRIPOD). BMJ, 350, g7594.",
    "[6]  Ramos-Lima et al. (2020). Predicting depression using ML — systematic review. Psychiatry Research.",
    "[7]  Lundberg & Lee (2017). A unified approach to interpreting model predictions (SHAP). NeurIPS.",
    "[8]  Wolff et al. (2019). PROBAST: Tool to assess prediction model risk of bias. Annals Internal Med."],
   sizes=[12]*8,
   bolds=[False]*8,
   colors=[WHITE]*8)


# ==================================================================
# Save
# ==================================================================
prs.save(OUTPUT)
print(f"SUCCESS: {OUTPUT} saved!")
slides_final = list(prs.slides)
print(f"Total slides: {len(slides_final)}")
for i, sl in enumerate(slides_final):
    texts = [sh.text.strip()[:50].replace('\n',' ')
             for sh in sl.shapes if hasattr(sh,'text') and sh.text.strip()]
    print(f"  Slide {i+1}: {texts[0] if texts else '(empty)'}")
