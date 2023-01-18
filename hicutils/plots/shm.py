import re

import pandas as pd
import seaborn as sns


def _add_counts(df, field):
    sizes = df.groupby(field).size()
    df[field] = df[field].apply(lambda f: f'{f} ({sizes[f]})')
    return df


def _get_shm(pdf, df, pool, size_metric):
    total = df[df[pool] == pdf.name[1]][size_metric].sum()
    ret = pd.Series({'size': 100 * pdf[size_metric].sum() / total})
    return ret


def plot_shm_distribution(df, pool, size_metric, palette=None, order=None,
                          **kwargs):
    '''
    Plots the SHM distribution of a pooled DataFrame using either clones,
    copies, or uniques as a size metric.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame used to plot the SHM distribution.
    pool : str
        The pool to use for plotting.
    size_metric : str
        The metric to determine each clones' size.  Must be ``clones``,
        ``copies``, or ``uniques``.

    Returns
    -------
    A tuple ``(g, df)`` where ``g`` is a handle to the plot and ``df`` is the
    underlying DataFrame.

    '''

    assert size_metric in ('clones', 'copies', 'uniques')
    df = df.copy()
    if order:
        df['order'] = df[pool].apply(order.index)
        df = df.sort_values('order').drop('order', axis=1)
    df = _add_counts(df, pool)
    df['shm'] = df['shm'].round()
    df = (
        df
        .groupby(['shm', pool])
        .apply(_get_shm, df, pool, size_metric).reset_index()
    )

    final_colors = None
    if palette:
        final_colors = {}
        for label in df[pool].unique():
            for feature, color in palette.items():
                if label.rsplit('(')[0].strip() == feature.strip():
                    final_colors[label] = color

    with sns.plotting_context('poster'):
        g = sns.relplot(
            data=df,
            x='shm',
            y='size',
            hue=pool,
            kind='line',
            height=kwargs.pop('height', 8),
            aspect=kwargs.pop('aspect', 1.5),
            palette=final_colors,
            **kwargs
        )
        g.set(
            xlabel='SHM (% of Mutated V-gene NT)',
            ylabel=f'% of {size_metric}',
        )
    return g, df


def plot_shm_aggregate(df, pool, **kwargs):
    '''
    Categorically plots the SHM of each pool.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame used to plot the SHM.
    pool : str
        The pool to use for plotting.

    Returns
    -------
    A tuple ``(g, df)`` where ``g`` is a handle to the plot and ``df`` is the
    underlying DataFrame.

    '''

    g = sns.catplot(
        data=df,
        x=pool,
        y='shm',
        kind=kwargs.pop('kind', 'violin'),
        **kwargs
    )
    g.set(xlabel='', ylabel='SHM %')
    return g, df


def _clone_frac_norm(df):
    df = df.groupby('shm_bucket').clone_id.nunique()
    df = 100 * df / df.sum()
    return df.to_frame()


def _get_bucket(shm, buckets=(1, 2, 5, 10, 20)):
    buckets = [0, *buckets]
    for i, b in enumerate(buckets[:-1]):
        if b <= shm < buckets[i + 1]:
            return f'[{b}-{buckets[i + 1]})'
    return f'{buckets[-1]}+'


def _sort_buckets(buckets):
    bucket_info = [
        (
            int(re.search(r'\d+', b).group()) if '-' in b
            else int(re.search(r'\d+', b).group()) + 1,
            b
        )
        for b in buckets
    ]
    return [
        buckets.index(b[1]) for b in sorted(bucket_info, key=lambda b: b[0])
    ]


def plot_shm_range(df, pool, buckets=(1, 10, 25), **kwargs):
    '''
    Plot the range of clonal SHM for each pool.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame used to plot the SHM.
    pool : str
        The pool to use for plotting.
    buckets : list(int)
        A list of cut-points to bin SHM.  The default is ``(1, 10, 25)``
        meaning clones will be stratified by SHM into the buckets ``[1, 10)``,
        ``[10, 25)``, and ``25+``.  All intervals are left-closed; that is the
        lesser value in each interval is inclusive and the greater value is
        exclusive.

    Returns
    -------
    A tuple ``(g, df)`` where ``g`` is a handle to the plot and ``df`` is the
    underlying DataFrame.

    '''

    buckets = [b for b in buckets if b < df.shm.max()]
    df = df.copy()
    df['shm_bucket'] = df['shm'].apply(_get_bucket, buckets=buckets)
    df = (
        df
        .groupby(pool)
        .apply(_clone_frac_norm)
        .unstack()['clone_id']
    )
    df = df[[df.columns[i] for i in _sort_buckets(list(df.columns))]]
    with sns.plotting_context('poster'):
        g = (
            df
            .plot
            .bar(
                stacked=True,
                figsize=kwargs.pop('figsize', (12, 8)),
                color=kwargs.pop('color', sns.color_palette()[1:]),
                legend='reverse'
            )
        )
        g.set(xlabel='', ylabel='% of Mutated Clones')
        handles, labels = g.get_legend_handles_labels()
        g.legend(
            reversed(handles),
            reversed(labels),
            loc='upper right',
            bbox_to_anchor=(1.3, 1),
            title='SHM %'
        )

    return g, df


def plot_shm_distribution_bar(df, pool, size_metric, **kwargs):
    '''
    Plots the SHM distribution of a pooled DataFrame using either clones,
    copies, or uniques as a size metric.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame used to plot the SHM distribution.
    pool : str
        The pool to use for plotting.
    size_metric : str
        The metric to determine each clones' size.  Must be ``clones``,
        ``copies``, or ``uniques``.

    Returns
    -------
    A tuple ``(g, df)`` where ``g`` is a handle to the plot and ``df`` is the
    underlying DataFrame.

    '''

    assert size_metric in ('clones', 'copies', 'uniques')
    df = df.copy()
    df = _add_counts(df, pool)
    df['shm'] = df['shm'].round(1)
    df = (
        df
        .groupby(['shm', pool])
        .apply(_get_shm, df, pool, size_metric).reset_index()
    )
    evaluation_bins = [0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75,
                       3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5, 5.25, 5.5,
                       5.75, 6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75, 8, 8.25,
                       8.5, 8.75, 9, 9.25, 9.5, 9.75, 10, float('inf')]
    df['shm'] = pd.cut(df['shm'], bins=evaluation_bins, include_lowest=True)
    with sns.plotting_context('poster'):
        g = sns.catplot(
            data=df,
            x='shm',
            y='size',
            hue=pool,
            kind='bar',
            errorbar=None,
            height=kwargs.pop('height', 8),
            aspect=kwargs.pop('aspect', 2),
            palette=['purple', '#4169E1', '#E1341E'],
            **kwargs
        )
        g.set(
            xlabel='SHM',
            ylabel=f'% of {size_metric}',
        )
        g.set_xticklabels(rotation=90)
    return g, df
