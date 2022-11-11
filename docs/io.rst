Loading Data
============
There are two ways to load AIRR-seq data in ``hicutils``:

#. Directly downloading and loading data from a hosted ImmuneDB instance using
   its URL and database name.

#. Using existing pooled AIRR-formatted files exported from ImmuneDB, where
   pooling metadata is embedded in the file names.

#. Using existing un-pooled AIRR-formatted files with a metadata file with one
   row per file.

.. include:: notebooks/loading_data.rst

API Documentation
-----------------
.. automodule:: hicutils.core.io
   :members:
