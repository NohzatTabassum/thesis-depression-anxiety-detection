"""
Clear placeholder/instruction text from template slides so only our content shows.
"""
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor

CLEAR_TEXTS = [
    "TITLE", "Presented By-", "Student Name (ID)", "Supervisor: ABC",
    "List down your objectives",
    "Defines the boundaries",
    "List down all the relevant works",
    "Provide a work-flow diagram",
    "Be specific to select",
    "Be specific to compare",
    "Logo",
]

def should_clear(text):
    for phrase in CLEAR_TEXTS:
        if phrase.lower() in text.lower():
            return True
    return False

prs = Presentation('Mid_Defense_FINAL.pptx')

for slide in prs.slides:
    for shape in slide.shapes:
        if not hasattr(shape, 'text_frame'):
            continue
        if not shape.text.strip():
            continue
        if should_clear(shape.text):
            # Make text invisible (white/transparent) instead of deleting shape
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    run.text = ''

prs.save('Mid_Defense_FINAL.pptx')
print("Placeholder text cleared!")

# Quick verify slide 1
prs2 = Presentation('Mid_Defense_FINAL.pptx')
print("\nSlide 1 shapes:")
for sh in list(prs2.slides)[0].shapes:
    if hasattr(sh,'text') and sh.text.strip():
        print(f"  {sh.name}: {sh.text.strip()[:60].replace(chr(10),' | ')}")
