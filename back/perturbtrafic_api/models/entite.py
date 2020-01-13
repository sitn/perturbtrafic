from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Integer
)

from .meta import Base


class Entite(Base):
    __tablename__ = 'entite'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    nom = Column(Text)
    id_responsable = Column(BigInteger)
    limite_echeance_popup_evenement = Column(Integer, default=10)
    nom_groupe_ad = Column(Text)

    def format(self):
        return {
            'id': self.id,
            'nom': self.nom
        }

#Index('my_index', Entite.nom, unique=True, mysql_length=255)
