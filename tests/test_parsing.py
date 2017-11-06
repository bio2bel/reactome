# -*- coding: utf-8 -*-

""" This module contains the tests related with the parsing module"""

import unittest

from bio2bel_reactome.models import Pathway
from tests.constants import DatabaseMixin


class TestParse(DatabaseMixin):
    """Tests the parsing module"""

    def test1(self):
        pathway_number = self.manager.session.query(Pathway).count()

        self.assertEquals(pathway_number, 21)


if __name__ == '__main__':
    unittest.main()
