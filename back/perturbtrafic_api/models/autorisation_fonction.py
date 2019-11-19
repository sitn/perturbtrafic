from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
    Boolean
)

from .meta import Base


class AutorisationFonction(Base):
    __tablename__ = 'autorisation_fonction'
    #id = Column(BigInteger, primary_key=True)
    id_utilisateur = Column(BigInteger, primary_key=True)
    ajouter_evenement = Column(Boolean)
    ajouter_perturbation = Column(Boolean)
    modifier_etat_perturbation_creation = Column(Boolean)
    gerer_contacts = Column(Boolean)
    gerer_organismes = Column(Boolean)
    gerer_contacts_preavis = Column(Boolean)
    gerer_contacts_avis_urgences = Column(Boolean)
    gerer_contacts_srb = Column(Boolean)
    gerer_utilisateurs = Column(Boolean)
    peut_deleguer = Column(Boolean)

    def format(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'ajouter_evenement': self.ajouter_evenement,
            'ajouter_perturbation': self.ajouter_perturbation,
            'modifier_etat_perturbation_creation': self.modifier_etat_perturbation_creation,
            'gerer_contacts': self.gerer_contacts,
            'gerer_organismes': self.gerer_organismes,
            'gerer_contacts_preavis': self.gerer_contacts_preavis,
            'gerer_contacts_avis_urgences': self.gerer_contacts_avis_urgences,
            'gerer_contacts_srb': self.gerer_contacts_srb,
            'gerer_utilisateurs': self.gerer_utilisateurs,
            'peut_deleguer': self.peut_deleguer
        }

#Index('my_index', AutorisationFonction.nom, unique=True, mysql_length=255)
