from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Integer
)

from .meta import Base


class Axe(Base):
    __tablename__ = 'axe'
    proprietaire = Column(Text)
    nom = Column(Text)
    position = Column(Text)
    nom_complet = Column(Text, primary_key=True)


#Index('my_index', Axe.nom, unique=True, mysql_length=255)

