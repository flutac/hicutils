import numpy as np

from .heatmap import basic_clustermap


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

    g = basic_clustermap(pdf, normalize_by, cluster_by, figsize)
    return g, pdf
