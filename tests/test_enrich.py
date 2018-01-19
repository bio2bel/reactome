# -*- coding: utf-8 -*-

""" This module contains the tests related with the graph enrichment"""

from bio2bel_reactome.enrich import map_hgnc_node
from bio2bel_reactome.models import Protein
from tests.constants import DatabaseMixin

from bio2bel_hgnc.manager import Manager as bio2bel_hgnc_manager

class TestParse(DatabaseMixin):
    """Tests the parsing module"""

    def help_check_rat_cd80_model(self, model):
        """Checks if the given model is CD33 (https://rgd.mcw.edu/rgdweb/report/gene/main.html?id=RGD:2314)
        :param pyhgnc.manager.models.HGNC model: The result from a search of the PyHGNC database
        """
        self.assertEqual('2314', str(model.identifier))
        self.assertEqual('Cd80', model.symbol)
        self.assertEqual('Cd80 molecule', model.name)

    def test_uniprot_rgd_mapping(self):
        """ Maps uniprot id http://www.uniprot.org/uniprot/A0A0G2K0F2 to Rat Cd80"""

        cd80_uniprot = self.manager.session.query(Protein).filter(Protein.uniprot_id == 'A0A0G2K0F2').one_or_none()

        cd80_hgnc = map_hgnc_node(manager=bio2bel_hgnc_manager, identifier=cd80_uniprot)

        self.help_check_rat_cd80_model(cd80_hgnc)
