# -*- coding: utf-8 -*-

"""This modules loads the dictionaries to perform mappings across bio2bel packages."""

from bio2bel_hgnc.manager import Manager as bio2bel_hgnc_manager


"""Mapping hgnc symbols to their ids and vice versa using Bio2bel_hgnc"""
manager = bio2bel_hgnc_manager()

hgnc_id_to_symbol = manager.build_hgnc_id_symbol_mapping()
symbol_to_hgnc_id = manager.build_hgnc_symbol_id_mapping()


"""Mapping interpro ids to their hgnc symbols and vice versa using Bio2bel_hgnc"""
