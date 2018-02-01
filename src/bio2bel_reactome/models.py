# -*- coding: utf-8 -*-

"""Reactome database model"""

from pybel.dsl import bioprocess, protein, abundance
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from bio2bel_reactome.constants import HGNC, REACTOME, CHEBI, UNIPROT

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
    Column('chemical_id', Integer, ForeignKey('{}.id'.format(CHEMICAL_TABLE_NAME))),
    Column('pathway_id', Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)))
)


class Pathway(Base):
    """Pathway Table"""
    __tablename__ = PATHWAY_TABLE_NAME

    id = Column(Integer, primary_key=True)

    reactome_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))

    parent_id = Column(Integer, ForeignKey('{}.id'.format(PATHWAY_TABLE_NAME)))

    children = relationship('Pathway', backref=backref('parent', remote_side=[id]))

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

    uniprot_id = Column(String, unique=True, nullable=False, index=True)

    # Only for Human Genes
    hgnc_symbol = Column(String, nullable=True)
    hgnc_id = Column(String, nullable=True)

    def __repr__(self):
        return self.uniprot_id

    def as_pybel_dict(self):
        """Function to serialize to PyBEL node data dictionary.
        :rtype: pybel.dsl.protein
        """

        if self.hgnc_symbol and self.hgnc_id:
            return protein(
                namespace=HGNC,
                name=self.hgnc_symbol,
                identifier=self.hgnc_id
            )

        else:
            return protein(
                namespace=UNIPROT,
                name=self.uniprot_id,
                identifier=self.uniprot_id
            )

    def get_pathways(self):
        """Returns the pathways associated with the protein"""
        return {
            pathway.name
            for pathway in self.pathways
        }


class Chemical(Base):
    """Chemical Table"""
    __tablename__ = CHEMICAL_TABLE_NAME

    id = Column(Integer, primary_key=True)

    chebi_id = Column(String, unique=True, nullable=False)
    chebi_name = Column(String)

    def __repr__(self):
        return self.chebi_id

    def as_pybel_dict(self):
        """Function to serialize to PyBEL node data dictionary.
        :rtype: pybel.dsl.abundance
        """
        return abundance(
            namespace=CHEBI,
            name=str(self.chebi_name),
            identifier=str(self.chebi_id)
        )
