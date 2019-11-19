from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Float,
    Numeric,
    Text,
    Boolean,
    DateTime
)

from .meta import Base


class Reperage(Base):
    __tablename__ = 'reperage'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_evenement_ligne = Column(Numeric)
    id_perturbation_ligne = Column(BigInteger)
    id_deviation = Column(BigInteger)
    proprietaire = Column(Text)
    axe = Column(Text)
    sens = Column(Text)
    pr_debut = Column(Text)
    pr_debut_distance = Column(Float)
    pr_fin = Column(Text)
    pr_fin_distance = Column(Float)
    ecartd = Column(Float)
    ecartf = Column(Float)
    usage_neg = Column(Boolean)
    f_surf = Column(Float)
    f_long = Column(Float)

    def format(self):
        return {
            'id': self.id,
            'id_evenement_ligne': self.id_evenement_ligne,
            'id_perturbation_ligne': self.id_perturbation_ligne,
            'id_deviation': self.id_deviation,
            'proprietaire': self.proprietaire,
            'axe': self.axe,
            'sens': self.sens,
            'pr_debut': self.pr_debut,
            'pr_debut_distance': self.pr_debut_distance,
            'pr_fin': self.pr_fin,
            'pr_fin_distance': self.pr_fin_distance,
            'ecartd': self.ecartd,
            'ecartf': self.ecartf,
            'usage_neg': self.usage_neg,
            'f_surf': self.f_surf,
            'f_long': self.f_long
        }
#Index('my_index', Reperage.id, unique=True, mysql_length=255)
