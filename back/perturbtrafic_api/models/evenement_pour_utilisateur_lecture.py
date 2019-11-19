from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class EvenementPourUtilisateurLecture(Base):
    __tablename__ = 'evenement_pour_utilisateur_lecture'
    id_evenement = Column(BigInteger, primary_key=True)
    id_utilisateur = Column(BigInteger, primary_key=True)


#Index('my_index', EvenementPourUtilisateurLecture.nom, unique=True, mysql_length=255)
