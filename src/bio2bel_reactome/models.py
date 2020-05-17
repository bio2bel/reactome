# -*- coding: utf-8 -*-

"""Reactome database model."""

from __future__ import annotations

from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

import pybel.dsl
from bio2bel.compath import CompathPathwayMixin, CompathProteinMixin
from bio2bel.manager.models import SpeciesMixin
from .constants import CHEBI, HGNC, REACTOME, UNIPROT

Base = declarative_base()

TABLE_PREFIX = 'reactome'
PATHWAY_TABLE_NAME = f'{TABLE_PREFIX}_pathway'
PATHWAY_TABLE_HIERARCHY = f'{TABLE_PREFIX}_pathway_hierarchy'
SPECIES_TABLE_NAME = f'{TABLE_PREFIX}_species'
PROTEIN_TABLE_NAME = f'{TABLE_PREFIX}_protein'
CHEMICAL_TABLE_NAME = f'{TABLE_PREFIX}_chemical'
PROTEIN_PATHWAY_TABLE = f'{TABLE_PREFIX}_protein_pathway'
CHEMICAL_PATHWAY_TABLE = f'{TABLE_PREFIX}_chemical_pathway'
SPECIES_PATHWAY_TABLE = f'{TABLE_PREFIX}_species_pathway'

protein_pathway = Table(
    PROTEIN_PATHWAY_TABLE,
    Base.metadata,
    Column('protein_id', Integer, ForeignKey(f'{PROTEIN_TABLE_NAME}.id')),
    Column('pathway_id', Integer, ForeignKey(f'{PATHWAY_TABLE_NAME}.id')),
)

chemical_pathway = Table(
    CHEMICAL_PATHWAY_TABLE,
    Base.metadata,
    Column('chemical_id', Integer, ForeignKey(f'{CHEMICAL_TABLE_NAME}.id'), primary_key=True),
    Column('pathway_id', Integer, ForeignKey(f'{PATHWAY_TABLE_NAME}.id'), primary_key=True),
)


class Species(Base, SpeciesMixin):
    """Species Table."""

    __tablename__ = SPECIES_TABLE_NAME


class Protein(Base, CompathProteinMixin):
    """Protein Table."""

    __tablename__ = PROTEIN_TABLE_NAME
    id = Column(Integer, primary_key=True)  # noqa:A003

    uniprot_id = Column(String(64), unique=True, nullable=False, index=True)
    uniprot_accession = Column(String(64), nullable=True)

    # Only for Human Genes
    hgnc_symbol = Column(String(64), nullable=True)
    hgnc_id = Column(String(64), nullable=True)

    def __repr__(self) -> str:  # noqa:D105
        return self.uniprot_id

    def to_pybel(self) -> pybel.dsl.Protein:
        """Serialize to PyBEL node data dictionary."""
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
    id = Column(Integer, primary_key=True)  # noqa:A003

    chebi_id = Column(String(64), unique=True, nullable=False)
    name = Column(String(4096))

    pathways: List[Pathway]

    def __repr__(self) -> str:  # noqa:D105
        return self.chebi_id

    def to_pybel(self) -> pybel.dsl.Abundance:
        """Serialize to PyBEL node data dictionary."""
        return pybel.dsl.Abundance(
            namespace=CHEBI,
            identifier=self.chebi_id,
            name=self.name,
        )


class Pathway(Base, CompathPathwayMixin):
    """A reactome pathway."""

    __tablename__ = PATHWAY_TABLE_NAME
    id = Column(Integer, primary_key=True)  # noqa:A003

    prefix = REACTOME
    identifier = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))

    parent_id = Column(Integer, ForeignKey(f'{PATHWAY_TABLE_NAME}.id'))
    children = relationship('Pathway', backref=backref('parent', remote_side=[id]))

    species = relationship(Species, backref='pathways')
    species_id = Column(Integer, ForeignKey(f'{Species.__tablename__}.id'))

    proteins = relationship(Protein, secondary=protein_pathway, backref='pathways')
    chemicals = relationship(Chemical, secondary=chemical_pathway, backref='pathways')
