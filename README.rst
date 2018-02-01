Bio2BEL Reactome |build| |coverage| |docs|
==========================================
This package converts Reactome to BEL. So far, exporting the pathway namespace has been implemented.

Installation
------------
This code can be installed with :code:`pip3 install git+https://github.com/bio2bel/reactome.git`

Note that the two following resources should be installed and loaded in order to fully populate the tables of the database:

- `Bio2BEL CHEBI <https://github.com/bio2bel/chebi>`_
- `Bio2BEL HGNC <https://github.com/bio2bel/hgnc>`_

These two resources will be installed together with this package and can be quickly loaded by running the following commands:

1. :code:`python3 -m bio2bel_hgnc populate`
2. :code:`python3 -m bio2bel_chebi populate`


Creating a Local Copy of the Namespace
--------------------------------------
A BEL namespace can be generated with :code:`python3 -m bio2bel_reactome write -o ~/Downloads/reactome.belns`

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
