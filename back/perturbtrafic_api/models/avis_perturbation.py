from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Numeric,
    Text,
    Boolean,
    DateTime
)

from .meta import Base
from sqlalchemy.sql import func

class AvisPerturbation(Base):
    __tablename__ = 'avis_perturbation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_perturbation = Column(Numeric)
    id_contact = Column(BigInteger)
    date_envoi = Column(DateTime, default=func.now())

#Index('my_index', AvisPerturbation.nom, unique=True, mysql_length=255)

