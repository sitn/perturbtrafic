from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Integer
)

from .meta import Base


class Localite(Base):
    __tablename__ = 'localite'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    npa_nom = Column(Text)

#Index('my_index', Localite.nom, unique=True, mysql_length=255)
