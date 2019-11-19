from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class LienFouillePlanType(Base):
    __tablename__ = 'lien_fouille_plan_type'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_evenement = Column(BigInteger)
    id_plan_type = Column(BigInteger)


#Index('my_index', LienChantierCategorieChantier.nom, unique=True, mysql_length=255)
