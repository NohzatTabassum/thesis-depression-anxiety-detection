"""
Reorder slides: put extra slides (12-15) in correct position after slide 7 (Methodology),
remove Certification slide (index 8), keep Thank You and Questions at end.

Current:  1=Title, 2=Outlines, 3=ProbStmt, 4=Objectives, 5=ResearchGap,
          6=LitReview, 7=Methodology, 8=References, 9=Certifications,
          10=ThankYou, 11=Questions,
          12=RQ&Scope, 13=FeatureSpace, 14=Eval&SHAP, 15=MyContribs

Target:   1=Title, 2=Outlines, 3=ProbStmt, 4=ResearchGap, 5=Objectives,
          6=RQ&Scope, 7=LitReview, 8=Methodology, 9=FeatureSpace,
          10=Eval&SHAP, 11=MyContribs, 12=References, 13=ThankYou, 14=Questions
"""

from pptx import Presentation
from pptx.oxml.ns import qn

prs = Presentation('Mid_Defense_FINAL.pptx')
prs_el   = prs.part._element
sldIdLst = prs_el.find(qn('p:sldIdLst'))

# Current 0-based indices:
# 0=Title,1=Outlines,2=ProbStmt,3=Objectives,4=ResearchGap,
# 5=LitReview,6=Methodology,7=References,8=Certifications,
# 9=ThankYou,10=Questions,
# 11=RQ&Scope,12=FeatureSpace,13=Eval&SHAP,14=MyContribs

# Target order (skip Certifications index 8):
target = [0, 1, 2, 4, 3, 11, 5, 6, 12, 13, 14, 7, 9, 10]

all_sld = list(sldIdLst)
for el in all_sld:
    sldIdLst.remove(el)
for idx in target:
    sldIdLst.append(all_sld[idx])

prs.save('Mid_Defense_FINAL.pptx')
print("Reordered successfully!")

# Verify
prs2 = Presentation('Mid_Defense_FINAL.pptx')
for i, sl in enumerate(prs2.slides):
    texts = [sh.text.strip()[:55].replace('\n',' ')
             for sh in sl.shapes if hasattr(sh,'text') and sh.text.strip()]
    print(f"  Slide {i+1:2d}: {texts[0] if texts else '(empty)'}")
