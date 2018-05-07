Bio2BEL Reactome |build| |coverage| |documentation| |zenodo|
============================================================
This package allows the enrichment of BEL networks with Reactome information by wrapping its RESTful API.
Furthermore, it is integrated in the `ComPath environment <https://github.com/ComPath>`_ for pathway database comparison.

Installation
------------
This code can be installed with :code:`pip3 install git+https://github.com/bio2bel/reactome.git`


These two resources will be installed together with this package and can be quickly loaded by running the following commands in your terminal:

- :code:`python3 -m bio2bel_hgnc populate`
- :code:`python3 -m bio2bel_chebi populate`

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_reactome`` can be installed easily from `PyPI <https://pypi.python.org/pypi/bio2bel_reactome>`_ with the
following code in your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install bio2bel_reactome

or from the latest code on `GitHub <https://github.com/bio2bel/reactome>`_ with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/bio2bel/reactome.git@master

Setup
-----
Reactome can be downloaded and populated from either the Python REPL or the automatically installed command line
utility.

The following resources will be automatically installed and loaded in order to fully populate the tables of the
database:

- `Bio2BEL CHEBI <https://github.com/bio2bel/chebi>`_
- `Bio2BEL HGNC <https://github.com/bio2bel/hgnc>`_

Python REPL
~~~~~~~~~~~
.. code-block:: python

    >>> import bio2bel_reactome
    >>> reactome_manager = bio2bel_reactome.Manager()
    >>> reactome_manager.populate()

Command Line Utility
~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    bio2bel_reactome populate

Other Command Line Utilities
----------------------------
- Run an admin site for simple querying and exploration :code:`python3 -m bio2bel_reactome web` (http://localhost:5000/admin/)
- Export gene sets for programmatic use :code:`python3 -m bio2bel_reactome export`

Citation
--------
- Fabregat, Antonio et al. “The Reactome Pathway Knowledgebase.” Nucleic Acids Research 44.Database issue (2016): D481–D487. PMC. Web. 6 Oct. 2017.
- Croft, David et al. “The Reactome Pathway Knowledgebase.” Nucleic Acids Research 42.Database issue (2014): D472–D477. PMC. Web. 6 Oct. 2017.

.. |build| image:: https://travis-ci.org/bio2bel/reactome.svg?branch=master
    :target: https://travis-ci.org/bio2bel/reactome
    :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/bio2bel/reactome/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/reactome?branch=master
    :alt: Coverage Status

.. |documentation| image:: http://readthedocs.org/projects/bio2bel-interpro/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/reactome/en/latest/?badge=latest
    :alt: Documentation Status

.. |climate| image:: https://codeclimate.com/github/bio2bel/reactome/badges/gpa.svg
    :target: https://codeclimate.com/github/bio2bel/reactome
    :alt: Code Climate

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/bio2bel_reactome.svg
    :alt: Stable Supported Python Versions

.. |pypi_version| image:: https://img.shields.io/pypi/v/bio2bel_reactome.svg
    :alt: Current version on PyPI

.. |pypi_license| image:: https://img.shields.io/pypi/l/bio2bel_reactome.svg
    :alt: MIT License

.. |zenodo| image:: https://zenodo.org/badge/103138323.svg
    :target: https://zenodo.org/badge/latestdoi/103138323
