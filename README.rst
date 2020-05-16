Bio2BEL Reactome |build| |coverage| |documentation| |zenodo|
============================================================
This package handles the nomenclature and membership of chemicals/proteins in Reactome pathways.
It is integrated with the `ComPath environment <https://github.com/ComPath>`_ for pathway database
comparison.

If you find this package useful, please consider citing [domingofernandez2018]_:

.. [domingofernandez2018] Domingo-Fernandez, D., *et al* (2018). `ComPath: an ecosystem for exploring, analyzing,
   and curating mappings across pathway databases <https://doi.org/10.1038/s41540-018-0078-8>`_.
   *Npj Systems Biology and Applications*, **5**(1), 3.

**Warning** This package creates ``partOf`` relationships in BEL, but does not convert Reactome
to BEL. That functionality is implemented in the `PathMe project <https://github.com/pathwaymerger/pathme>`_.

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_reactome`` can be installed easily from `PyPI <https://pypi.python.org/pypi/bio2bel_reactome>`_ with the
following code in your favorite terminal:

.. code-block:: sh

    $ pip install bio2bel_reactome

or from the latest code on `GitHub <https://github.com/bio2bel/reactome>`_ with:

.. code-block:: sh

    $ git clone https://github.com/bio2bel/reactome.git
    $ cd reactome
    $ pip install -e .

Setup
-----
Reactome can be downloaded and populated from either the Python REPL or the automatically installed command line
utility.

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
- Run an admin site for simple querying and exploration :code:`bio2bel_reactome web` (http://localhost:5000/admin/)
- Export gene sets for programmatic use :code:`bio2bel_reactome export`

Citation
--------
- Fabregat, Antonio et al. “The Reactome Pathway Knowledgebase.” Nucleic Acids Research 44.Database issue (2016):
  D481–D487. PMC. Web. 6 Oct. 2017.
- Croft, David et al. “The Reactome Pathway Knowledgebase.” Nucleic Acids Research 42.Database issue (2014): D472–D477.
  PMC. Web. 6 Oct. 2017.

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
