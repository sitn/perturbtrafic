from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class DestinataireFacturation(Base):
    __tablename__ = 'destinataire_facturation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    description = Column(Text)


Index('my_index', DestinataireFacturation.description, unique=True, mysql_length=255)
