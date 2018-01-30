# -*- coding: utf-8 -*-

""" This module contains all test constants"""

import os
import tempfile
import unittest

from bio2bel_chebi.manager import Manager as ChebiManager
from bio2bel_hgnc.manager import Manager as HgncManager

from bio2bel_reactome.manager import Manager

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

pathways = os.path.join(resources_path, 'ReactomePathways.txt')
pathway_hierarchy = os.path.join(resources_path, 'ReactomePathwaysRelation.txt')
proteins_to_reactome = os.path.join(resources_path, 'UniProt2Reactome_All_Levels.txt')
chemicals_to_reactome = os.path.join(resources_path, 'ChEBI2Reactome_All_Levels.txt')

hgnc_test_path = os.path.join(resources_path, 'hgnc_test.json')
hcop_test_path = os.path.join(resources_path, 'hcop_test.txt')

chebi_test_path = os.path.join(resources_path, 'chebi_test.tsv.gz')


class DatabaseMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary file"""

        """Create temporary file"""

        cls.fd, cls.path = tempfile.mkstemp()
        cls.connection = 'sqlite:///' + cls.path

        """HGNC Manager"""

        hgnc_manager = HgncManager(connection=cls.connection)

        hgnc_manager.create_all()

        hgnc_manager.populate(
            hgnc_file_path=hgnc_test_path,
            hcop_file_path=hcop_test_path,
        )

        """CHEBI Manager"""

        chebi_manager = ChebiManager(connection=cls.connection)

        chebi_manager._populate_compounds(
            url=chebi_test_path
        )

        # create temporary database
        cls.manager = Manager(cls.connection)

        """Reactome Manager"""
        # fill temporary database with test data
        cls.manager.populate(
            hgnc_manager=hgnc_manager,
            chebi_manager=chebi_manager,
            pathways_path=pathways,
            pathways_hierarchy_path=pathway_hierarchy,
            pathways_proteins_path=proteins_to_reactome,
            pathways_chemicals_path=chemicals_to_reactome,
            only_human=False
        )

        hgnc_manager.session.close()
        chebi_manager.session.close()


    @classmethod
    def tearDownClass(cls):
        """Closes the connection in the manager and deletes the temporary database"""
        cls.manager.drop_all()
        cls.manager.session.close()

        os.close(cls.fd)
        os.remove(cls.path)
