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
    ret_df = pdf[:]

    pdf = pdf.head(limit or len(pdf))
    pdf = pdf.fillna(0)
    if order:
        pdf = pdf[order]
    else:
        pdf = pdf[(pdf / pdf).sum().sort_values().index]
    pdf = pdf.reindex((pdf / pdf).sort_values(list(pdf.columns)).index)

    pdf.columns = ['{} ({:.0f})'.format(*c) for c in col_clone_counts.items()]

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
