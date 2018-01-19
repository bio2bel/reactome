# -*- coding: utf-8 -*-

""" This module contains the tests related with the parsing module"""

import unittest

from bio2bel_reactome.models import Pathway, Species, Chemical, Protein
from tests.constants import DatabaseMixin


class TestParse(DatabaseMixin):
    """Tests the parsing module"""

    def test_pathway_count(self):
        pathway_number = self.manager.session.query(Pathway).count()
        self.assertEqual(21, pathway_number)

    def test_chemical_count(self):
        chemical_number = self.manager.session.query(Chemical).count()
        self.assertEqual(4, chemical_number)

    def test_protein_count(self):
        protein_number = self.manager.session.query(Protein).count()
        self.assertEqual(3, protein_number)

    def test_species_count(self):
        species_number = self.manager.session.query(Species).count()
        self.assertEqual(18, species_number)

    def test_empty_pathway_chemicals(self):
        pathway = self.manager.get_pathway_by_id('R-DME-389357')
        self.assertIsNotNone(pathway)
        self.assertEqual(0, len(pathway.chemicals))

    def test_empty_pathway_proteins(self):
        pathway = self.manager.get_pathway_by_id('R-DME-389357')
        self.assertIsNotNone(pathway)
        self.assertEqual(0, len(pathway.proteins))

    def test_drugs(self):
        pathway = self.manager.get_pathway_by_id('R-HSA-389357')
        self.assertIsNotNone(pathway)
        self.assertEqual(4, len(pathway.chemicals))
        self.assertEqual(
            {'15422', '16761', '16618', '18348'}, {
                chemical.chebi_id
                for chemical in pathway.chemicals
            }
        )

    def test_drugs_to_pathways(self):
        chemical = self.manager.session.query(Chemical).filter(Chemical.chebi_id == '16761').one_or_none()
        self.assertIsNotNone(chemical)
        self.assertEqual(1, len(chemical.pathways))

    def test_hierarchy(self):
        granfather = self.manager.get_pathway_by_id('R-HSA-388841')
        self.assertIsNotNone(granfather)
        self.assertEqual('R-HSA-389356', granfather.children[0].reactome_id)

        parent = self.manager.get_pathway_by_id('R-HSA-389356')
        self.assertIsNotNone(parent)
        self.assertEqual(
            {'CD28 dependent PI3K/Akt signaling', 'CD28 dependent Vav1 pathway'},
            {children.name
             for children in parent.children
             }
        )
