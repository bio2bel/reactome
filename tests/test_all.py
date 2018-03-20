# -*- coding: utf-8 -*-

""" This module contains the tests related with the graph enrichment"""

from pybel.dsl import abundance, protein

from bio2bel_chebi.manager import Manager as ChebiManager
from bio2bel_chebi.models import Chemical
from bio2bel_reactome.constants import CHEBI
from bio2bel_reactome.models import Chemical
from tests.constants import DatabaseMixin


class TestGlobal(DatabaseMixin):
    """Tests the parsing module"""

    def test_get_all_human_pathways(self):
        """Checks get all human pathways"""

        human_pathways = self.manager.get_pathways_by_species('Homo sapiens')
        xenopus_pathways = self.manager.get_pathways_by_species('Xenopus tropicalis')
        should_be_none = self.manager.get_pathways_by_species('invalid species')

        self.assertEqual(4, len(human_pathways))
        self.assertEqual(1, len(xenopus_pathways))
        self.assertEqual(None, should_be_none)

    def test_protein_exporting(self):
        """Checks export methods of protein table"""

        cd86_uniprot = self.manager.get_protein_by_uniprot_id('A0A0G2JXF7')

        self.assertIsNotNone(cd86_uniprot)

        self.assertEqual(
            cd86_uniprot.as_pybel_dict(),
            protein(namespace='UNIPROT', name='A0A0G2JXF7', identifier='A0A0G2JXF7')
        )

    def test_chebi_exporting(self):
        """Checks export methods of chemical table"""

        adp_chebi = self.manager.get_chemical_by_chebi_id('16761')

        self.assertEqual(
            adp_chebi.as_pybel_dict(),
            abundance(namespace=CHEBI, name='ADP', identifier='16761')
        )

    def test_pathway_count(self):
        pathway_number = self.manager.count_pathways()
        self.assertEqual(21, pathway_number)

    def test_get_all_pathways(self):
        all_pathways = self.manager.get_all_pathways()
        self.assertEqual(21, len(all_pathways))

    def test_chemical_count(self):
        chemical_number = self.manager.count_chemicals()
        self.assertEqual(4, chemical_number)

    def test_protein_count(self):
        protein_number = self.manager.count_proteins()
        self.assertEqual(10, protein_number)

    def test_species_count(self):
        species_number = self.manager.count_species()
        self.assertEqual(18, species_number)

    def test_protein_1(self):
        """Test protein relationships"""

        protein = self.manager.get_protein_by_uniprot_id('P08237')
        self.assertIsNotNone(protein, 'Protein not found')
        self.assertEqual(3, len(protein.pathways))

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

    def test_hierarchy_1(self):
        granfather = self.manager.get_pathway_by_id('R-HSA-388841')
        self.assertIsNotNone(granfather)

        childrens = {
            children.reactome_id
            for children in granfather.children
        }

        self.assertEqual(
            {'R-HSA-389356',
             'R-ATH-389357',
             'R-CEL-389357',
             'R-CFA-389357',
             'R-DRE-389357',
             'R-DDI-389357',
             'R-DME-389357',
             },
            childrens
        )

        parent = self.manager.get_pathway_by_id('R-HSA-389356')
        self.assertIsNotNone(parent)
        self.assertEqual(
            {'CD28 dependent PI3K/Akt signaling', 'CD28 dependent Vav1 pathway'},
            {children.name
             for children in parent.children
             }
        )

    def test_hierarchy_2(self):
        """Tests get pathway by name method"""
        child = self.manager.get_pathway_by_name('CD28 dependent PI3K/Akt signaling', 'Homo sapiens')
        self.assertIsNotNone(child, msg='Pathway not found')
        self.assertEqual('R-HSA-389356', child.parent.reactome_id)

    def test_hierarchy_3(self):
        """Tests get_pathway_parent_by_id by name method"""
        parent = self.manager.get_pathway_parent_by_id('R-HSA-389359')
        self.assertIsNotNone(parent, msg='Pathway not found')
        self.assertEqual('CD28 co-stimulation', parent.name)

    def test_hierarchy_4(self):
        """Tests get top hierarchy method by finding the top member of the hierarchy"""
        granfather = self.manager.get_top_hiearchy_parent_by_id('R-HSA-389359')
        self.assertIsNotNone(granfather, msg='Pathway not found')
        self.assertEqual('R-HSA-388841', granfather.reactome_id)

    def test_top_hierarchy(self):
        """Tests get all top hierarchy members"""
        main_pathways = self.manager.get_all_top_hierarchy_pathways()
        # Only 12 pathways are in the highest hierarchy level
        self.assertEqual(len(main_pathways), 12)

    def test_get_pathway_by_name(self):
        """Tests get get pathway name 2"""

        bos_taurus_cd29_pathway = self.manager.get_pathway_by_name('CD28 dependent PI3K/Akt signaling', 'Bos taurus')
        self.assertIsNotNone(bos_taurus_cd29_pathway, msg='Pathway not found')

        self.assertEqual('R-BTA-389357', bos_taurus_cd29_pathway.reactome_id)

        sativa_cd29_pathway = self.manager.get_pathway_by_name('CD28 dependent PI3K/Akt signaling', 'Oryza sativa')
        self.assertIsNotNone(sativa_cd29_pathway, msg='Pathway not found')

        self.assertEqual('R-OSA-389357', sativa_cd29_pathway.reactome_id)

        self.assertEqual(sativa_cd29_pathway.name, bos_taurus_cd29_pathway.name)
        self.assertNotEqual(sativa_cd29_pathway.species.name, bos_taurus_cd29_pathway.species.name)

    def test_chebi_parser(self):
        chebi_manager = ChebiManager(connection=self.connection)

        all_chemicals = chebi_manager.session.query(Chemical).all()
        self.assertEqual(4, len(all_chemicals))

    def test_gene_query_1(self):
        """Single protein query. This protein is associated with 3 pathways"""
        enriched_pathways = self.manager.query_gene_set(['HGNC_SYMBOL_3'])
        self.assertIsNotNone(enriched_pathways, msg='Enriching function is not working')

        self.assertEqual(
            {
                "pathway_id": "R-HSA-389359",
                "pathway_name": "CD28 dependent Vav1 pathway",
                "mapped_proteins": 1,
                "pathway_size": 7,
                "pathway_gene_set": {
                    'HGNC_SYMBOL_1',
                    'HGNC_SYMBOL_2',
                    'HGNC_SYMBOL_3',
                    'HGNC_SYMBOL_4',
                    'HGNC_SYMBOL_5',
                    'HGNC_SYMBOL_6',
                    'PFKM'
                }
            },
            enriched_pathways["R-HSA-389359"]
        )

        self.assertEqual(
            {
                "pathway_id": "R-RNO-389357",
                "pathway_name": "CD28 dependent PI3K/Akt signaling",
                "mapped_proteins": 1,
                "pathway_size": 3,
                "pathway_gene_set": {'HGNC_SYMBOL_3', 'PFKM', 'HGNC_SYMBOL_2'}
            },
            enriched_pathways["R-RNO-389357"]
        )

        self.assertEqual(
            {
                "pathway_id": "R-HSA-389356",
                "pathway_name": "CD28 co-stimulation",
                "mapped_proteins": 1,
                "pathway_size": 3,
                "pathway_gene_set": {'PFKM', 'HGNC_SYMBOL_3', 'HGNC_SYMBOL_1'}
            },
            enriched_pathways["R-HSA-389356"]
        )

    def test_gene_query_2(self):
        """Multiple protein query"""
        enriched_pathways = self.manager.query_gene_set(['HGNC_SYMBOL_3', 'HGNC_SYMBOL_5'])
        self.assertIsNotNone(enriched_pathways, msg='Enriching function is not working')

        self.assertEqual(
            {
                "pathway_id": "R-RNO-389357",
                "pathway_name": "CD28 dependent PI3K/Akt signaling",
                "mapped_proteins": 1,
                "pathway_size": 3,
                "pathway_gene_set": {'HGNC_SYMBOL_3', 'PFKM', 'HGNC_SYMBOL_2'}
            },
            enriched_pathways["R-RNO-389357"]
        )

        self.assertEqual(
            {
                "pathway_id": "R-HSA-389356",
                "pathway_name": "CD28 co-stimulation",
                "mapped_proteins": 1,
                "pathway_size": 3,
                "pathway_gene_set": {'PFKM', 'HGNC_SYMBOL_3', 'HGNC_SYMBOL_1'}
            },
            enriched_pathways["R-HSA-389356"]
        )

        self.assertEqual(
            {
                "pathway_id": "R-HSA-389359",
                "pathway_name": "CD28 dependent Vav1 pathway",
                "mapped_proteins": 2,
                "pathway_size": 7,
                "pathway_gene_set": {
                    'HGNC_SYMBOL_1',
                    'HGNC_SYMBOL_2',
                    'HGNC_SYMBOL_3',
                    'HGNC_SYMBOL_4',
                    'HGNC_SYMBOL_5',
                    'HGNC_SYMBOL_6',
                    'PFKM'
                }
            },
            enriched_pathways["R-HSA-389359"]
        )

    def test_gene_query_3(self):
        """Multiple protein query"""
        enriched_pathways = self.manager.query_gene_set(['HGNC_SYMBOL_3', 'HGNC_SYMBOL_1'])
        self.assertIsNotNone(enriched_pathways, msg='Enriching function is not working')

        self.assertEqual(
            {
                "pathway_id": "R-RNO-389357",
                "pathway_name": "CD28 dependent PI3K/Akt signaling",
                "mapped_proteins": 1,
                "pathway_size": 3,
                "pathway_gene_set": {'HGNC_SYMBOL_3', 'PFKM', 'HGNC_SYMBOL_2'}
            },
            enriched_pathways["R-RNO-389357"]
        )

        self.assertEqual(
            {
                "pathway_id": "R-HSA-389356",
                "pathway_name": "CD28 co-stimulation",
                "mapped_proteins": 2,
                "pathway_size": 3,
                "pathway_gene_set": {'PFKM', 'HGNC_SYMBOL_3', 'HGNC_SYMBOL_1'}
            },
            enriched_pathways["R-HSA-389356"]
        )

        self.assertEqual(
            {
                "pathway_id": "R-HSA-389359",
                "pathway_name": "CD28 dependent Vav1 pathway",
                "mapped_proteins": 2,
                "pathway_size": 7,
                "pathway_gene_set": {
                    'HGNC_SYMBOL_1',
                    'HGNC_SYMBOL_2',
                    'HGNC_SYMBOL_3',
                    'HGNC_SYMBOL_4',
                    'HGNC_SYMBOL_5',
                    'HGNC_SYMBOL_6',
                    'PFKM'
                }
            },
            enriched_pathways["R-HSA-389359"]
        )
