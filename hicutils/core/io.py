import glob
import os

import pandas as pd
import matplotlib.pyplot as plt


def read_tsvs(path, features=None):
    dfs = []
    for fn in glob.glob(os.path.join(path, '*.pooled.tsv')):
        df = pd.read_csv(fn, sep='\t', dtype={'subject': str})
        if features:
            values = os.path.basename(fn).split('.')[1].split('_AND_')
            for i, feature in enumerate(values):
                df[features[i]] = feature
        df['copies_fraction'] = df.copies / df.copies.sum()
        df['copies_percent'] = 100 * df['copies_fraction']
        df['shm'] = 100 * (1 - df['avg_v_identity'])
        df['clones'] = 1
        df = df.sort_values('copies', ascending=False)

        dfs.append(df)

    return pd.concat(dfs)


def save_fig_and_data(name, df, path='./', **kwargs):
    path = os.path.join(path, name)
    df.to_csv(path + '.tsv', sep='\t', **kwargs)
    plt.savefig(path + '.pdf', bbox_inches='tight')
