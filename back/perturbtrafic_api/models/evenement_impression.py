from sqlalchemy import (
    Column,
    Index,
    Integer,
    BigInteger,
    Text,
    DateTime,
    Boolean,
    JSON
)

from .meta import Base


class EvenementImpression(Base):
    __tablename__ = 'evenement_impression'
    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger)
    type_description = Column(Text)
    numero_dossier = Column(Text)
    prevision = Column(Boolean)
    division = Column(Text)
    libelle = Column(Text)
    date_debut = Column(DateTime)
    heure_debut = Column(DateTime)
    date_fin = Column(DateTime)
    heure_fin = Column(DateTime)
    nom_requerant = Column(Text)
    nom_responsable = Column(Text)
    prenom_responsable = Column(Text)
    mobile_responsable = Column(Text)
    localisation = Column(Text)
    nom_maitre_ouvrage = Column(Text)
    nom_direction_locale = Column(Text)
    prenom_direction_locale = Column(Text)
    mobile_direction_locale = Column(Text)
    nom_entrepreneur = Column(Text)
    nom_responsable_travaux = Column(Text)
    prenom_responsable_travaux = Column(Text)
    mobile_responsable_travaux = Column(Text)
    date_facture = Column(DateTime)
    date_demande = Column(DateTime)
    nom_entite = Column(Text)
    geometry_point = Column(JSON)
    geometry_ligne = Column(JSON)
    geometry_polygone = Column(JSON)

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'type_description': self.type_description,
            'numero_dossier': self.numero_dossier,
            'prevision': self.prevision,
            'division': self.division,
            'libelle': self.libelle,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'heure_debut': self.heure_debut if not self.heure_debut else self.heure_debut.isoformat(),
            'date_fin': self.date_fin if not self.date_fin else self.date_fin.isoformat(),
            'heure_fin': self.heure_fin if not self.heure_fin else self.heure_fin.isoformat(),
            'nom_requerant': self.nom_requerant,
            'nom_responsable': self.nom_responsable,
            'prenom_responsable': self.prenom_responsable,
            'mobile_responsable': self.mobile_responsable,
            'localisation': self.localisation,
            'nom_maitre_ouvrage': self.nom_maitre_ouvrage,
            'nom_direction_locale': self.nom_direction_locale,
            'prenom_direction_locale': self.prenom_direction_locale,
            'mobile_direction_locale': self.mobile_direction_locale,
            'nom_entrepreneur': self.nom_entrepreneur,
            'nom_responsable_travaux': self.nom_responsable_travaux,
            'prenom_responsable_travaux': self.prenom_responsable_travaux,
            'mobile_responsable_travaux': self.mobile_responsable_travaux,
            'date_facture': self.date_facture if not self.date_facture else self.date_facture.isoformat(),
            'date_demande': self.date_demande if not self.date_demande else self.date_demande.isoformat(),
            'nom_entite': self.nom_entite,
            'geometry_point': self.geometry_point,
            'geometry_ligne': self.geometry_ligne,
            'geometry_polygone': self.geometry_polygone
        }


#Index('my_index', EvenementEcheance.description, unique=True, mysql_length=255)
