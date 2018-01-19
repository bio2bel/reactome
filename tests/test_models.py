# -*- coding: utf-8 -*-

""" This module contains the tests related to models"""

from pybel.dsl import protein, abundance

from bio2bel_reactome.constants import HGNC, CHEBI
from bio2bel_reactome.models import Protein, Chemical
from tests.constants import DatabaseMixin


class TestModels(DatabaseMixin):
    """Tests the models module"""

    def test_protein_exporting(self):
        """Checks export methods of protein table"""

        cd86_uniprot = self.manager.get_protein_by_uniprot_id('A0A0G2JXF7')

        self.assertEqual(
            cd86_uniprot.as_pybel_dict(),
            protein(namespace=HGNC, name='CD86')
        )

    def test_chebi_exporting(self):
        """Checks export methods of chemical table"""

        adp_chebi = self.manager.get_chemical_by_chebi_id('16761')

        self.assertEqual(
            adp_chebi.as_pybel_dict(),
            abundance(namespace=CHEBI, name='ADP')
        )