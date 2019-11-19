from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Numeric,
    Text,
    Boolean
)

from .meta import Base


class Occupation(Base):
    __tablename__ = 'occupation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_perturbation = Column(Numeric)
    id_responsable_regulation = Column(Numeric)
    type_regulation = Column(Text)
    voies_condamnees = Column(Text)
    largeur_gabarit = Column(Text)
    hauteur_gabarit = Column(Text)
    heure_pointe = Column(Boolean, default=False)
    week_end = Column(Boolean, default=False)
    type_occupation = Column(Text)


#Index('my_index', Occupation.nom, unique=True, mysql_length=255)
