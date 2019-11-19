from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class Organisme(Base):
    __tablename__ = 'organisme'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    nom = Column(Text)
    adresse = Column(Text)
    localite = Column(Text)
    telephone = Column(Text)
    fax = Column(Text)
    courriel = Column(Text)

Index('my_index', Organisme.nom, unique=True, mysql_length=255)
