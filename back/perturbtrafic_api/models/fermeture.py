from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    Text,
)

from .meta import Base


class Fermeture(Base):
    __tablename__ = 'fermeture'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_perturbation = Column(Numeric)
    deviation = Column(Text)
    id_responsable = Column(Numeric)
