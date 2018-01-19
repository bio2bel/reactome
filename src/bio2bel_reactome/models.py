# -*- coding: utf-8 -*-

"""Reactome database model"""

from pybel.dsl import bioprocess, protein, abundance
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from bio2bel_reactome.constants import HGNC, REACTOME, CHEBI

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

pathway_hierarchy = Table(
    PATHWAY_TABLE_HIERARCHY,
    Base.metadata,
    Column('parent_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)), primary_key=True),
    Column('child_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)), primary_key=True)
)

protein_pathway = Table(
    PROTEIN_PATHWAY_TABLE,
    Base.metadata,
    Column('protein_id', Integer, ForeignKey('{}.id'.format(PROTEIN_TABLE_NAME))),
    Column('pathway_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)))
)

chemical_pathway = Table(
    CHEMICAL_PATHWAY_TABLE,
    Base.metadata,
    Column('chemical_id', Integer, ForeignKey('{}.id'.format(CHEMICAL_TABLE_NAME))),
    Column('pathway_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)))
)


class Pathway(Base):
    """Pathway Table"""
    __tablename__ = PATHWAY_TABLE_NAME

    id = Column(Integer, primary_key=True)

    reactome_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))

    children = relationship(
        'Pathway',
        secondary=pathway_hierarchy,
        primaryjoin=(id == pathway_hierarchy.c.parent_id),
        secondaryjoin=(id == pathway_hierarchy.c.child_id)
    )

    species = relationship(
        'Species',
        backref='pathways'
    )

    species_id = Column(Integer, ForeignKey('{}.id'.format(SPECIES_TABLE_NAME)))

    proteins = relationship(
        'Protein',
        secondary=protein_pathway,
        backref='pathways'
    )

    chemicals = relationship(
        'Chemical',
        secondary=chemical_pathway,
        backref='pathways'
    )

    def __repr__(self):
        return self.name

    def as_pybel_dict(self):
        """Function to serialize to PyBEL node data dictionary.
        :rtype: pybel.dsl.bioprocess
        """
        return bioprocess(
            namespace=REACTOME,
            name=str(self.name),
            identifier=str(self.reactome_id)
        )

    def get_pathway_pathway_hierarchy(self):
        NotImplemented


class Species(Base):
    """Species Table"""

    __tablename__ = SPECIES_TABLE_NAME

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name


class Protein(Base):
    """Protein Table"""
    __tablename__ = PROTEIN_TABLE_NAME

    id = Column(Integer, primary_key=True)
    species_id = Column(Integer, ForeignKey('{}.id'.format(SPECIES_TABLE_NAME)))

    uniprot_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return self.uniprot_id

    def as_pybel_dict(self):
        """Function to serialize to PyBEL node data dictionary.
        :rtype: pybel.dsl.protein
        """
        return protein(
            namespace=HGNC,
            name=str(self.get_hgnc_symbol(self.uniprot_id)),
            identifier=str(self.uniprot_id)
        )

    def get_hgnc_symbol(self, uniprot_id):
        NotImplemented

    def get_hgnc_id(self, uniprot_id):
        NotImplemented


class Chemical(Base):
    """Chemical Table"""
    __tablename__ = CHEMICAL_TABLE_NAME

    id = Column(Integer, primary_key=True)

    chebi_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return self.chebi_id

    def as_pybel_dict(self):
        """Function to serialize to PyBEL node data dictionary.
        :rtype: pybel.dsl.abundance
        """
        return abundance(
            namespace=CHEBI,
            name=str(self.get_chebi_name(self.chebi_id)),
            identifier=str(self.chebi_id)
        )

    def get_chebi_name(self, chebi_id):
        NotImplemented
