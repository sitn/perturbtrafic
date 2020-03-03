from sqlalchemy import (
    Column,
    Index,
    Integer,
    BigInteger,
    Text,
    DateTime,
    JSON,
    Boolean
)

from .meta import Base


class PerturbationImpression(Base):
    __tablename__ = 'perturbation_impression'
    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger)
    localisation = Column(Text)
    localisation_impression = Column(Text)
    type_description = Column(Text)
    urgence = Column()
    numero_dossier = Column(Text)
    division = Column(Text)
    libelle_evenement = Column(Text)
    type_description_evenement = Column(Text)
    description = Column(Text)
    decision = Column(Text)
    date_debut = Column(DateTime)
    heure_debut = Column(DateTime)
    date_fin = Column(DateTime)
    heure_fin = Column(DateTime)
    tranche_horaire = Column(Boolean)
    remarque = Column(Text)
    nom_responsable_trafic = Column(Text)
    prenom_responsable_trafic = Column(Text)
    mobile_responsable_trafic = Column(Text)
    telephone_responsable_trafic = Column(Text)
    fax_responsable_trafic = Column(Text)
    courriel_responsable_trafic = Column(Text)
    etat_description = Column(Text)
    deviation = Column(Text)
    type_occupation = Column(Text)
    voies_condamnees = Column(Text)
    type_regulation = Column(Text)
    largeur_gabarit = Column(Text)
    hauteur_gabarit = Column(Text)
    heure_pointe = Column(Boolean)
    week_end = Column(Boolean)
    logo_entite = Column(Text)
    nom_entite = Column(Text)
    geometry_point = Column(JSON)
    geometry_ligne = Column(JSON)
    geometry_deviation = Column(JSON)
    preavis_contacts = Column(JSON)
    reperages = Column(JSON)

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'localisation': self.localisation,
            'localisation_impression': self.localisation_impression,
            'type_description': self.type_description,
            'urgence': self.urgence,
            'numero_dossier': self.numero_dossier,
            'division': self.division,
            'libelle_evenement': self.libelle_evenement,
            'type_description_evenement': self.type_description_evenement,
            'description': self.description,
            'decision': self.decision,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'heure_debut': self.heure_debut if not self.heure_debut else self.heure_debut.isoformat(),
            'date_fin': self.date_fin if not self.date_fin else self.date_fin.isoformat(),
            'heure_fin': self.heure_fin if not self.heure_fin else self.heure_fin.isoformat(),
            'tranche_horaire': self.tranche_horaire,
            'remarque': self.remarque,
            'nom_responsable_trafic': self.nom_responsable_trafic,
            'prenom_responsable_trafic': self.prenom_responsable_trafic,
            'mobile_responsable_trafic': self.mobile_responsable_trafic,
            'telephone_responsable_trafic': self.telephone_responsable_trafic,
            'fax_responsable_trafic': self.fax_responsable_trafic,
            'courriel_responsable_trafic': self.courriel_responsable_trafic,
            'etat_description': self.etat_description,
            'deviation': self.deviation,
            'type_occupation': self.type_occupation,
            'voies_condamnees': self.voies_condamnees,
            'type_regulation': self.type_regulation,
            'largeur_gabarit': self.largeur_gabarit,
            'hauteur_gabarit': self.hauteur_gabarit,
            'heure_pointe': self.heure_pointe,
            'week_end': self.week_end,
            'logo_entite': self.logo_entite,
            'nom_entite': self.nom_entite,
            'geometry_point': self.geometry_point,
            'geometry_ligne': self.geometry_ligne,
            'geometry_deviation': self.geometry_deviation,
            'preavis_contacts': self.preavis_contacts,
            'reperages': self.reperages
        }


#Index('my_index', EvenementEcheance.description, unique=True, mysql_length=255)
