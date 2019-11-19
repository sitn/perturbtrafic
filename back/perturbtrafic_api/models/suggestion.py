from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Integer
)

from .meta import Base


class Suggestion(Base):
    __tablename__ = 'suggestion'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    liste = Column(Text)
    valeur = Column(Text)



#Index('my_index', Suggestion.nom, unique=True, mysql_length=255)
