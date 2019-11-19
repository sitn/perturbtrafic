from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Numeric,
    Text,
    Boolean
)

from .meta import Base


class Fermeture(Base):
    __tablename__ = 'fermeture'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_perturbation = Column(Numeric)
    deviation = Column(Text)
    id_responsable = Column(Numeric)

#Index('my_index', Fermeture.nom, unique=True, mysql_length=255)
