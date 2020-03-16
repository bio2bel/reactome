# -*- coding: utf-8 -*-

"""Reactome database model."""

from __future__ import annotations

from typing import List

from bio2bel.manager.compath import CompathPathwayMixin, CompathProteinMixin
from bio2bel.manager.models import SpeciesMixin
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

import pybel.dsl
from .constants import CHEBI, HGNC, REACTOME, UNIPROT

Base = declarative_base()

TABLE_PREFIX = 'reactome'
PATHWAY_TABLE_NAME = '{}_pathway'.format(TABLE_PREFIX)
PATHWAY_TABLE_HIERARCHY = '{}_pathway_hierarchy'.format(TABLE_PREFIX)
SPECIES_TABLE_NAME = '{}_species'.format(TABLE_PREFIX)
PROTEIN_TABLE_NAME = '{}_protein'.format(TABLE_PREFIX)
CHEMICAL_TABLE_NAME = '{}_chemical'.format(TABLE_PREFIX)
PROTEIN_PATHWAY_TABLE = '{}_protein_pathway'.format(TABLE_PREFIX)
CHEMICAL_PATHWAY_TABLE = '{}_chemical_pathway'.format(TABLE_PREFIX)
SPECIES_PATHWAY_TABLE = '{}_species_pathway'.format(TABLE_PREFIX)

protein_pathway = Table(
    PROTEIN_PATHWAY_TABLE,
    Base.metadata,
    Column('protein_id', Integer, ForeignKey('{}.id'.format(PROTEIN_TABLE_NAME))),
    Column('pathway_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)))
)

chemical_pathway = Table(
    CHEMICAL_PATHWAY_TABLE,
    Base.metadata,
    Column('chemical_id', Integer, ForeignKey('{}.id'.format(CHEMICAL_TABLE_NAME)), primary_key=True),
    Column('pathway_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)), primary_key=True)
)


class Species(Base, SpeciesMixin):
    """Species Table."""

    __tablename__ = SPECIES_TABLE_NAME


class Protein(Base, CompathProteinMixin):
    """Protein Table."""

    __tablename__ = PROTEIN_TABLE_NAME
    id = Column(Integer, primary_key=True)

    uniprot_id = Column(String(64), unique=True, nullable=False, index=True)
    uniprot_accession = Column(String(64), unique=True, nullable=False, index=True)

    # Only for Human Genes
    hgnc_symbol = Column(String(64), nullable=True)
    hgnc_id = Column(String(64), nullable=True)

    def __repr__(self) -> str:
        return self.uniprot_id

    def to_pybel(self) -> pybel.dsl.Protein:
        """Function to serialize to PyBEL node data dictionary."""
        if self.hgnc_symbol and self.hgnc_id:
            return pybel.dsl.Protein(
                namespace=HGNC,
                identifier=self.hgnc_id,
                name=self.hgnc_symbol,
            )

        else:
            return pybel.dsl.Protein(
                namespace=UNIPROT,
                identifier=self.uniprot_id,
                name=self.uniprot_id,
            )


class Chemical(Base):
    """Chemical Table."""

    __tablename__ = CHEMICAL_TABLE_NAME
    id = Column(Integer, primary_key=True)

    chebi_id = Column(String(64), unique=True, nullable=False)
    name = Column(String(4096))

    pathways: List[Pathway]

    def __repr__(self):
        return self.chebi_id

    def to_pybel(self) -> pybel.dsl.Abundance:
        """Function to serialize to PyBEL node data dictionary."""
        return pybel.dsl.Abundance(
            namespace=CHEBI,
            identifier=self.chebi_id,
            name=self.name,
        )


class Pathway(Base, CompathPathwayMixin):
    """A reactome pathway."""

    __tablename__ = PATHWAY_TABLE_NAME
    id = Column(Integer, primary_key=True)

    prefix = REACTOME
    identifier = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))

    parent_id = Column(Integer, ForeignKey(f'{PATHWAY_TABLE_NAME}.id'))
    children = relationship('Pathway', backref=backref('parent', remote_side=[id]))

    species = relationship(Species, backref='pathways')
    species_id = Column(Integer, ForeignKey(f'{Species.__tablename__}.id'))

    proteins = relationship(Protein, secondary=protein_pathway, backref='pathways')
    chemicals = relationship(Chemical, secondary=chemical_pathway, backref='pathways')
