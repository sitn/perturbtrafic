from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class LienChantierCategorieChantier(Base):
    __tablename__ = 'lien_chantier_categorie_chantier'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_chantier = Column(BigInteger)
    categorie = Column(BigInteger)


#Index('my_index', LienChantierCategorieChantier.nom, unique=True, mysql_length=255)
