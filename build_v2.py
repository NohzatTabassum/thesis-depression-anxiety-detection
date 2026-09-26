import collections 
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation('DRISHTI-Bn_Mid_Defense_Final.pptx')

# Helper functions
def set_text(shape, text, font_size=None, bold=False):
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    if font_size:
        run.font.size = Pt(font_size)
    run.font.bold = bold

def add_bullet_box(slide, left, top, width, height, bullets, font_size=14, title=None, title_size=16):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True

    if title:
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = title
        run.font.size = Pt(title_size)
        run.font.bold = True

    for bullet in bullets:
        p = tf.add_paragraph()
        p.level = 0
        run = p.add_run()
        run.text = bullet
        run.font.size = Pt(font_size)
    return txBox

def delete_shape(slide, shape_to_delete):
    sp = shape_to_delete._element
    sp.getparent().remove(sp)

def clear_and_remove_pictures(slide, keep_titles=True):
    shapes_to_delete = []
    for shape in slide.shapes:
        if shape.shape_type == 13: # PICTURE
            shapes_to_delete.append(shape)
        elif shape.has_text_frame:
            # Check if it's a title or slide number, usually we don't clear those
            if keep_titles and shape.is_placeholder and shape.placeholder_format.type in [1, 3, 13, 15]: 
                # 1: Title, 3: Subtitle, 13: Slide Number, 15: Footer
                continue
            elif "Title" in shape.name or "Slide Number" in shape.name:
                continue
            # Clear text in content placeholders and other text boxes
            shape.text_frame.clear()
    
    for shape in shapes_to_delete:
        delete_shape(slide, shape)

# Slide 1 (Title)
s1 = prs.slides[0]
for sh in s1.shapes:
    if "Title 1" in sh.name:
        set_text(sh, "AI-Assisted Early Risk Detection of Depression and Anxiety in University Students During Job Search", font_size=28, bold=True)
    if "Subtitle 2" in sh.name:
        set_text(sh, "Presented By:\n[Your Name] (ID- [Your ID])\n\nSupervisor: [Supervisor Name]\nDepartment of Software Engineering, Daffodil International University", font_size=16, bold=True)

# Slide 2 (Outlines)
s2 = prs.slides[1]
clear_and_remove_pictures(s2)
add_bullet_box(s2, 1.0, 1.5, 11.0, 5.5, [
    "01  |  Problem Statement",
    "02  |  Objectives",
    "03  |  Research Gap",
    "04  |  Literature Review",
    "05  |  Methodology",
    "06  |  References"
], font_size=18)

# Slide 3 (Problem Statement)
s3 = prs.slides[2]
clear_and_remove_pictures(s3)
add_bullet_box(s3, 0.5, 1.5, 12.0, 5.5, [
    "Students face severe psychological strain during the school-to-work transition. Labour market uncertainty creates distress comparable to actual unemployment.",
    "Standard screening tools (PHQ-9, GAD-7) are used in isolation. They ignore behavioral and social signals — missing many at-risk students.",
    "Most AI/ML models use single-modality data (e.g., social media only), are opaque, lack explainability, and are not reproducible.",
    "Severe class imbalance in existing datasets causes high-risk minority groups to be systematically under-detected."
], font_size=16)

# Slide 4 (Objectives)
s4 = prs.slides[3]
clear_and_remove_pictures(s4)
add_bullet_box(s4, 0.5, 1.5, 12.0, 5.5, [
    "O1: Construct an integrated feature space combining PHQ-9, GAD-7, MSPSS with quantified job-search behavioral indicators.",
    "O2: Develop and compare supervised ML baselines (LR, SVM, RF, XGBoost) for joint depression-anxiety risk classification.",
    "O3: Apply SHAP explainability to generate interpretable feature-level explanations for non-clinical decision support.",
    "O4: Operationalize behavioral variables (search intensity, planfulness, rejection load) with consistent measurement definitions.",
    "O5: Implement a TRIPOD-aligned evaluation workflow using stratified CV and macro-F1 with class-imbalance-aware analysis."
], font_size=16)

