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
        num_color=None):
    df = df[:]
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
    pdf.columns = [
        '{} ({})'.format(k, int(v))
        for k, v in (pdf / pdf).sum().iteritems()
    ]
    if len(pdf.columns) < 2:
        raise IndexError('Overlap plots must have at least two columns')

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

    pdf = pdf.head(num_color if num_color else len(pdf))
    pdf = pdf.fillna(0)
    pdf = pdf[(pdf / pdf).sum().sort_values().index]
    pdf = pdf.reindex((pdf / pdf).sort_values(list(pdf.columns)).index)

    if num_color:
        pal = LinearSegmentedColormap.from_list(
            name='vdjtools',
            colors=['#2b8cbe', '#e0f3db', '#fdbb84']
        )
    else:
        pal = sns.diverging_palette(10, 240, s=95, sep=1, as_cmap=True)
        pdf = (pdf / pdf).reindex(
            (pdf / pdf).sort_values(list(pdf.columns)).index
        ).fillna(0)

    with sns.axes_style('darkgrid'):
        g = sns.clustermap(
            data=pdf,
            cmap=pal,
            figsize=(20, .3 * (num_color or 100)),
            mask=pdf == 0,
            linewidths=1 if num_color else 0,
            row_cluster=False,
            col_cluster=False,
            yticklabels=num_color is not None,
            vmin=0 if not num_color else pdf.min().min(),
            vmax=1 if not num_color else None,
            cbar_kws={
                'label': '% of column'
            }
        )

        if not num_color:
            g.cax.set_visible(False)
            labels = np.arange(1, len(pdf) + 1, max(1, len(pdf) // 5))
            g.ax_heatmap.set_yticks(labels)
            g.ax_heatmap.set_yticklabels(labels)
        else:
            g.ax_heatmap.set_yticklabels(
                g.ax_heatmap.get_yticklabels(),
                fontsize=8
            )
        g.ax_heatmap.set_xlabel('')
        g.ax_heatmap.set_ylabel('')

    return g, ret_df
