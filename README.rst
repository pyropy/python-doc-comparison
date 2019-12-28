========
Overview
========

Python Package for simple document comparsion.

* Free software: MIT license

Installation
============

::

    pip install comparedocs

You can also install the in-development version with::

    pip install git+ssh://git@https://github.com/pyropy/python-doc-comparsion/pyropy/python-doc-comparison.git@master

Documentation
=============


https://python-doc-comparison.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
