import numpy as np

from .heatmap import basic_clustermap


def plot_gene_usage(df, pool, gene, size_metric='clones', normalize_by='rows',
                    cluster_by='both', figsize=(30, 10)):
    '''
    Generates a gene-usage heatmap showing the utilization of each V or J gene
    based on pools.

    Parameters
    -----------
    df : pd.DataFrame
        The DataFrame to use as the source of gene usage information.
    gene : str (``v_gene`` or ``j_gene``)
        The gene to plot. Must be either ``v_gene`` or ``j_gene``.
    size_metric : str
        The size metric which is plotted as the intensity of each cell.  Must
        be one of ``clones``, ``copies``, or ``uniques``.
    normalize_by : str
        Sets how to normalize the plot.  If set to ``rows`` (the default) each
        row is normalized to sum to one.  Setting it to ``cols`` causes each
        column (gene) to sum to one.
    cluster_by : str (``rows``, ``cols``, or ``both``) or None
        Sets which clustering to display.  Valid values are ``rows``, ``cols``,
        ``both``, or clustering can be disabled with ``None``.

    Returns
    -------
    A tuple ``(g, df)`` where ``g`` is a handle to the plot and ``df`` is the
    underlying DataFrame.

    '''

    assert gene in ('v_gene', 'j_gene')
    assert size_metric in ('clones', 'copies', 'uniques')
    assert cluster_by in ('both', 'rows', 'cols')
    df = df.copy()
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
