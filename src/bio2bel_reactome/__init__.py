# -*- coding: utf-8 -*-

"""Bio2BEL Reactome is a package for enriching BEL networks with Reactome information by wrapping its RESTful API.

Reactome is a pathway database comprising established pathways between different species that contain genetic as well
as chemical information. This package downloads pathway information from Reactome's API and store it in template
data model relating genes and chemical to pathways. Moreover, the hierarchy of the pathways is maintained enabling
pathway comparison and exploration in the `ComPath environment <https://github.com/ComPath>`_.

Citation
--------
- Fabregat, Antonio et al. The Reactome Pathway Knowledgebase. Nucleic Acids Research 44.Database issue (2016):
  D481–D487. PMC. Web. 6 Oct. 2017.
- Croft, David et al. The Reactome Pathway Knowledgebase. Nucleic Acids Research 42.Database issue (2014): D472–D477.
  PMC. Web. 6 Oct. 2017.
"""

from .manager import Manager  # noqa:F401
