import pandas as pd
import seaborn as sns


def _add_counts(df, field):
    sizes = df.groupby(field).size()
    df[field] = df[field].apply(lambda f: '{} ({})'.format(f, sizes[f]))
    return df


def _get_shm(pdf, df, pool, size_metric):
    total = df[df[pool] == pdf.name[1]][size_metric].sum()
    ret = pd.Series({'size': 100 * pdf[size_metric].sum() / total})
    return ret


def plot_shm_distribution(df, pool, size_metric, **kwargs):
    assert size_metric in ('clones', 'copies', 'uniques')
    df = df.copy()
    df = _add_counts(df, pool)
    df['shm'] = df['shm'].round()
    pdf = (
        df
        .groupby(['shm', pool])
        .apply(_get_shm, df, pool, size_metric).reset_index()
    )

    with sns.plotting_context('poster'):
        g = sns.relplot(
            data=pdf,
            x='shm',
            y='size',
            hue=pool,
            kind='line',
            height=8,
            aspect=1.5,
            **kwargs
        )
        g.set(
            xlabel='SHM (% of Mutated V-gene NT)',
            ylabel='% of {}'.format(size_metric),
        )
    return g, pdf


def plot_shm_aggregate(df, pool, **kwargs):
    g = sns.catplot(
        data=df,
        x=pool,
        y='shm',
        kind=kwargs.get('kind', 'violin'),
        **kwargs
    )
    g.set(xlabel='', ylabel='SHM %')
    return g, df
