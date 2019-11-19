from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Boolean,
    DateTime,
    func
)

from .meta import Base


class Evenement(Base):
    __tablename__ = 'evenement'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_entite = Column(BigInteger)
    id_responsable = Column(BigInteger)
    id_requerant = Column(BigInteger)
    type = Column(BigInteger)
    numero_dossier = Column(Text)
    division = Column(Text)
    libelle = Column(Text)
    description = Column(Text)
    prevision = Column(Boolean)
    #urgence = Column(Boolean)
    date_debut = Column(DateTime)
    heure_debut = Column(DateTime)
    date_fin = Column(DateTime)
    heure_fin = Column(DateTime)
    localisation = Column(Text)
    #localite = Column(Text)
    #lieu_dit = Column(Text)
    #reperage_effectif = Column(Boolean)
    nom_requerant = Column(Text)
    rue_requerant = Column(Text)
    localite_requerant = Column(Text)
    telephone_requerant = Column(Text)
    fax_requerant = Column(Text)
    courriel_requerant = Column(Text)
    nom_contact = Column(Text)
    prenom_contact = Column(Text)
    mobile_contact = Column(Text)
    telephone_contact = Column(Text)
    fax_contact = Column(Text)
    courriel_contact = Column(Text)
    remarque = Column(Text)
    date_demande = Column(DateTime)
    date_octroi = Column(DateTime)
    id_utilisateur_ajout = Column(BigInteger)
    date_ajout = Column(DateTime, default=func.now())
    id_utilisateur_modification = Column(BigInteger)
    date_modification = Column(DateTime, default=func.now(), onupdate=func.now())
    date_suppression = Column(DateTime)

    def format(self):
        return {
            'id': self.id,
            'id_entite': self.id_entite,
            'id_responsable': self.id_responsable ,
            'id_requerant': self.id_requerant ,
            'type': self.type,
            'numero_dossier': self.numero_dossier,
            'division': self.division,
            'libelle': self.libelle,
            'description': self.description,
            'prevision': self.prevision,
            #'urgence': self.urgence,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'heure_debut': self.heure_debut if not self.heure_debut else self.heure_debut.isoformat(),
            'date_fin': self.date_fin if not self.date_fin else self.date_fin.isoformat(),
            'heure_fin': self.heure_fin if not self.heure_fin else self.heure_fin.isoformat(),
            'localisation': self.localisation,
            #'localite': self.localite,
            #'lieu_dit': self.lieu_dit,
            #'reperage_effectif': self.reperage_effectif,
            'nom_requerant': self.nom_requerant,
            'rue_requerant': self.rue_requerant,
            'localite_requerant': self.localite_requerant,
            'telephone_requerant': self.telephone_requerant,
            'fax_requerant': self.fax_requerant,
            'courriel_requerant': self.courriel_requerant,
            'nom_contact': self.nom_contact,
            'prenom_contact': self.prenom_contact,
            'mobile_contact': self.mobile_contact,
            'telephone_contact': self.telephone_contact,
            'fax_contact': self.fax_contact,
            'courriel_contact': self.courriel_contact,
            'remarque': self.remarque,
            'date_demande': self.date_demande if not self.date_demande else self.date_demande.isoformat(),
            'date_octroi': self.date_octroi if not self.date_octroi else self.date_octroi.isoformat(),
            'id_utilisateur_ajout': self.id_utilisateur_ajout,
            'date_ajout': self.date_ajout if not self.date_ajout else self.date_ajout.isoformat(),
            'id_utilisateur_modification': self.id_utilisateur_modification,
            'date_modification': self.date_modification if not self.date_modification else self.date_modification.isoformat(),
            'date_suppression': self.date_suppression if not self.date_suppression else self.date_suppression.isoformat()
        }


    def format_simple(self):
        return {
            'id': self.id,
            'libelle': self.libelle,
            'numero_dossier': self.numero_dossier
        }

#Index('my_index', Evenement.libelle, unique=True, mysql_length=255)
