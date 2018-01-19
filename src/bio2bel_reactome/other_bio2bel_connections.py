# -*- coding: utf-8 -*-

"""This modules loads the dictionaries to perform mappings across bio2bel packages."""

from bio2bel_chebi.manager import Manager as ChebiManager
from bio2bel_hgnc.manager import Manager as HgncManager

"""Mapping hgnc symbols to their ids and vice versa using Bio2bel_hgnc"""
hgnc_manager = HgncManager()

hgnc_id_to_symbol = hgnc_manager.build_hgnc_id_symbol_mapping()
symbol_to_hgnc_id = hgnc_manager.build_hgnc_symbol_id_mapping()

"""Mapping interpro ids to their hgnc symbols and vice versa using Bio2bel_hgnc"""

hgnc_symbol_to_uniprot_ids = hgnc_manager.build_hgnc_symbol_uniprot_ids_mapping()
uniprot_id_to_hgnc_symbol = hgnc_manager.build_uniprot_id_hgnc_symbol_mapping()
uniprot_id_to_hgnc_id = hgnc_manager.build_uniprot_id_hgnc_id_mapping()

"""Mapping chebi ids to their names and vice versa using Bio2bel_chebi"""

chebi_manager = ChebiManager()

chebi_id_to_name = chebi_manager.build_chebi_id_name_mapping()
chebi_name_to_id = chebi_manager.build_chebi_name_id_mapping()
