# -*- coding: utf-8 -*-

"""Reactome database model"""

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from pybel.constants import FUNCTION, NAMESPACE, NAME, BIOPROCESS

Base = declarative_base()

TABLE_PREFIX = 'reactome'
PATHWAY_TABLE_NAME = '{}_pathway'.format(TABLE_PREFIX)
PATHWAY_TABLE_HIERARCHY = '{}_pathway_hierarchy'.format(TABLE_PREFIX)
SPECIES_TABLE_NAME = '{}_species'.format(TABLE_PREFIX)
UNIPROT_TABLE_NAME = '{}_uniprot'.format(TABLE_PREFIX)
CHEBI_TABLE_NAME = '{}_chebi'.format(TABLE_PREFIX)
UNIPROT_PATHWAY_TABLE = '{}_uniprot_pathway'.format(TABLE_PREFIX)
CHEBI_PATHWAY_TABLE = '{}_chebi_pathway'.format(TABLE_PREFIX)

pathway_hierarchy = Table(
    PATHWAY_TABLE_HIERARCHY,
    Base.metadata,
    Column('parent_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)), primary_key=True),
    Column('child_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)), primary_key=True)
)

uniprot_pathway = Table(
    UNIPROT_PATHWAY_TABLE,
    Base.metadata,
    Column('uniprot_id', Integer, ForeignKey(UNIPROT_TABLE_NAME + 'uniprot_id')),
    Column('pathway_id', Integer, ForeignKey(PATHWAY_TABLE_NAME + 'reactome_id'))
)

chebi_pathway = Table(
    CHEBI_PATHWAY_TABLE,
    Base.metadata,
    Column('chebi_id', Integer, ForeignKey(CHEBI_TABLE_NAME + 'chebi_id')),
    Column('pathway_id', Integer, ForeignKey(PATHWAY_TABLE_NAME + 'reactome_id'))
)


class Pathway(Base):
    """Pathway Table"""

    __tablename__ = PATHWAY_TABLE_NAME

    reactome_id = Column(String(255), primary_key=True)

    name = Column(String(255))

    children = relationship(
        'Pathway',
        secondary=pathway_hierarchy,
        primaryjoin=(id == pathway_hierarchy.c.parent_id),
        secondaryjoin=(id == pathway_hierarchy.c.child_id)
    )

    species = relationship('Species', back_populates='pathways')

    genes = relationship(
        'UniProt',
        secondary=uniprot_pathway,
        backref='pathways'
    )

    chemicals = relationship(
        'Chebi',
        secondary=chebi_pathway,
        backref='pathways'
    )

    def __repr__(self):
        return self.name

    @property
    def pathway_species(self):
        return self.species.name

    def serialize_to_pathway_node(self):
        """Function to serialize to PyBEL node data dictionary.
        :rtype: dict
        """
        return {
            FUNCTION: BIOPROCESS,
            NAMESPACE: 'REACTOME',
            NAME: self.name
        }


class Species(Base):
    """Species Table"""

    __tablename__ = SPECIES_TABLE_NAME

    species_id = Column(Integer, primary_key=True)

    name = Column(String(255))

    def __repr__(self):
        return self.name


class UniProt(Base):
    """Genes Table"""

    __tablename__ = UNIPROT_TABLE_NAME

    uniprot_id = Column(String(255), primary_key=True)

    def __repr__(self):
        return self.uniprot_id


class Chebi(Base):
    """Chemical Chebi Table"""

    __tablename__ = CHEBI_TABLE_NAME

    chebi_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return self.chebi_id
