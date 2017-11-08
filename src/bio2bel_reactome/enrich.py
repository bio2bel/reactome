# -*- coding: utf-8 -*-

""" Enrich functions for BEL graphs"""

__all__ = [
    'map_hgnc_node'
]


def map_hgnc_node(manager, identifier):
    """Maps a gene from the PyHGNC database, whether it has a HGNC, RGD, MGI, or EG identifier.

    :param pyhgnc.manager.query.QueryManager manager: A PyHGNC database manager
    :param pybel.BELGraph graph: A BEL graph
    :rtype: pyhgnc.manager.models.HGNC
    """

    raise NotImplementedError
