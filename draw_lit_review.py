import matplotlib.pyplot as plt

# Data for the table
columns = ["Topic", "Key Finding", "Research Gap"]
cell_text = [
    ["PHQ-9 / GAD-7", "88% sensitivity at cutoff >= 10", "Used in isolation only"],
    ["Job Insecurity", "29% elevated depression risk", "Ignored in ML models"],
    ["Social Support (MSPSS)", "Inverse correlation with distress", "Omitted from pipelines"],
    ["ML for Depression", "SVM/RF/BERT; AUC up to 0.89", "Opaque, non-reproducible"]
]

# Create figure and axes
fig, ax = plt.subplots(figsize=(10, 3.5))
ax.axis('off')

# Add table
table = ax.table(cellText=cell_text, colLabels=columns, cellLoc='center', loc='center')

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 2.5)  # Scale width and height

# Style headers
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#004d40')
    else:
        # Alternating row colors
        if row % 2 == 0:
            cell.set_facecolor('#e0f2f1')
        else:
            cell.set_facecolor('#ffffff')

plt.title('Literature Review Summary', fontsize=16, fontweight='bold', color='#263238', y=0.95)
plt.savefig('literature_review_table.png', dpi=300, bbox_inches='tight')
plt.close()