# Slide 5 (Research Gap)
s5 = prs.slides[4]
clear_and_remove_pictures(s5)
add_bullet_box(s5, 0.5, 1.5, 12.0, 5.5, [
    "Gap 1: Models rely on single-modality data — social media OR clinical records. Perceived social support (MSPSS) is omitted.",
    "Gap 2: No joint depression-anxiety pipeline for student job-search context exists.",
    "Gap 3: Deep learning models are opaque — no SHAP or interpretability for practitioners.",
    "Gap 4: Behavioral signals (search intensity, planfulness) are inconsistently defined.",
    "Gap 5: TRIPOD & PROBAST violations are widespread — reproducibility is lacking.",
    "Gap 6: Class imbalance causes high-risk minority groups to be under-detected."
], font_size=16)

# Slide 6 (Literature Review)
s6 = prs.slides[5]
clear_and_remove_pictures(s6)
for shape in s6.shapes:
    if shape.has_table:
        table = shape.table
        # Adjust table content
        table.cell(0, 0).text = "Topic"
        table.cell(0, 1).text = "Key Finding"
        table.cell(0, 2).text = "Research Gap"
        
        table.cell(1, 0).text = "PHQ-9 / GAD-7"
        table.cell(1, 1).text = "88% sensitivity at cutoff >= 10"
        table.cell(1, 2).text = "Used in isolation only"
        
        table.cell(2, 0).text = "Job Insecurity"
        table.cell(2, 1).text = "29% elevated depression risk"
        table.cell(2, 2).text = "Ignored in ML models"
        
        table.cell(3, 0).text = "Social Support (MSPSS)"
        table.cell(3, 1).text = "Inverse correlation with distress"
        table.cell(3, 2).text = "Omitted from pipelines"
        
        table.cell(4, 0).text = "ML for Depression"
        table.cell(4, 1).text = "SVM/RF/BERT; AUC up to 0.89"
        table.cell(4, 2).text = "Opaque, non-reproducible"
        
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(14)

# Slide 7 (Methodology)
s7 = prs.slides[6]
clear_and_remove_pictures(s7)
add_bullet_box(s7, 0.5, 1.5, 12.0, 5.5, [
    "Phase 1 — Data Collection: Survey via secure web platform (PHQ-9, GAD-7, MSPSS + behavioral + demographics).",
    "Phase 2 — Preprocessing: Median imputation, Z-score standardization, One-hot encoding, Winsorize outliers, SMOTE / cost-sensitive weights.",
    "Phase 3 — Modeling: Baselines (LR, SVM, RF, XGBoost), Joint multi-label target, Stratified k-fold CV + grid search.",
    "Phase 4 — Explainability & Evaluation: SHAP (global + local), Confusion matrix, FN analysis, Metrics (Macro-F1, Precision, Recall, ROC-AUC)."
], font_size=16)

# Slide 8 (References)
s8 = prs.slides[7]
clear_and_remove_pictures(s8)
add_bullet_box(s8, 0.5, 1.5, 12.0, 5.5, [
    "[1] Kroenke et al. (2001). The PHQ-9. J General Internal Medicine, 16(9), 606-613.",
    "[2] Spitzer et al. (2006). GAD-7 brief measure. Archives of Internal Medicine, 166, 1092-1097.",
    "[3] Zimet et al. (1988). Multidimensional Scale of Perceived Social Support. J Personality Assessment.",
    "[4] Paul & Moser (2009). Unemployment impairs mental health: Meta-analyses. J Vocational Behavior.",
    "[5] Collins et al. (2015). Transparent Reporting of prediction models (TRIPOD). BMJ, 350, g7594.",
    "[6] Ramos-Lima et al. (2020). Predicting depression using ML — systematic review. Psychiatry Research.",
    "[7] Lundberg & Lee (2017). A unified approach to interpreting model predictions (SHAP). NeurIPS.",
    "[8] Wolff et al. (2019). PROBAST: Tool to assess prediction model risk of bias. Annals Internal Med."
], font_size=14)

# Keeping Certification and Thank You as is.

prs.save('Mid_Defense_FINAL_v2.pptx')
print("Saved Mid_Defense_FINAL_v2.pptx successfully!")
