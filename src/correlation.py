import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway


class Analysis:
    def __init__(self, df_path: str):
        self.df_path = df_path
        self.df = pd.read_csv(df_path)

    def anova(self):
        groups = self.df.groupby('Engagement Level')['Engagement Score'].apply(list)
        f_val, p_val = f_oneway(*groups)
        return {'F-value': round(f_val, 2), 'P-value': round(p_val, 2)}

    def plot_kde(self, st: bool = False):
        plt.figure(figsize=(10, 6))
        categories = sorted(self.df['Engagement Level'].unique())
        colors = sns.color_palette("colorblind")
        line_styles = ['solid', 'dotted', 'dashed']
        label = {
            1: 'Low',
            2: 'Average',
            3: 'High'
        }

        for i, category in enumerate(categories):
            subset = self.df[self.df['Engagement Level'] == category]
            sns.kdeplot(subset['Engagement Score'],
                        bw_adjust=0.5,
                        cut=0,
                        label=label[category],
                        color=colors[i],
                        linestyle=line_styles[i],
                        linewidth=2)
            # mean_value = subset['Engagement Score'].mean()
            # plt.scatter(mean_value, 0.1, color=colors[i], s=50)

        plt.xlabel('Engagement Index', fontsize=14)
        plt.ylabel('Density', fontsize=14)
        # plt.title('Engagement Scores by Engagement Levels', fontsize=14, pad=15)

        legend = plt.legend(
            title='Engagement Level',
            fontsize=10,
            title_fontsize=13,
            loc='upper right'
        )

        for text in legend.get_texts():
            text.set_fontsize(12)

        legend.get_frame().set_linewidth(0)
        legend.get_frame().set_facecolor('none')
        legend.get_frame().set_alpha(0.5)
        sns.despine(left=True, bottom=True)

        plt.tight_layout()
        # plt.savefig('../images/engagement_scores_plot.png', dpi=300)
        if st:
            return plt.gcf()
        else:
            plt.show()
