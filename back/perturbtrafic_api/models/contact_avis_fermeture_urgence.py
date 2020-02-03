from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Boolean
)

from .meta import Base


class ContactAvisFermetureUrgence(Base):
    __tablename__ = 'contact_avis_fermeture_urgence'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_contact = Column(BigInteger)

    def format(self, nom, prenom, organisme):
        return {
            'id': self.id,
            'id_contact': self.id_contact,
            'nom': nom,
            'prenom': prenom,
            'organisme': organisme
        }

#Index('my_index', Contact.nom, unique=True, mysql_length=255)
