import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_top_clones(
        df,
        cutoff=20,
        figsize=(12, 8),
        color=sns.color_palette()[3],
        annotate=False):
    df = df.sort_values('copies', ascending=False)
    df['rank'] = np.arange(1, len(df) + 1)

    fig, ax = plt.subplots(figsize=figsize)
    cdf = df[:cutoff]
    g = sns.barplot(
        x='rank',
        y='copies_percent',
        data=cdf,
        color=color,
        ax=ax
    )
    g.set_xlabel('Rank')
    g.set_ylabel('% of Total Copies')

    if annotate:
        for i, p in enumerate(g.patches):
            ax.annotate(
                df.iloc[i]['clone_id'],
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', fontsize=10, color='black',
                rotation=90, xytext=(0, 30),
                textcoords='offset points'
            )
    a = plt.axes([0.69, 0.58, .2, .2], facecolor='y')
    colors = [
        sns.color_palette()[3],
        sns.color_palette('Reds', n_colors=5)[1]
    ]
    frac = df[:cutoff]['copies_percent'].sum()

    top_df = pd.DataFrame({
        'percent': [frac, max(0, 100 - frac)]
    }, index=['top', 'rest'])

    ax = top_df.plot.pie(
        y='percent',
        colors=colors,
        legend=False,
        labels=['{}%'.format(round(frac, 1)), ''],
        ax=a
    )
    ax.set_title('% of Total Copies\n({})'.format(df.copies.sum()))
    ax.set_ylabel('')
    return g, cdf
