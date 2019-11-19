from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from .meta import Base


class PlanTypeFouille(Base):
    __tablename__ = 'plan_type_fouille'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    description = Column(Text)


#Index('my_index', plan_type_fouille.description, unique=True, mysql_length=255)
