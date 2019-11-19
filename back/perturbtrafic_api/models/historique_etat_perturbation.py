from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    DateTime,
    func
)

from .meta import Base


class HistoriqueEtatPerturbation(Base):
    __tablename__ = 'historique_etat_perturbation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_perturbation = Column(BigInteger)
    id_utilisateur = Column(BigInteger)
    date = Column(DateTime, default=func.now(), onupdate=func.now())
    etat = Column(BigInteger)

#Index('my_index', HistoriqueEtatPerturbation.nom, unique=True, mysql_length=255)
