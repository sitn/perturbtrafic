from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class Manifestation(Base):
    __tablename__ = 'manifestation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_evenement = Column(BigInteger)
    parcours = Column(Text)

    def format(self):
        return {
            'id': self.id,
            'id_evenement': self.id_evenement,
            'parcours': self.parcours
        }

#Index('my_index', Manifestation.nom, unique=True, mysql_length=255)
