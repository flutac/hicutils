import numpy as np
import seaborn as sns

from matplotlib.colors import LinearSegmentedColormap


def _sort_presence(df):
    return df.reindex(
        (df / df).sort_values(list(df.columns)).index
    )


def plot_strings(
        df,
        pool,
        only_overlapping=True,
        overlapping_features=('clone_id', 'cdr3_aa', 'v_gene', 'j_gene'),
        scale=False,
        limit=None,
        ylabels='counts',
        order=None,
        **kwargs):
    '''
    Creates an overlap string plot where each row represents a clone and each
    column represents a pool.  Among other features, the definition of a clone
    can be modified and the heatmap can be boolean or scaled to the number of
    copies a clone comprises in each pool.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to use for tracking clones.
    pool : str
        The column to use for pooling clones into columns.
    only_overlapping : bool
        If set to ``True`` (the default), only clones overlapping at least two
        pools will be included in the overlap plot.
    overlapping_features : list
        The feature(s) to use to track clones across pools. By default the
        ``clone_id`` value is used. To alter this behavior, this value can be
        changed to any clonal information field such as ``cdr3_aa``,
        ``v_gene``, ``j_gene``, and ``cdr3_nt``.

        This is particularly useful to track clones across donors where the
        ``clone_id`` will differ but the ``cdr3_aa`` can be used instead.
    scale : bool or ``log``
        If ``scale=False`` (the default) presence of a clone in a pool is
        indicated by blue and absence by gray.  When ``scale=True`` the color
        of each clone/pool indicates the total number of copies.  Setting
        ``scale='log'`` changes the scale to be the log10 of copies.
    limit : int or None
        If set to an integer ``n``, limits the number of clones to the top
        ``n``.
    ylabels : ``counts`` or ``full``
        If set to ``counts`` (the default) y-axis ticks will be shown
        indicating the number of clones in the plot.  If set to ``full``, all
        features in ``overlapping_features`` will be shown for each row.
    order : function or None
        A function that is passed the pd.DataFrame and shall return a list of
        columns in the desired order.

    Returns
    -------
    A tuple ``(g, df)`` where ``g`` is a handle to the plot and ``df`` is the
    underlying DataFrame.


    '''
    assert ylabels in ('counts', 'full')
    assert scale in (False, True, 'log')

    df = df.copy()
    df['label'] = df[list(overlapping_features)].apply(
        lambda c: ' '.join([str(s) for s in c]),
        axis=1
    )

    pdf = df.pivot_table(
        index='label',
        columns=pool,
        values='copies',
        aggfunc=np.sum
    ).fillna(0)

    if len(pdf.columns) < 2:
        raise IndexError('Overlap plots must have at least two columns')

    col_clone_counts = (pdf / pdf).sum()

    pdf = pdf.div(pdf.sum(axis=0), axis=1) * 100
    if only_overlapping:
        pdf = pdf[(pdf / pdf).sum(axis=1) >= 2]
        if len(pdf) == 0:
            raise IndexError('No overlapping clones')

    pdf['total'] = pdf.sum(axis=1)
    pdf = (
        pdf
        .sort_values('total', ascending=False)
        .drop('total', axis=1)
    )
    ret_df = pdf.copy()

    pdf = pdf.head(limit or len(pdf))
    pdf = pdf.fillna(0)
    if order:
        pdf = pdf[order(pdf)]
    else:
        pdf = pdf[(pdf / pdf).sum().sort_values().index]

    pdf = pdf.reindex((pdf / pdf).sort_values(list(pdf.columns)).index)

    pdf.columns = [f'{c} ({col_clone_counts[c]:.0f})' for c in pdf.columns]

    if scale == 'log':
        pdf = (
            pdf
            .apply(np.log10)
            .replace(np.inf, 0)
            .replace([np.inf, -np.inf], np.nan)
        )

    if scale:
        pal = LinearSegmentedColormap.from_list(
            name='vdjtools',
            colors=['#2b8cbe', '#e0f3db', '#fdbb84'],
        )
    else:
        pal = sns.diverging_palette(10, 240, s=95, sep=1, as_cmap=True)
        pdf /= pdf

    with sns.axes_style('darkgrid'):
        g = sns.clustermap(
            data=pdf,
            cmap=pal,
            mask=pdf == 0,
            row_cluster=False,
            col_cluster=False,
            vmin=pdf.min().min() if scale else 0,
            vmax=pdf.max().max() if scale else 1,
            cbar_pos=(0, .25, .03, .4),
            dendrogram_ratio=(.2, .01) if scale else (0.01, 0.01),
            cbar_kws={
                'label': '% of column{}'.format(
                    ' (log scale)' if scale == 'log' else ''
                ),
            },
            **kwargs
        )

        if ylabels == 'full':
            g.ax_heatmap.set_yticklabels(
                g.ax_heatmap.get_yticklabels(),
                fontsize=8
            )
        elif ylabels == 'counts':
            labels = np.arange(1, len(pdf) + 1, max(1, len(pdf) // 5))
            g.ax_heatmap.set_yticks(labels)
            g.ax_heatmap.set_yticklabels(labels)

    g.cax.set_visible(scale)

    g.ax_heatmap.set_xlabel('')
    g.ax_heatmap.set_ylabel('')

    return g, ret_df
