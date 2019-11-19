from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class EtatPerturbation(Base):
    __tablename__ = 'etat_perturbation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    description = Column(Text)


Index('my_index', EtatPerturbation.description, unique=True, mysql_length=255)
