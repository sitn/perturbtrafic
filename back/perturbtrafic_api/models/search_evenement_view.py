from sqlalchemy import (
    Column,
    Index,
    Numeric,
    Text,
    Boolean,
    DateTime,
    Integer,
    BigInteger
)

from .meta import Base


class SearchEvenementView(Base):
    __tablename__ = 'recherche_evenement'

    id = Column(BigInteger, primary_key=True)
    id_entite = Column(BigInteger)
    numero_dossier = Column(Text)
    localisation = Column(Text)
    description = Column(Text)
    type = Column(Numeric)
    description_type = Column(Text)
    prevision = Column(Boolean)
    libelle = Column(Text)
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    division = Column(Text)
    id_requerant = Column(Numeric)
    nom_requerant = Column(Text)
    id_responsable = Column(Numeric)
    nom_responsable = Column(Text)
    axe = Column(Text)
    pr_debut = Column(Text)
    pr_debut_seg_seq = Column(Integer)
    pr_debut_sec_seq = Column(Integer)
    pr_fin = Column(Text)
    pr_fin_seg_seq = Column(Integer)
    pr_fin_sec_seq = Column(Integer)
    id_utilisateur_ajout = Column(Numeric)
    nom_utilisateur_ajout = Column(Text)
    localisation_impression = Column(Text)
    pr_touches = Column(Boolean)
    compteur_touche = Column(Boolean)
    id_utilisateur = Column(Numeric)
    modification_autorise = Column(Boolean)
    suppression_autorise = Column(Boolean)

    def format(self):
        return {
            'id': self.id,
            'id_entite': self.id_entite,
            'numero_dossier': self.numero_dossier,
            'localisation': self.localisation,
            'description': self.description,
            'type': self.type,
            'description_type': self.description_type,
            'prevision': self.prevision,
            'libelle': self.libelle,
            'date_debut': self.date_debut if not self.date_debut else self.date_debut.isoformat(),
            'date_fin': self.date_fin if not self.date_fin else self.date_fin.isoformat(),
            'division': self.division,
            'id_requerant': self.id_requerant,
            'nom_requerant': self.nom_requerant,
            'id_responsable': self.id_responsable,
            'nom_responsable': self.nom_responsable,
            'axe': self.axe,
            'pr_debut': self.pr_debut,
            'pr_debut_seg_seq': self.pr_debut_seg_seq,
            'pr_debut_sec_seq': self.pr_debut_sec_seq,
            'pr_fin': self.pr_fin,
            'pr_fin_seg_seq': self.pr_fin_seg_seq,
            'pr_fin_sec_seq': self.pr_fin_sec_seq,
            'id_utilisateur_ajout': self.id_utilisateur_ajout,
            'nom_utilisateur_ajout': self.nom_utilisateur_ajout,
            'localisation_impression': self.localisation_impression,
            'pr_touches': self.pr_touches,
            'compteur_touche': self.compteur_touche,
            'modification_autorise': self.modification_autorise,
            'suppression_autorise': self.suppression_autorise
        }

#Index('my_index', SearchEvenementView.libelle, unique=True, mysql_length=255)
