from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Integer,
    Boolean
)

from .meta import Base


class Delegation(Base):
    __tablename__ = 'delegation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_delegant = Column(BigInteger)
    id_delegataire = Column(BigInteger)
    autorisation_lecture = Column(Boolean)
    autorisation_modification = Column(Boolean)
    autorisation_suppression = Column(Boolean)


    def format(self, nom, prenom):
        return {
            'id': self.id,
            'id_delegant': self.id_delegant,
            'id_delegataire': self.id_delegataire,
            'autorisation_lecture': self.autorisation_lecture,
            'autorisation_modification': self.autorisation_modification,
            'autorisation_suppression': self.autorisation_suppression,
            'nom': nom,
            'prenom': prenom
        }

#Index('my_index', Delegation.nom, unique=True, mysql_length=255)
