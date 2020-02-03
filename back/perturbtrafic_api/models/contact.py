from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class Contact(Base):
    __tablename__ = 'contact'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    login = Column(Text)
    nom = Column(Text)
    prenom = Column(Text)
    telephone = Column(Text)
    mobile = Column(Text)
    courriel = Column(Text)
    id_organisme = Column(BigInteger)

    def format(self):
        return {
            'id': self.id,
            'login': self.login,
            'nom': self.nom,
            'prenom': self.prenom,
            'telephone': self.telephone,
            'mobile': self.mobile,
            'courriel': self.courriel,
            'id_organisme': self.id_organisme
        }

#Index('my_index', Contact.nom, unique=True, mysql_length=255)
