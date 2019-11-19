from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Boolean
)

from .meta import Base


class ContactPotentielAvisPerturbation(Base):
    __tablename__ = 'contact_potentiel_avis_perturbation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_entite = Column(BigInteger)
    id_contact = Column(BigInteger)
    envoi_auto_occupation = Column(Boolean)
    envoi_auto_fermeture = Column(Boolean)

    def format(self, nom, prenom, organisme):
        return {
            'id': self.id,
            'id_contact': self.id_contact,
            'envoi_auto_occupation': self.envoi_auto_occupation,
            'envoi_auto_fermeture': self.envoi_auto_fermeture,
            'nom': nom,
            'prenom': prenom,
            'organisme': organisme
        }
#Index('my_index', Contact.nom, unique=True, mysql_length=255)
