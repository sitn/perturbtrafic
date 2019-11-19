from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class PerturbationPourUtilisateurLecture(Base):
    __tablename__ = 'perturbation_pour_utilisateur_lecture'
    id_perturbation = Column(BigInteger, primary_key=True)
    id_utilisateur = Column(BigInteger, primary_key=True)


#Index('my_index', PerturbationPourUtilisateurLecture.nom, unique=True, mysql_length=255)
