import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot_spectratype(df, color_top=10, **kwargs):
    all_df = df.groupby('cdr3_num_nts').copies_percent.sum().reset_index()
    top_df = df.sort_values('copies_percent', ascending=False)[:color_top]
    cdf = (
        pd
        .concat([top_df, all_df], sort=False)
        .fillna('')
        .sort_values('copies_percent', ascending=False)
    )[['cdr3_num_nts', 'copies_percent', 'cdr3_aa']]

    colors = ['#dddddd'] + sns.color_palette()
    g = sns.catplot(
        data=cdf,
        x='cdr3_num_nts',
        y='copies_percent',
        hue='cdr3_aa',
        kind='bar',
        dodge=False,
        height=kwargs.get('height', 8),
        aspect=kwargs.get('aspect', 3),
        legend=False,
        errorbar=None,
        palette=colors
    )

    g.set(xticklabels=[
        l if i % 3 == 0 else ''
        for i, l in enumerate(g.ax.get_xticklabels())
    ])
    g.set(xlabel='CDR3 Length (NT)', ylabel='% Total Copies')
    g.despine(left=True)
    plt.legend(loc='upper right')

    return g, cdf
