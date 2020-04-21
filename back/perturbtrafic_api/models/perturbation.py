from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    Text,
    DateTime,
    Boolean,
    func
)

from .meta import Base


class Perturbation(Base):
    __tablename__ = 'perturbation'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_evenement = Column(Numeric)
    id_responsable_trafic = Column(Numeric)
    type = Column(Numeric)
    tranche_horaire = Column(Boolean, default=False)
    description = Column(Text)
    date_debut = Column(DateTime)
    heure_debut = Column(DateTime)
    date_fin = Column(DateTime)
    heure_fin = Column(DateTime)
    localisation = Column(Text)
    nom_responsable_trafic = Column(Text)
    prenom_responsable_trafic = Column(Text)
    mobile_responsable_trafic = Column(Text)
    telephone_responsable_trafic = Column(Text)
    fax_responsable_trafic = Column(Text)
    courriel_responsable_trafic = Column(Text)
    remarque = Column(Text)
    urgence = Column(Boolean)
    etat = Column(Numeric)
    date_validation = Column(DateTime)
    id_utilisateur_validation = Column(BigInteger)
    decision = Column(Text)
    date_decision = Column(DateTime)
    id_utilisateur_ajout = Column(Numeric)
    date_ajout = Column(DateTime, default=func.now())
    id_utilisateur_modification = Column(Numeric)
    date_modification = Column(DateTime, default=func.now(), onupdate=func.now())
    date_suppression = Column(DateTime)

    def format(self):
        return {
            'id': self.id,
            'id_evenement': self.id_evenement,
            'id_responsable_trafic': self.id_responsable_trafic,
            'type': self.type,
            'tranche_horaire': self.tranche_horaire,
            'description': self.description,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'heure_debut': self.heure_debut if not self.heure_debut else self.heure_debut.isoformat(),
            'date_fin': self.date_fin if not self.date_fin else self.date_fin.isoformat(),
            'heure_fin': self.heure_fin if not self.heure_fin else self.heure_fin.isoformat(),
            'localisation': self.localisation,
            'nom_responsable_trafic': self.nom_responsable_trafic,
            'prenom_responsable_trafic': self.prenom_responsable_trafic,
            'mobile_responsable_trafic': self.mobile_responsable_trafic,
            'telephone_responsable_trafic': self.telephone_responsable_trafic,
            'fax_responsable_trafic': self.fax_responsable_trafic,
            'courriel_responsable_trafic': self.courriel_responsable_trafic,
            'remarque': self.remarque,
            'urgence': self.urgence,
            'etat': self.etat,
            'date_validation': self.date_validation if not self.date_validation else self.date_validation.isoformat(),
            'id_utilisateur_validation': self.id_utilisateur_validation,
            'decision': self.decision,
            'date_decision': self.date_decision if not self.date_decision else self.date_decision.isoformat(),
            'id_utilisateur_ajout': self.id_utilisateur_ajout,
            'date_ajout': self.date_ajout if not self.date_ajout else self.date_ajout.isoformat(),
            'id_utilisateur_modification': self.id_utilisateur_modification,
            'date_modification': self.date_modification if not self.date_modification else self.date_modification.isoformat(),
            'date_suppression': self.date_suppression if not self.date_suppression else self.date_suppression.isoformat()
        }

    def format_with_type_evenement(self, type_evenement):
        return {
            'id': self.id,
            'id_evenement': self.id_evenement,
            'id_responsable_trafic': self.id_responsable_trafic,
            'type': self.type,
            'tranche_horaire': self.tranche_horaire,
            'description': self.description,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'heure_debut': self.heure_debut if not self.heure_debut else self.heure_debut.isoformat(),
            'date_fin': self.date_fin if not self.date_fin else self.date_fin.isoformat(),
            'heure_fin': self.heure_fin if not self.heure_fin else self.heure_fin.isoformat(),
            'localisation': self.localisation,
            'nom_responsable_trafic': self.nom_responsable_trafic,
            'prenom_responsable_trafic': self.prenom_responsable_trafic,
            'mobile_responsable_trafic': self.mobile_responsable_trafic,
            'telephone_responsable_trafic': self.telephone_responsable_trafic,
            'fax_responsable_trafic': self.fax_responsable_trafic,
            'courriel_responsable_trafic': self.courriel_responsable_trafic,
            'remarque': self.remarque,
            'urgence': self.urgence,
            'etat': self.etat,
            'date_validation': self.date_validation if not self.date_validation else self.date_validation.isoformat(),
            'id_utilisateur_validation': self.id_utilisateur_validation,
            'decision': self.decision,
            'date_decision': self.date_decision if not self.date_decision else self.date_decision.isoformat(),
            'id_utilisateur_ajout': self.id_utilisateur_ajout,
            'date_ajout': self.date_ajout if not self.date_ajout else self.date_ajout.isoformat(),
            'id_utilisateur_modification': self.id_utilisateur_modification,
            'date_modification': self.date_modification if not self.date_modification else self.date_modification.isoformat(),
            'date_suppression': self.date_suppression if not self.date_suppression else self.date_suppression.isoformat(),
            'type_evenement': type_evenement
        }
