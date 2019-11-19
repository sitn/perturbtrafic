from sqlalchemy import (
    Column,
    Text,
    Integer,
    Numeric
)

from .meta import Base
import json
import decimal

class Secteur(Base):
    __tablename__ = 'secteur'
    axe_nom = Column(Text)
    axe_nom_complet = Column(Text, primary_key=True)
    segment_sequence = Column(Integer)
    secteur_nom = Column(Text, primary_key=True)
    secteur_sequence = Column(Numeric)
    secteur_longueur = Column(Numeric)

    def format(self):
        return {
            'axe_nom_complet' : self.axe_nom_complet,
            'segment_sequence' : self.segment_sequence,
            'secteur_nom' : self.secteur_nom,
            'secteur_sequence' : 0 if self.secteur_sequence == 0 else json.loads(str(self.secteur_sequence)) if self.secteur_sequence else None,
            'secteur_longueur': 0 if self.secteur_longueur == 0 else json.loads(str(self.secteur_longueur)) if self.secteur_longueur else None
        }

#Index('my_index', Secteur.nom, unique=True, mysql_length=255)


