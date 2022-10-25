import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt


def _basic_clustermap(df, normalize_by, cluster_by, figsize=None):
    assert normalize_by in ('rows', 'cols')
    if normalize_by == 'rows':
        df = df.div(df.sum(axis=1), axis=0)
    else:
        df = df.div(df.sum(axis=0), axis=1)
    g = sns.clustermap(
        data=df,
        cmap='coolwarm',
        figsize=figsize or (20, len(df) * 2),
        mask=df == 0,
        linewidths=1,
        row_cluster=cluster_by in ('both', 'rows') and len(df) > 2,
        col_cluster=cluster_by in ('both', 'cols') and len(df) > 2,
        xticklabels=True,
        yticklabels=True
    )
    g.cax.set_visible(False)
    g.ax_heatmap.set_xlabel('')
    g.ax_heatmap.set_ylabel('')
    plt.setp(g.ax_heatmap.get_yticklabels(), va='center')
    return g


def plot_gene_usage(df, pool, gene, size_metric='clones', normalize_by='rows',
                    cluster_by='both', figsize=(30, 10)):
    assert size_metric in ('clones', 'copies', 'uniques')
    assert cluster_by in ('both', 'rows', 'cols')
    df = df.copy()
    df.loc[:, 'clones'] = 1
    pdf = df.pivot_table(
        index=pool, columns=gene, values=size_metric, aggfunc=np.sum
    ).fillna(0)

    total_clones = df.groupby(pool).clone_id.nunique()
    pdf.index = [
        '{} ({})'.format(c, int(total_clones.loc[c]))
        for c in pdf.index
    ]

    g = _basic_clustermap(pdf, normalize_by, cluster_by, figsize)
    return g, pdf
