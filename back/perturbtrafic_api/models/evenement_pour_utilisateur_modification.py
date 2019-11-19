from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class EvenementPourUtilisateurModification(Base):
    __tablename__ = 'evenement_pour_utilisateur_modification'
    id_evenement = Column(BigInteger, primary_key=True)
    id_utilisateur = Column(BigInteger, primary_key=True)


#Index('my_index', EvenementPourUtilisateurModification.nom, unique=True, mysql_length=255)
