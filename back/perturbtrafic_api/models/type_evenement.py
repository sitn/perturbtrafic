from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class TypeEvenement(Base):
    __tablename__ = 'type_evenement'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    description = Column(Text)


Index('my_index', TypeEvenement.description, unique=True, mysql_length=255)
