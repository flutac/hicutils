from collections import Counter
import pandas as pd

from .heatmap import basic_clustermap


def _get_counts(pdf, size_metric):
    # TODO: Fix this to count clones only once if size_metric = clones
    return pd.DataFrame(pdf.cdr3_aa.apply(
        lambda r: pd.Series(Counter(r))
    ).fillna(0).mul(pdf[size_metric], axis=0).sum()).T


def plot_cdr3_aa_usage(df, pool, size_metric='clones', normalize_by='rows',
                       cluster_by='both', figsize=(20, 10)):
    assert size_metric in ('clones', 'copies', 'uniques')
    assert cluster_by in ('both', 'rows', 'cols')
    df = df.copy()

    pdf = pd.concat(
        {k: _get_counts(d, size_metric) for k, d in df.groupby(pool)},
        sort=True
    ).fillna(0)
    pdf.index = pdf.index.droplevel(1)

    g = basic_clustermap(pdf, normalize_by, cluster_by)
    return g, pdf
