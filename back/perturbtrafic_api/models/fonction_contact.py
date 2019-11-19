from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Integer
)

from .meta import Base


class FonctionContact(Base):
    __tablename__ = 'fonction_contact'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_contact = Column(BigInteger)
    fonction = Column(Text)

#Index('my_index', FonctionContact.nom, unique=True, mysql_length=255)
