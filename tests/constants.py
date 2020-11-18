# -*- coding: utf-8 -*-

"""Test constants for Bio2BEL Reactome."""

import os

import bio2bel_reactome
from bio2bel.testing import TemporaryConnectionMixin

dir_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(dir_path, 'resources')

pathways = os.path.join(resources_path, 'ReactomePathways.txt')
pathway_hierarchy = os.path.join(resources_path, 'ReactomePathwaysRelation.txt')
proteins_to_reactome = os.path.join(resources_path, 'UniProt2Reactome_All_Levels.txt')
chemicals_to_reactome = os.path.join(resources_path, 'ChEBI2Reactome_All_Levels.txt')


class DatabaseMixin(TemporaryConnectionMixin):
    """Load the database before each test."""

    reactome_manager: bio2bel_reactome.Manager

    @classmethod
    def setUpClass(cls):
        """Create a temporary file and populate the database."""
        super().setUpClass()

        # Reactome manager
        cls.reactome_manager = bio2bel_reactome.Manager(connection=cls.connection)
        cls.reactome_manager.populate(
            pathways_path=pathways,
            pathways_hierarchy_path=pathway_hierarchy,
            pathways_proteins_path=proteins_to_reactome,
            pathways_chemicals_path=chemicals_to_reactome,
        )

    @classmethod
    def tearDownClass(cls):
        """Close the connection in the manager and deletes the temporary database."""
        cls.reactome_manager.session.close()
        super().tearDownClass()
