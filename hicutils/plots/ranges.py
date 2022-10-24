from collections import Counter
import re

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def _range_for_pool(df, portions, total_clones, intervals):
    pool = df.name
    total_clones[pool] += len(df)

    for start, end in zip(intervals[:-1], intervals[1:]):
        portions.append({
            'pool': pool,
            'start': start,
            'end': end,
            'copies': df[start:end].copies.sum()
        })
    portions.append({
        'pool': pool,
        'start': end,
        'end': '+',
        'copies': df[end:].copies.sum()
    })
    return portions


def _get_d(df, d):
    return (
        df.sort_values('copies', ascending=False)
        .head(d)
        .copies.sum()
    ) / df.copies.sum()


def _label(r):
    if r['end'] != '+':
        return '{}-{}'.format(r['start'] + 1, r['end'])
    return '{}+'.format(r['start'] + 1)


def plot_ranges(
        df,
        pool,
        intervals=(0, 10, 100, 1000),
        ):
    portions = []
    total_clones = Counter()

    df.groupby(pool).apply(_range_for_pool, portions, total_clones, intervals)

    portions = pd.DataFrame(portions)
    portions['pool'] = portions['pool'].apply(
        lambda p: '{} ({})'.format(p, total_clones[p])
    )
    portions['range'] = portions.apply(_label, axis=1)
    pdf = (
        portions
        .pivot_table(index='pool', columns='range', values='copies',
                     aggfunc=np.sum)
    )
    pdf = pdf.div(-pdf.sum(axis=1), axis=0)

    order = pd.Series(
        int(re.search(r'\d+', c).group(0)) for c in pdf.columns
    ).argsort()

    pdf = (
        pdf[pdf.columns[order]]
        .reindex(
            pdf[pdf.columns[:-1]].sum(axis=1).sort_values().index
        )
    )

    d20s = list(
        df
        .groupby(pool).apply(_get_d, 20)
        .sort_values(ascending=False)
        .index
    )
    pdf['order'] = [
        d20s.index(label.rsplit(' (')[0]) for label in pdf.index
    ]
    pdf = pdf.sort_values('order').drop('order', axis=1)

    colors = [
        sns.color_palette()[3],  # red
        sns.color_palette()[0],  # blue
        sns.color_palette()[2],  # green
        (0.86, 0.86, 0.86)  # gray
    ]

    ax = pdf.plot.bar(stacked=True, figsize=(12, 12), color=colors)
    ax.set_yticklabels([round(abs(tick), 2) for tick in ax.get_yticks()])
    ax.set_xlabel('')
    ax.set_ylabel('Fraction of Copies')
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))

    return ax, pdf
