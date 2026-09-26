import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set a wider figure for horizontal layout
fig, ax = plt.subplots(figsize=(18, 5))
ax.axis('off')

# Data
phases = [
    ("Phase 1: Data Collection", 
     "• Survey via secure web platform\n• Instruments: PHQ-9, GAD-7, MSPSS\n• Behavioral & Demographics"),
    ("Phase 2: Preprocessing",
     "• Median imputation & Z-score\n• One-hot encoding & Winsorize\n• Class imbalance handling:\n  SMOTE or class-weighted"),
    ("Phase 3: Modeling",
     "• Baselines: LR, SVM, RF, XGBoost\n• Joint depression–anxiety target\n• Stratified k-fold CV\n• Grid search hyperparameter tuning"),
    ("Phase 4: Evaluation",
     "• SHAP (global + local)\n• Confusion matrix & FN analysis\n• Metrics: Macro-F1, Precision,\n  Recall, Specificity, ROC-AUC")
]

# Soft, professional colors
colors = ['#E3F2FD', '#E8F5E9', '#FFF3E0', '#F3E5F5']
edge_colors = ['#1565C0', '#2E7D32', '#EF6C00', '#7B1FA2']
title_colors = ['#0D47A1', '#1B5E20', '#E65100', '#4A148C']

box_width = 0.21
box_height = 0.6
y_start = 0.2

x_positions = [0.03, 0.28, 0.53, 0.78]

for i, (title, content) in enumerate(phases):
    x = x_positions[i]
    
    # Draw box with shadow effect (slight offset)
    shadow = patches.FancyBboxPatch((x+0.005, y_start-0.015), box_width, box_height, 
                                  boxstyle="round,pad=0.03", 
                                  edgecolor='none', facecolor='#000000', alpha=0.1)
    ax.add_patch(shadow)
    
    # Main box
    rect = patches.FancyBboxPatch((x, y_start), box_width, box_height, 
                                  boxstyle="round,pad=0.03", 
                                  edgecolor=edge_colors[i], facecolor=colors[i], lw=2)
    ax.add_patch(rect)
    
    # Add text
    ax.text(x + box_width/2, y_start + box_height - 0.05, title, 
            fontsize=15, fontweight='bold', va='top', ha='center', color=title_colors[i])
    
    # Line separator
    ax.plot([x + 0.02, x + box_width - 0.02], [y_start + box_height - 0.12, y_start + box_height - 0.12], 
            color=edge_colors[i], lw=1, alpha=0.5)
            
    ax.text(x + 0.02, y_start + box_height - 0.17, content, 
            fontsize=12, va='top', ha='left', color='#333333', linespacing=1.6)
    
    # Draw arrow pointing right
    if i < len(phases) - 1:
        arrow_x_start = x + box_width + 0.02
        arrow_x_end = x_positions[i+1] - 0.02
        ax.annotate('', xy=(arrow_x_end, y_start + box_height/2), xytext=(arrow_x_start, y_start + box_height/2),
                    arrowprops=dict(facecolor='#555555', edgecolor='#555555', shrink=0.0, width=3, headwidth=12))

# Title and Subtitle
plt.figtext(0.5, 1.05, 'Research Methodology Pipeline', fontsize=22, fontweight='bold', ha='center', color='#263238')
plt.figtext(0.5, 0.95, 'Planned workflow (data collection in progress)', fontsize=15, style='italic', ha='center', color='#D32F2F')

plt.savefig('methodology_diagram.png', dpi=300, bbox_inches='tight')
plt.close()
