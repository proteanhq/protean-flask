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
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/protean-flask/badge/?style=flat
    :target: https://readthedocs.org/projects/protean-flask
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/protean-flask.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/protean-flask

.. |commits-since| image:: https://img.shields.io/github/commits-since/proteanhq/protean-flask/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/proteanhq/protean-flask/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/protean-flask.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/protean-flask

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/protean-flask.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/protean-flask

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/protean-flask.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/protean-flask


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
