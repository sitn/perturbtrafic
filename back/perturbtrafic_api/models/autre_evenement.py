from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    Text,
    DateTime
)

from .meta import Base


class AutreEvenement(Base):
    __tablename__ = 'autre_evenement'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_evenement = Column(Numeric)
    id_maitre_ouvrage = Column(Numeric)
    id_direction_locale = Column(Numeric)
    id_entrepreneur = Column(Numeric)
    id_responsable_travaux = Column(Numeric)
    cause = Column(Text)
    nom_maitre_ouvrage = Column(Text)
    rue_maitre_ouvrage = Column(Text)
    localite_maitre_ouvrage = Column(Text)
    telephone_maitre_ouvrage = Column(Text)
    fax_maitre_ouvrage = Column(Text)
    courriel_maitre_ouvrage = Column(Text)
    nom_direction_locale = Column(Text)
    prenom_direction_locale = Column(Text)
    mobile_direction_locale = Column(Text)
    telephone_direction_locale = Column(Text)
    fax_direction_locale = Column(Text)
    courriel_direction_locale = Column(Text)
    nom_entrepreneur = Column(Text)
    rue_entrepreneur = Column(Text)
    localite_entrepreneur = Column(Text)
    telephone_entrepreneur = Column(Text)
    fax_entrepreneur = Column(Text)
    courriel_entrepreneur = Column(Text)
    nom_responsable_travaux = Column(Text)
    prenom_responsable_travaux = Column(Text)
    mobile_responsable_travaux = Column(Text)
    telephone_responsable_travaux = Column(Text)
    fax_responsable_travaux = Column(Text)
    courriel_responsable_travaux = Column(Text)
    facturation = Column(Numeric)
    date_debut_valide = Column(DateTime)
    date_fin_valide = Column(DateTime)
    date_maj_valide = Column(DateTime)
    numero_facture = Column(Text)
    date_facture = Column(DateTime)
    reserve_eventuelle = Column(Text)

    def format(self):
        return {
            'id': self.id,
            'id_evenement': self.id_evenement,
            'id_maitre_ouvrage': self.id_maitre_ouvrage,
            'id_direction_locale': self.id_direction_locale,
            'id_entrepreneur': self.id_entrepreneur,
            'id_responsable_travaux': self.id_responsable_travaux,
            'cause': self.cause,
            'nom_maitre_ouvrage': self.nom_maitre_ouvrage,
            'rue_maitre_ouvrage': self.rue_maitre_ouvrage,
            'localite_maitre_ouvrage': self.localite_maitre_ouvrage,
            'telephone_maitre_ouvrage': self.telephone_maitre_ouvrage,
            'fax_maitre_ouvrage': self.fax_maitre_ouvrage,
            'courriel_maitre_ouvrage': self.courriel_maitre_ouvrage,
            'nom_direction_locale': self.nom_direction_locale,
            'prenom_direction_locale': self.prenom_direction_locale,
            'mobile_direction_locale': self.mobile_direction_locale,
            'telephone_direction_locale': self.telephone_direction_locale,
            'fax_direction_locale': self.fax_direction_locale,
            'courriel_direction_locale': self.courriel_direction_locale,
            'nom_entrepreneur': self.nom_entrepreneur,
            'rue_entrepreneur': self.rue_entrepreneur,
            'localite_entrepreneur': self.localite_entrepreneur,
            'telephone_entrepreneur': self.telephone_entrepreneur,
            'fax_entrepreneur': self.fax_entrepreneur,
            'courriel_entrepreneur': self.courriel_entrepreneur,
            'nom_responsable_travaux': self.nom_responsable_travaux,
            'prenom_responsable_travaux': self.prenom_responsable_travaux,
            'mobile_responsable_travaux': self.mobile_responsable_travaux,
            'telephone_responsable_travaux': self.telephone_responsable_travaux,
            'fax_responsable_travaux': self.fax_responsable_travaux,
            'courriel_responsable_travaux': self.courriel_responsable_travaux,
            'facturation': self.facturation,
            'date_debut_valide': self.date_debut_valide if not self.date_debut_valide else self.date_debut_valide.isoformat(),
            'date_fin_valide': self.date_fin_valide if not self.date_fin_valide else self.date_fin_valide.isoformat(),
            'date_maj_valide': self.date_maj_valide if not self.date_maj_valide else self.date_maj_valide.isoformat(),
            'numero_facture': self.numero_facture,
            'date_facture': self.date_facture if not self.date_facture else self.date_facture.isoformat(),
            'reserve_eventuelle': self.reserve_eventuelle
        }
