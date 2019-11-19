from sqlalchemy import (
    Column,
    Index,
    Integer,
    BigInteger,
    Text,
    DateTime,
    Boolean
)

from .meta import Base


class EvenementEcheance(Base):
    __tablename__ = 'evenement_echeance'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_entite = Column(BigInteger)
    numero_dossier = Column(Text)
    libelle = Column(Text)
    date_debut =  Column(DateTime)
    modification_autorise = Column(Boolean)
    id_utilisateur = Column(BigInteger)

    def format(self):
        return {
            'id': self.id,
            'id_entite': self.id_entite,
            'numero_dossier': self.numero_dossier,
            'libelle': self.libelle,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'modification_autorise': self.modification_autorise,
            'id_utilisateur': self.id_utilisateur
        }


#Index('my_index', EvenementEcheance.description, unique=True, mysql_length=255)
