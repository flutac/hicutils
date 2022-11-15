``hicutils``: HIC utilities for AIRR-seq data
=============================================
|circleci| |codecov| |docs|

.. |circleci| image:: https://dl.circleci.com/status-badge/img/gh/PennHIC/hicutils/tree/main.svg?style=shield
   :target: https://dl.circleci.com/status-badge/redirect/gh/PennHIC/hicutils/tree/main
.. |docs| image:: https://readthedocs.org/projects/hicutils/badge/?version=latest
    :target: https://hicutils.readthedocs.io/en/latest/?badge=latest
.. |codecov| image:: https://codecov.io/github/PennHIC/hicutils/branch/main/graph/badge.svg?token=8WXJNSEXEV
    :target: https://codecov.io/github/PennHIC/hicutils

The ``hicutils`` package is a suite of tools for loading, filtering,
manipulating, and plotting `AIRR-seq
<https://docs.airr-community.org/en/stable/>`_ data in `standard AIRR format
<https://docs.airr-community.org/en/stable/datarep/rearrangements.html>`_.  It
is specifically meant to interact with `ImmuneDB <http://immunedb.com>`_ and
provide utilities commonly used in the Human Immunology Core at the University
of Pennsylvania, but may be used with AIRR-seq output from other tools.

Getting Started
---------------
To get started, follow the :doc:`installation instructions <install>` and then
continue to the :doc:`io`.

.. toctree::
   :maxdepth: 3
   :hidden:

   install
   io
   filters
   metadata
   plotting
