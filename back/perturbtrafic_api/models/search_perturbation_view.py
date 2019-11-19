from sqlalchemy import (
    Column,
    Index,
    Numeric,
    Text,
    Boolean,
    DateTime,
    BigInteger,
    Integer
)

from .meta import Base


class SearchPerturbationView(Base):
    __tablename__ = 'recherche_perturbation'

    id = Column(Numeric, primary_key=True)
    id_entite = Column(BigInteger)
    type = Column(Numeric)
    description_type = Column(Text)
    etat = Column(Numeric)
    description_etat = Column(Text)
    urgence = Column(Boolean)
    description = Column(Text)
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    heure_debut = Column(DateTime)
    heure_fin = Column(DateTime)
    id_utilisateur_ajout = Column(Numeric)
    nom_utilisateur_ajout = Column(Text)
    axe = Column(Text)
    pr_debut = Column(Text)
    pr_debut_seg_seq = Column(Integer)
    pr_debut_sec_seq = Column(Integer)
    pr_fin = Column(Text)
    pr_fin_seg_seq = Column(Integer)
    pr_fin_sec_seq = Column(Integer)
    id_evenement = Column(Numeric)
    numero_dossier_evenement = Column(Text)
    description_evenement = Column(Text)
    type_evenement = Column(Numeric)
    description_type_evenement = Column(Text)
    localisation_impression = Column(Text)
    tranche_horaire = Column(Boolean)
    deviation = Column(Text)
    id_utilisateur = Column(Numeric)
    compteur_touche = Column(Boolean)
    modification_autorise = Column(Boolean)
    suppression_autorise = Column(Boolean)

    def format(self):
        return {
            'id': self.id,
            'id_entite': self.id_entite,
            'type': self.type,
            'description_type': self.description_type,
            'etat': self.etat,
            'description_etat': self.description_etat,
            'urgence': self.urgence,
            'description': self.description,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'date_fin': self.date_fin if not self.date_fin else self.date_fin.isoformat(),
            'heure_debut': self.heure_debut if not self.heure_debut else self.heure_debut.isoformat(),
            'heure_fin': self.heure_fin if not self.heure_fin else self.heure_fin.isoformat(),
            'id_utilisateur_ajout': self.id_utilisateur_ajout,
            'nom_utilisateur_ajout': self.nom_utilisateur_ajout,
            'axe': self.axe,
            'pr_debut': self.pr_debut,
            'pr_debut_seg_seq': self.pr_debut_seg_seq,
            'pr_debut_sec_seq': self.pr_debut_sec_seq,
            'pr_fin': self.pr_fin,
            'pr_fin_seg_seq': self.pr_fin_seg_seq,
            'pr_fin_sec_seq': self.pr_fin_sec_seq,
            'id_evenement': self.id_evenement,
            'numero_dossier_evenement': self.numero_dossier_evenement,
            'description_evenement': self.description_evenement,
            'type_evenement': self.type_evenement,
            'description_type_evenement': self.description_type_evenement,
            'localisation_impression': self.localisation_impression,
            'tranche_horaire': self.tranche_horaire,
            'deviation': self.deviation,
            'compteur_touche': self.compteur_touche,
            'modification_autorise': self.modification_autorise,
            'suppression_autorise': self.suppression_autorise
        }

#Index('my_index', SearchEvenementView.libelle, unique=True, mysql_length=255)
