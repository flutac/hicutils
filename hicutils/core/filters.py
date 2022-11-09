def filter_by_overall_copies(df, copies):
    valid_clones = df.groupby('clone_id').copies.sum() >= copies
    valid_clones = valid_clones[valid_clones == True].index  # noqa: E712
    return df[df.clone_id.isin(valid_clones)]


def filter_functional(df, functional='T'):
    return df[df.functional == functional]
