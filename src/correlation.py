import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr, f_oneway, kruskal

# Load your dataset
df = pd.read_csv('../data/normalised_results.csv')
df = df[['Engagement Score', 'Engagement Level']]

# ANOVA
groups = df.groupby('Engagement Level')['Engagement Score'].apply(list)
f_val, p_val = f_oneway(*groups)
print(f'ANOVA F-value: {round(f_val, 2)}, P-value: {round(p_val, 2)}')

# Initialize the plot
plt.figure(figsize=(10, 6))
categories = sorted(df['Engagement Level'].unique())
colors = sns.color_palette("colorblind")
line_styles = ['solid', 'dotted', 'dashed']
label = {
    1: 'Baixo',
    2: 'Médio',
    3: 'Alto'
}

# Plot KDE for each category
for i, category in enumerate(categories):
    subset = df[df['Engagement Level'] == category]
    sns.kdeplot(subset['Engagement Score'],
                bw_adjust=0.5,
                cut=0,
                label=label[category],
                color=colors[i],
                linestyle=line_styles[i],
                linewidth=2)
    # mean_value = subset['Engagement Score'].mean()
    # plt.scatter(mean_value, 0.1, color=colors[i], s=50)

# Style adjustments for a clean look
plt.xlabel(
    'Densidade',
    fontsize=14,
    # labelpad=10
)
plt.ylabel(
    'Índice de Engajamento',
    fontsize=14,
    # labelpad=10
)
# plt.title('Engagement Scores by Engagement Levels', fontsize=14, pad=15)

legend = plt.legend(
    title='Nível de Engajamento',
    fontsize=10,
    title_fontsize=13,
    loc='upper right'
)

for text in legend.get_texts():
    text.set_fontsize(12)

legend.get_frame().set_linewidth(0)
legend.get_frame().set_facecolor('none')
legend.get_frame().set_alpha(0.5)
# plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.3)
sns.despine(left=True, bottom=True)

# Show the plot
plt.tight_layout()
plt.savefig('../images/engagement_scores_plot.png', dpi=400)
plt.show()
