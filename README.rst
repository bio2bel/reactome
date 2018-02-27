Bio2BEL Reactome |build| |coverage| |docs|
==========================================
This package allows the enrichment of BEL networks with Reactome information by wrapping its RESTful API.
Furthermore, it is integrated in the `ComPath environment <https://github.com/ComPath>`_ for pathway database comparison.

Installation
------------
This code can be installed with :code:`pip3 install git+https://github.com/bio2bel/reactome.git`

Note that the two following resources should be installed and loaded in order to fully populate the tables of the database:

- `Bio2BEL CHEBI <https://github.com/bio2bel/chebi>`_
- `Bio2BEL HGNC <https://github.com/bio2bel/hgnc>`_

These two resources will be installed together with this package and can be quickly loaded by running the following commands in your terminal:

- :code:`python3 -m bio2bel_hgnc populate`
- :code:`python3 -m bio2bel_chebi populate`

Functionalities and Commands
----------------------------
Following, the main functionalities and commands to work with this package:

- Populate local database with Reactome info :code:`python3 -m bio2bel_reactome populate`
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

.. |docs| image:: http://readthedocs.org/projects/bio2bel-reactome/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/reactome/en/latest/?badge=latest
    :alt: Documentation Status
