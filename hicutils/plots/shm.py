import pandas as pd
import seaborn as sns


def _get_shm(pdf, df, pool, size_metric):
    total = df[df[pool] == pdf.name[1]][size_metric].sum()
    ret = pd.Series({'size': 100 * pdf[size_metric].sum() / total})
    return ret


def plot_shm_distribution(df, pool, size_metric):
    assert size_metric in ('clones', 'copies', 'uniques')
    df = df.copy()
    df['shm'] = df['shm'].round()
    pdf = (
        df
        .groupby(['shm', pool])
        .apply(_get_shm, df, pool, size_metric).reset_index()
    )

    g = sns.relplot(
        data=pdf,
        x='shm',
        y='size',
        hue=pool,
        kind='line',
        height=8,
        aspect=1.5
    )
    g.set(
        xlabel='SHM (% of Mutated V-gene NT)',
        ylabel='% of {}'.format(size_metric),
    )
    return g, pdf
