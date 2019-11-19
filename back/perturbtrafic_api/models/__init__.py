from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy
from pyramid_mailer.mailer import Mailer

# import or define all models here to ensure they are attached to the
# Base.metadata prior to any initialization routines
from .type_evenement import TypeEvenement
from .type_perturbation import TypePerturbation
from .perturbation import Perturbation
from .etat_perturbation import EtatPerturbation
from .destinataire_facturation import DestinataireFacturation
from .categorie_chantier import CategorieChantier
from .type_reperage import TypeReperage
from .contact import Contact
from .organisme import Organisme
from .evenement import Evenement
from .search_evenement_view import SearchEvenementView
from .search_perturbation_view import SearchPerturbationView
from .chantier import Chantier
from .manifestation import Manifestation
from .fouille import Fouille
from .autre_evenement import AutreEvenement
from .fermeture import Fermeture
from .occupation import Occupation
from .evenement_point import EvenementPoint
from .evenement_ligne import EvenementLigne
from .evenement_polygone import EvenementPolygone
from .perturbation_point import PerturbationPoint
from .perturbation_ligne import PerturbationLigne
from .evenement_echeance import EvenementEcheance
from .evenement_impression import EvenementImpression
from .perturbation_impression import PerturbationImpression
from .lien_chantier_categorie_chantier import LienChantierCategorieChantier
from .lien_fouille_plan_type import LienFouillePlanType
from .reperage import Reperage
from .contact_potentiel_avis_perturbation import ContactPotentielAvisPerturbation
from .contact_avis_fermeture_urgence import ContactAvisFermetureUrgence
from .avis_perturbation import AvisPerturbation
from .plan_type_fouille import PlanTypeFouille
from .lien_contact_entite import LienContactEntite
from .entite import Entite
from .localite import Localite
from .evenement_pour_utilisateur_lecture import EvenementPourUtilisateurLecture
from .evenement_pour_utilisateur_modification import EvenementPourUtilisateurModification
from .evenement_pour_utilisateur_suppression import EvenementPourUtilisateurSuppression
from .perturbation_pour_utilisateur_ajout import PerturbationPourUtilisateurAjout
from .perturbation_pour_utilisateur_lecture import PerturbationPourUtilisateurLecture
from .perturbation_pour_utilisateur_modification import PerturbationPourUtilisateurModification
from .perturbation_pour_utilisateur_suppression import PerturbationPourUtilisateurSuppression
from .perturbation_pour_utilisateur_modification_etat import PerturbationPourUtilisateurModificationEtat
from .deviation import Deviation
from .delegation import Delegation
from .fonction_contact import FonctionContact
from .autorisation_fonction import AutorisationFonction
from .contact_avis_pr_touche import ContactAvisPrTouche
from .historique_etat_perturbation import HistoriqueEtatPerturbation
from .axe import Axe
from .secteur import Secteur
from .suggestion import Suggestion

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """
    Get a ``sqlalchemy.orm.Session`` instance backed by a transaction.

    This function will hook the session to the transaction manager which
    will take care of committing any changes.

    - When using pyramid_tm it will automatically be committed or aborted
      depending on whether an exception is raised.

    - When using scripts you should wrap the session in a manager yourself.
      For example::

          import transaction

          engine = get_engine(settings)
          session_factory = get_session_factory(engine)
          with transaction.manager:
              dbsession = get_tm_session(session_factory, transaction.manager)

    """
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('perturbtrafic_api.models')``.

    """
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    # use pyramid_retry to retry a request when transient exceptions occur
    config.include('pyramid_retry')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    # Include pyramid mail
    config.registry['mailer'] = Mailer.from_settings(settings)

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )
