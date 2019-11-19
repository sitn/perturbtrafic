from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class TypeReperage(Base):
    __tablename__ = 'type_reperage'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    description = Column(Text)


Index('my_index', TypeReperage.description, unique=True, mysql_length=255)
