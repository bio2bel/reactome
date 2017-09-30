# -*- coding: utf-8 -*-

"""Reactome database model"""

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from pybel.constants import FUNCTION, NAMESPACE, NAME, BIOPROCESS

Base = declarative_base()

TABLE_PREFIX = "reactome"
PATHWAY_TABLE_NAME = "{}_pathway".format(TABLE_PREFIX)
PATHWAY_TABLE_HIERARCHY = "{}_pathway_hierarchy".format(TABLE_PREFIX)
SPECIES_TABLE_NAME = "{}_species".format(TABLE_PREFIX)
UNIPROT_TABLE_NAME = "{}_uniprot".format(TABLE_PREFIX)
CHEBI_TABLE_NAME = "{}_chebi".format(TABLE_PREFIX)

pathway_hierarchy = Table(
    PATHWAY_TABLE_HIERARCHY,
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("{}.id".format(PATHWAY_TABLE_NAME)), primary_key=True),
    Column("child_id", Integer, ForeignKey("{}.id".format(PATHWAY_TABLE_NAME)), primary_key=True)
)


class Pathway(Base):
    """Pathway Table"""

    __tablename__ = PATHWAY_TABLE_NAME

    reactome_id = Column(Integer, primary_key=True)

    pathway_name = Column(String(255))
    pathway_species = Column(String(255))

    children = relationship(
        "Pathway",
        secondary=pathway_hierarchy,
        primaryjoin=(id == pathway_hierarchy.c.parent_id),
        secondaryjoin=(id == pathway_hierarchy.c.child_id)
    )

    species = relationship("Species", back_populates="pathways")

    def __repr__(self):
        return self.pathway_name


    def serialize_to_pathway_node(self):
        """Function to serialize to PyBEL node data dictionary.
        :rtype: dict
        """
        return {
            FUNCTION: BIOPROCESS,
            NAMESPACE: 'REACTOME',
            NAME: self.pathway_name
        }


class Species(Base):
    """Species Table"""

    __tablename__ = SPECIES_TABLE_NAME

    species_id = Column(Integer, primary_key=True)

    species_name = Column(String(255))

    def __repr__(self):
        return self.species_name
