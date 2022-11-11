Filtering Data
==============

Data can be filtered arbitrarily using `pd.DataFrame` methods but the
``hicutils.core.filters`` module provides helper utilities for common filtering
routines.  Examples include filtering non-productive clones and excluding
clones by copy number cutoffs.

Below are some examples. See :ref:`API Documentation` for a full list of
provided filters.

.. include:: notebooks/filtering.rst

API Documentation
-----------------
.. automodule:: hicutils.core.filters
   :members:
