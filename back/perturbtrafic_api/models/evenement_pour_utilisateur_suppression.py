from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class EvenementPourUtilisateurSuppression(Base):
    __tablename__ = 'evenement_pour_utilisateur_suppression'
    id_evenement = Column(BigInteger, primary_key=True)
    id_utilisateur = Column(BigInteger, primary_key=True)


#Index('my_index', EvenementPourUtilisateurSuppression.nom, unique=True, mysql_length=255)
