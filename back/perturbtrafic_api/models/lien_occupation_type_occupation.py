from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class LienOccupationTypeOccupation(Base):
    __tablename__ = 'lien_occupation_type_occupation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_occupation = Column(BigInteger)
    id_type_occupation = Column(BigInteger)


#Index('my_index', LienOccupationTypeOccupation.nom, unique=True, mysql_length=255)
