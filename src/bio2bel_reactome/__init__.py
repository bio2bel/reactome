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

from .manager import Manager

__version__ = '0.0.6'

__title__ = 'bio2bel_reactome'
__description__ = "A wrapper around Reactome RESTful API"
__url__ = 'https://github.com/bio2bel/reactome'

__author__ = 'Daniel Domingo-Fernández and Charles Tapley Hoyt'
__email__ = 'daniel.domingo.fernandez@scai.fraunhofer.de'

__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2017-2018 Daniel Domingo-Fernández and Charles Tapley Hoyt'
