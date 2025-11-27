import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import os

# Create directory if not exists
output_dir = "c:/Users/ايهم/Desktop/رحال/docs/figures"
os.makedirs(output_dir, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
colors = ['#142C63', '#F57C00', '#D92B7D', '#A6D86B', '#FFD54F']

def create_figure_1_preprocessing():
    """Figure 1: Data Preprocessing Pipeline"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Nodes
    steps = [
        (1, 4, "Raw Data\n(CSV/Excel)", colors[0]),
        (3, 4, "Data Cleaning\n(Missing Values)", colors[1]),
        (5, 4, "Transformation\n(Normalization)", colors[2]),
        (7, 4, "Feature Engineering\n(Encoding)", colors[3]),
        (9, 4, "Processed Data\n(Ready for ML)", colors[4])
    ]
    
    for x, y, text, color in steps:
        rect = patches.FancyBboxPatch((x-0.8, y-0.5), 1.6, 1, boxstyle="round,pad=0.1", 
                                    linewidth=2, edgecolor=color, facecolor='white')
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold', color='#333')
        
        # Arrows
        if x < 9:
            ax.arrow(x+0.9, y, 1.0, 0, head_width=0.15, head_length=0.2, fc='#666', ec='#666')

    plt.title("Figure 1: Data Preprocessing Pipeline", fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_1_Data_Preprocessing.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_figure_2_system_design():
    """Figure 2: System Design Prototype"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Layers
    layers = [
        ("User Layer", 6.5, ["Visitors", "Admin"], colors[0]),
        ("Application Layer", 4.5, ["Streamlit Dashboard", "Virtual Assistant"], colors[1]),
        ("Intelligence Layer", 2.5, ["Crowd Prediction", "Recommendation", "Sentiment Analysis"], colors[2]),
        ("Data Layer", 0.5, ["Supabase DB", "External APIs"], colors[3])
    ]
    
    for name, y, items, color in layers:
        # Layer Box
        rect = patches.Rectangle((1, y), 10, 1.5, linewidth=2, edgecolor=color, facecolor=color+'20', linestyle='--')
        ax.add_patch(rect)
        ax.text(1.2, y+1.2, name, fontsize=12, fontweight='bold', color=color)
        
        # Items
        item_width = 8 / len(items)
        for i, item in enumerate(items):
            x = 2 + i * (item_width + 0.5)
            box = patches.FancyBboxPatch((x, y+0.3), item_width, 0.8, boxstyle="round,pad=0.1", 
                                       linewidth=1, edgecolor=color, facecolor='white')
            ax.add_patch(box)
            ax.text(x + item_width/2, y+0.7, item, ha='center', va='center', fontsize=9)

    # Arrows between layers
    ax.arrow(6, 6.5, 0, -0.5, head_width=0.2, head_length=0.2, fc='#666', ec='#666')
    ax.arrow(6, 4.5, 0, -0.5, head_width=0.2, head_length=0.2, fc='#666', ec='#666')
    ax.arrow(6, 2.5, 0, -0.5, head_width=0.2, head_length=0.2, fc='#666', ec='#666')

    plt.title("Figure 2: System Architecture", fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_2_System_Design.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_figure_3_data_loading():
    """Figure 3: Data Loading (ETL)"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # ETL Process
    steps = [
        (2, 2.5, "Extract\n(Raw Files)", colors[0]),
        (5, 2.5, "Transform\n(Python/Pandas)", colors[1]),
        (8, 2.5, "Load\n(Supabase)", colors[2])
    ]
    
    for x, y, text, color in steps:
        circle = patches.Circle((x, y), 1.2, linewidth=2, edgecolor=color, facecolor='white')
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold')
        
        if x < 8:
            ax.arrow(x+1.3, y, 1.4, 0, head_width=0.2, head_length=0.3, fc='#333', ec='#333', width=0.05)

    plt.title("Figure 3: ETL Data Loading Process", fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_3_Data_Loading.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_figure_4_accuracy():
    """Figure 4: Data Accuracy Using Random Forest"""
    models = ['Random Forest', 'Decision Tree', 'SVM', 'KNN']
    accuracy = [90.4, 85.2, 82.1, 78.5]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(models, accuracy, color=[colors[0], '#ccc', '#ccc', '#ccc'])
    
    # Add values
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Figure 4: Model Accuracy Comparison', fontsize=14, pad=20)
    
    # Highlight the best model
    bars[0].set_color(colors[1])
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_4_Data_Accuracy.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_figure_5_recommendation():
    """Figure 5: Recommendation System Experiment"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Flow
    steps = [
        (2, 4.5, "User Input\n(Age, Preferences)", colors[0]),
        (5, 4.5, "Clustering\n(K-Means)", colors[1]),
        (8, 4.5, "User Segment\n(e.g. Family)", colors[2]),
        (5, 1.5, "Recommendation\nEngine", colors[3]),
        (8, 1.5, "Personalized\nSuggestions", colors[4])
    ]
    
    for x, y, text, color in steps:
        box = patches.FancyBboxPatch((x-1.2, y-0.6), 2.4, 1.2, boxstyle="round,pad=0.1", 
                                   linewidth=2, edgecolor=color, facecolor='white')
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')

    # Arrows
    ax.arrow(3.3, 4.5, 0.4, 0, head_width=0.15, head_length=0.2, fc='#666', ec='#666') # Input -> Cluster
    ax.arrow(6.3, 4.5, 0.4, 0, head_width=0.15, head_length=0.2, fc='#666', ec='#666') # Cluster -> Segment
    ax.arrow(8, 3.8, 0, -1.0, head_width=0.15, head_length=0.2, fc='#666', ec='#666') # Segment -> Engine (down)
    ax.arrow(6.3, 1.5, 0.4, 0, head_width=0.15, head_length=0.2, fc='#666', ec='#666') # Engine -> Output
    
    # Feedback loop
    ax.arrow(5, 2.2, 0, 1.6, head_width=0.15, head_length=0.2, fc='#666', ec='#666', linestyle=':') # Engine -> Cluster

    plt.title("Figure 5: Recommendation System Logic", fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Figure_5_Recommendation_System.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_gantt_chart():
    """Appendix A: Gantt Chart"""
    tasks = [
        ("Initialization", 1, 2),
        ("Data Collection", 2, 1),
        ("Database Design", 3, 1),
        ("ETL Implementation", 4, 1),
        ("AI Modeling", 5, 4),
        ("Dashboard Dev", 9, 4),
        ("Testing", 13, 1),
        ("Documentation", 14, 1),
        ("Final Review", 15, 1)
    ]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, (task, start, duration) in enumerate(tasks):
        ax.barh(task, duration, left=start, height=0.5, color=colors[i % len(colors)], alpha=0.8)
        ax.text(start + duration/2, i, f"{duration}w", ha='center', va='center', color='white', fontweight='bold')
    
    ax.set_xlabel('Weeks')
    ax.set_title('Appendix A: Project Timeline (Gantt Chart)', fontsize=14, pad=20)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/Appendix_A_Gantt_Chart.png", dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_figure_1_preprocessing()
    create_figure_2_system_design()
    create_figure_3_data_loading()
    create_figure_4_accuracy()
    create_figure_5_recommendation()
    create_gantt_chart()
    print("All figures generated successfully in docs/figures/")
