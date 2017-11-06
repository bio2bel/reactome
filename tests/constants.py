# -*- coding: utf-8 -*-
""" This module contains all test constants"""

import os
import tempfile
import unittest

from bio2bel_reactome.manager import Manager

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

chemicals_to_reactome = os.path.join(resources_path, 'ChEBI2Reactome_All_Levels.txt')
pathways = os.path.join(resources_path, 'ReactomePathways.txt')
pathway_hierarchy = os.path.join(resources_path, 'ReactomePathwaysRelation.txt')
proteins_to_reactome = os.path.join(resources_path, 'UniProt2Reactome_All_Levels.txt')


class DatabaseMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary file"""

        cls.fd, cls.path = tempfile.mkstemp()
        cls.connection = 'sqlite:///' + cls.path

        # create temporary database
        cls.manager = Manager(cls.connection)
        cls.manager.make_tables()
        # fill temporary database with test data
        cls.manager.populate(
            pathways_path=pathways,
            pathways_hierarchy_path=pathway_hierarchy,
            pathways_proteins_path=proteins_to_reactome,
            pathways_chemicals_path=chemicals_to_reactome,
        )

    @classmethod
    def tearDownClass(cls):
        """Closes the connection in the manager and deletes the temporary database"""
        cls.manager.session.close()
        os.close(cls.fd)
        os.remove(cls.path)
