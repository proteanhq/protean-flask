========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/protean-flask/badge/?style=flat
    :target: https://readthedocs.org/projects/protean-flask
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/protean-flask.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/protean-flask

.. |wheel| image:: https://img.shields.io/pypi/wheel/protean-flask.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/protean-flask

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/protean-flask.svg
    :alt: Supported versions
    :target: https://pypi.org/project/protean-flask

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/protean-flask.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/protean-flask


.. end-badges

Protean Flask Extension

* Free software: BSD 3-Clause License

Installation
============

::

    pip install protean-flask

Documentation
=============

https://protean-flask.readthedocs.io/

Development
===========

::

    pyenv virtualenv -p python3.7 3.7.2 protean-flask-dev

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
