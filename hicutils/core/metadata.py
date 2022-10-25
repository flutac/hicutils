import numpy as np


def make_metadata_table(df, pool):
    pdf = df.groupby(pool).agg({
        'instances': np.sum,
        'copies': np.sum,
        'cdr3_num_nts': np.mean,
        'avg_v_identity': np.mean,
    }).rename({
        'instances': 'uniques'
    }, axis=1)
    pdf['in_frame'] = df.groupby(pool).apply(
        lambda d: len(d[d.functional == 'T']) / len(d)
    )
    pdf['clones'] = df.groupby(pool).clone_id.nunique()
    return pdf
