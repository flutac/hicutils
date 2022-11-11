Example 1: Filtering by functionality and copies
------------------------------------------------

This example shows how to remove non-functional clones and any clone
with less than 5 copies across all samples in the subject.

.. code:: ipython3

    import hicutils.core.io as io
    import hicutils.core.filters as filters
    
    df = io.read_directory('example_data_immunedb')
    filtered_df = (
        df
        .pipe(filters.filter_functional)
        .pipe(filters.filter_by_overall_copies, 5)
    )
    display('Total Functional, 5+ Copy Clones', filtered_df.groupby('subject').clone_id.nunique())



.. parsed-literal::

    'Total Functional, 5+ Copy Clones'



.. parsed-literal::

    subject
    HPAP015    1951
    HPAP017    2391
    Name: clone_id, dtype: int64


Example 2: Filtering clones based on presence in replicates
-----------------------------------------------------------

This example, clones will be filtered out if they occur in less than 2
replicates in the associated donor.

.. code:: ipython3

    import hicutils.core.io as io
    import hicutils.core.filters as filters
    
    df = io.read_directory('example_data_immunedb')
    pdf = filters.filter_number_of_pools(df, 'replicate_name', 2)
    display(f'There are {pdf.clone_id.nunique()} clones in any two or more replicates')



.. parsed-literal::

    'There are 487 clones in any two or more replicates'


It is also possible to limit the pools (replicates in this case) to
test. For example, this code snippet looks for clones that are in both
of the HPAP015 replicates.

.. code:: ipython3

    limit_reps = [
        'IgH_HPAP015_rep1_200p0ng', 'IgH_HPAP015_rep2_200p0ng'
    ]
    pdf = filters.filter_number_of_pools(df, 'replicate_name', 2, limit_to=limit_reps)
    display(f'There are {pdf.clone_id.nunique()} clones in both '
            f'replicates {", ".join(limit_reps)}')



.. parsed-literal::

    'There are 380 clones in both replicates IgH_HPAP015_rep1_200p0ng, IgH_HPAP015_rep2_200p0ng'



