from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class LienContactEntite(Base):
    __tablename__ = 'lien_contact_entite'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_contact = Column(BigInteger)
    id_entite = Column(BigInteger)


#Index('my_index', LienContactEntite.nom, unique=True, mysql_length=255)
