from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class TypePerturbation(Base):
    __tablename__ = 'type_perturbation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    description = Column(Text)


Index('my_index', TypePerturbation.description, unique=True, mysql_length=255)
