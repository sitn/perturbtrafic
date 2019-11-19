from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Numeric,
    Float,
    Text,
    Boolean,
    DateTime
)

from .meta import Base
import json

class Chantier(Base):
    __tablename__ = 'chantier'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_evenement = Column(Numeric)
    id_maitre_ouvrage = Column(Numeric)
    id_direction_locale = Column(Numeric)
    id_entrepreneur = Column(Numeric)
    id_responsable_travaux = Column(Numeric)
    projet = Column(Text)
    longueur_etape = Column(Float)
    surface = Column(Float)
    id_centrale_enrobage = Column(Numeric)
    epaisseur_caisson = Column(Text)
    qualite_caisson = Column(Text)
    epaisseur_support = Column(Text)
    qualite_support = Column(Text)
    epaisseur_revetement = Column(Text)
    qualite_revetement = Column(Text)
    qualite_encollage = Column(Text)
    boucle_induction = Column(Boolean)
    faucher_accotement = Column(Boolean)
    curer_depotoirs = Column(Boolean)
    nettoyer_bords = Column(Boolean)
    colmater_fissure = Column(Boolean)
    pr_touches = Column(Boolean)
    autre = Column(Text)
    lieu_seance = Column(Text)
    jour_seance = Column(Text)
    heure_seance = Column(Text)
    reperage_effectif = Column(Boolean)

    def format(self):
        return {
            'id': self.id,
            'id_evenement': self.id_evenement,
            'id_maitre_ouvrage': self.id_maitre_ouvrage,
            'id_direction_locale': self.id_direction_locale,
            'id_entrepreneur': self.id_entrepreneur,
            'id_responsable_travaux': self.id_responsable_travaux,
            'projet': self.projet,
            'longueur_etape': json.loads(str(self.longueur_etape)) if self.longueur_etape else None,
            'surface': json.loads(str(self.surface)) if self.surface else None,
            'id_centrale_enrobage': self.id_centrale_enrobage,
            'epaisseur_caisson': self.epaisseur_caisson,
            'qualite_caisson': self.qualite_caisson,
            'epaisseur_support': self.epaisseur_support,
            'qualite_support': self.qualite_support,
            'epaisseur_revetement': self.epaisseur_revetement,
            'qualite_revetement': self.qualite_revetement,
            'qualite_encollage': self.qualite_encollage,
            'boucle_induction': self.boucle_induction,
            'faucher_accotement': self.faucher_accotement,
            'curer_depotoirs': self.curer_depotoirs,
            'nettoyer_bords': self.nettoyer_bords,
            'colmater_fissure': self.colmater_fissure,
            'pr_touches': self.pr_touches,
            'autre': self.autre,
            'lieu_seance': self.lieu_seance,
            'jour_seance': self.jour_seance, # if not self.jour_seance else self.jour_seance.isoformat(),
            'heure_seance': self.heure_seance, # if not self.heure_seance else self.heure_seance.isoformat(),
            'reperage_effectif': self.reperage_effectif
        }


#Index('my_index', Chantier.nom, unique=True, mysql_length=255)
