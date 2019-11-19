from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class CategorieChantier(Base):
    __tablename__ = 'categorie_chantier'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    description = Column(Text)


Index('my_index', CategorieChantier.description, unique=True, mysql_length=255)
