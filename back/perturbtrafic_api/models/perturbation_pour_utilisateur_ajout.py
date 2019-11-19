from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class PerturbationPourUtilisateurAjout(Base):
    __tablename__ = 'perturbation_pour_utilisateur_ajout'
    id_evenement = Column(BigInteger, primary_key=True)
    id_entite = Column(BigInteger, primary_key=True)
    id_utilisateur = Column(BigInteger, primary_key=True)
    numero_dossier = Column(Text)
    libelle = Column(Text)
    description = Column(Text)

#Index('my_index', PerturbationPourUtilisateurAjout.nom, unique=True, mysql_length=255)
