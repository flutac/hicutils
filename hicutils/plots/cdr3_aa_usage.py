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
    '''
    Plots CDR3 amino-acid usage separated by pool.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to use as the source of CDR3 amino-acid usage
        information.
    pool : str
        The pooling column to use for each row of the heatmap.
    size_metric : str
        The size metric which is plotted as the intensity of each cell.  Must
        be one of ``clones``, ``copies``, or ``uniques``.
    normalize_by : str
        Sets how to normalize the plot.  If set to ``rows`` (the default) each
        row is normalized to sum to one.  Setting it to ``cols`` causes each
        column (amino-acid) to sum to one.
    cluster_by : str (``rows``, ``cols``, or ``both``) or None
        Sets which clustering to display.  Valid values are ``rows``, ``cols``,
        ``both``, or clustering can be disabled with ``None``.

    Returns
    -------
    A tuple ``(g, df)`` where ``g`` is a handle to the plot and ``df`` is the
    underlying DataFrame.

    '''

    assert size_metric in ('clones', 'copies', 'uniques')
    df = df.copy()

    pdf = pd.concat(
        {k: _get_counts(d, size_metric) for k, d in df.groupby(pool)},
        sort=True
    ).fillna(0)
    pdf.index = pdf.index.droplevel(1)

    g = basic_clustermap(pdf, normalize_by, cluster_by, figsize=figsize)
    return g, pdf
