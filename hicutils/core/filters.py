import numpy as np


def filter_by_overall_copies(df, copies, field='clone_id'):
    '''
    Removes clones identified by ``field`` (default ``clone_id``) from a
    DataFrame with *less than* ``copies`` total copies across all pools.

    Changing ``field`` changes the definition of a clone.  For example, setting
    ``field`` to ``'cdr3_aa'`` will defined clones by their CDR3 AA sequence.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter.
    copies : int
        The minimum copy number of each clone required to be included in the
        resulting DataFrame.

    Returns
    -------
    DataFrame filtered by copies.

    Examples
    --------
    The following removes all clones with less than 5 copies from ``df``:


    .. code-block:: python

        >>> df.copies.min()
        1
        >>> df = filter_by_overall_copies(df, 5)
        >>> df.copies.min()
        4


    '''
    valid_clones = df.groupby(field).copies.sum() >= copies
    valid_clones = valid_clones[valid_clones == True].index  # noqa: E712
    return df[df.clone_id.isin(valid_clones)]


def filter_functional(df, functional=True):
    '''
    Removes clones on functionality, by default removing non-functional clones.
    Setting ``functionality`` to ``False`` removes functional clones.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter.
    functional : bool
        The functionality of the clones to include.  Set to ``True`` (the
        default) to include functional clones only.  Set to ``False`` to only
        include non-functional clones.

    Returns
    -------
    DataFrame filtered by functionality.

    '''

    return df[df.functional == ('T' if functional else 'F')]


def _overlap_pivot(df, pool):
    return df.pivot_table(
        index='clone_id',
        columns=pool,
        values='copies',
        aggfunc=np.sum
    )


def filter_number_of_pools(df, pool, n, func='greater_equal', limit_to=None):
    '''
    Filters clones based on the number of pools in which it occurs.

    df : str
        The DataFrame to filter.
    pool : str
        The pool on which to filter.
    n : str
        The number of distinct pools a clone must be in to be included in the
        resulting DataFrame.
    func : function
        The comparison function to use between `n` and the number of
        occurrences of each clone.  The default is `greater_equal` meaning a
        clone must occur in ≥ `n` pools to be included.  Any `numpy` function
        may be used such as `equal` or `less_equal`.
    limit_to : list(str), str, None
        If specified, overlap will be limited to the specified pools.  This is
        useful to filter clones based on their overlap in a subset of pools.

    Returns
    -------
    DataFrame filtered by number of pools.

    '''

    func = getattr(np, func)
    counts = _overlap_pivot(df, pool)
    if limit_to:
        counts = counts[limit_to]
    counts = (counts / counts).sum(axis=1)
    counts = set(counts[func(counts, n)].index)
    return df[df.clone_id.isin(counts)]
