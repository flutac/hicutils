Plotting
========
The ``hicutils.plotting`` module provides all plotting functions.  Each
plotting function returns both a handle to the underlying figure as well as the
``pd.DataFrame`` which was used to create the plot.

Clone Size
----------
A variety of clone size plots are provide to visualize the overall clonal
landscape of a dataset.

.. raw:: html
   :file: notebooks/plotting/clone_size.html

.. automodule:: hicutils.plots.clone_size
   :members:


Gene Usage
----------
The gene usage plots show V- or J-gene usage grouped by pool.  This can be
useful for investigating gene skewing in different populations.  Each plot can
be scaled in various ways and clustered by row, column, both, or neither.

.. raw:: html
   :file: notebooks/plotting/gene_usage.html

.. automodule:: hicutils.plots.gene_usage
   :members:


Clonal Overlap
--------------
Clone overlap can be visualized with the ``plot_strings_*`` functions.  Each
row represents a clone and each column a pool.  The frequency of a given clone
in a pool can be indicated by the intensity of the corresponding cell if
desired.  Further, the definition of a clone (defaulting to ``clone_id``) can
be modified by the ``overlapping_features`` parameter.  For example, to track
clonal CDR3 amino-acids rather than ``clone_id``, one can specify
``overlapping_features=['cdr3_aa']``.  See the API documents for more
parameters.

.. raw:: html
   :file: notebooks/plotting/overlap.html

.. automodule:: hicutils.plots.overlap
   :members:


Somatic hypermutation (SHM)
---------------------------
The somatic hypermutation (SHM) of a dataset can be plotted in a variety of
ways including as a distribution, bar/violin plots, and as a range plot.

.. raw:: html
   :file: notebooks/plotting/shm.html

.. automodule:: hicutils.plots.shm
   :members:


CDR3 analysis
-------------
A number of CDR3 analysis plots are provided including CDR3 amino-acid usage
both as a heatmap and also as logo plots.  Additionally CDR3 spectratypes can
be created to show the CDR3 length distribution and highlight the top copy
clones.

.. raw:: html
   :file: notebooks/plotting/cdr3_analysis.html

.. automodule:: hicutils.plots.cdr3_analysis
   :members:
