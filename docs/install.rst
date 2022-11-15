Installation
============

Quick Install
-------------
To install run:

.. code-block:: bash

    git clone https://github.com/PennHIC/hicutils.git
    bash hicutils/install.sh


After this, ``hicutils`` should be installed and ready for use.

In the future, simply re-activate the environment with ``source
venv/bin/activate`` to use.


Running Tests (optional)
------------------------
To run the entire ``hicutils`` test suite before using the package, run:

.. code-block:: bash

    pip install pytest
    cd tests
    pytest -s -v .
