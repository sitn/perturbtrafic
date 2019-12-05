from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy import exc, func
from sqlalchemy import *
from sqlalchemy.schema import Sequence
from .. import models
from ..scripts.wfs_query import WFSQuery
from ..scripts.ldap_query import LDAPQuery
from ..scripts.utils import Utils
from ..scripts.evenements_xml import EvenementXML
from ..scripts.pt_mailer import PTMailer
from ..exceptions.custom_error import CustomError
from datetime import datetime, date, timedelta
import transaction
import json
import requests
import logging
import datetime
from pyramid.httpexceptions import HTTPFound, HTTPForbidden


log = logging.getLogger(__name__)

general_exception = 'An error occured while executing the query'
id_not_found_exception = 'Id not found'
user_not_found_exception = 'User not found'
not_authorized_exception = 'Not authorized'


########################################################
# Home view
########################################################
@view_config(route_name='home', renderer='../templates/home.jinja2')
@view_config(route_name='home_slash', renderer='../templates/home.jinja2')
def home_view(request):
    return {}


########################################################
# Type evenement by id view
########################################################
@view_config(route_name='type_evenement_by_id', request_method='GET', renderer='json')
def type_evenement_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        query = request.dbsession.query(models.TypeEvenement)
        result = query.filter(models.TypeEvenement.id == id).first()

        if not result:
            raise Exception(id_not_found_exception)



    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Types evenements view
########################################################
@view_config(route_name='types_evenements', request_method='GET', renderer='json')
@view_config(route_name='types_evenements_slash', request_method='GET', renderer='json')
def types_evenements_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        query = request.dbsession.query(models.TypeEvenement).all()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return query


########################################################
# Get evenement by id view
########################################################
@view_config(route_name='evenement_by_id', request_method='GET', renderer='json')
def get_evenement_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        query = request.dbsession.query(models.Evenement)
        result = query.filter(models.Evenement.id == id).first()

        if not result:
            raise Exception(id_not_found_exception)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result.format()


########################################################
# Delete evenement by id view
########################################################
@view_config(route_name='evenement_by_id', request_method='DELETE', renderer='json')
def delete_evenement_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        id = request.matchdict['id']

        # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        # Check if the user has permission to delete evenement
        user_can_delete_evenement = Utils.user_can_delete_evenement(request, current_user_id, id)

        if not user_can_delete_evenement:
            raise HTTPForbidden()


        # Evenement
        query = request.dbsession.query(models.Evenement)
        evenement = query.filter(models.Evenement.id == id).first()


        # Related perturbation
        query_p = request.dbsession.query(models.Perturbation)
        perturbations = query_p.filter(models.Perturbation.id_evenement == id).all()

        if not evenement:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            evenement.date_suppression = func.now()

            for p in perturbations:
                p.date_suppression = func.now()

            # Commit transaction
            transaction.commit()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Evenements view
########################################################
@view_config(route_name='evenements', request_method='GET', renderer='json')
@view_config(route_name='evenements_slash', request_method='GET', renderer='json')
def evenements_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Evenement).all()

        formattedResult = []

        for evenement in query:
            formattedResult.append(evenement.format())


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return formattedResult


########################################################
# Libeles evenements view
########################################################
@view_config(route_name='libelles_evenements', request_method='GET', renderer='json')
@view_config(route_name='libelles_evenements_slash', request_method='GET', renderer='json')
def libelles_evenements_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)

        id_entite = None

        # Read params evenement
        if 'idEntite' in request.params:
            id_entite = request.params['idEntite']


        query = request.dbsession.query(models.PerturbationPourUtilisateurAjout).filter(models.PerturbationPourUtilisateurAjout.id_utilisateur == current_user_id).filter(models.PerturbationPourUtilisateurAjout.id_entite == id_entite).all()



    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return query


########################################################
# Evenement arrivant à échéance view
########################################################
@view_config(route_name='evenements_echeance', request_method='GET', renderer='json')
@view_config(route_name='evenements_echeance_slash', request_method='GET', renderer='json')
def evenements_echeance_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)

        id_entite = None

        # Read params evenement
        if 'idEntite' in request.params:
            id_entite = request.params['idEntite']

        query = request.dbsession.query(models.EvenementEcheance).filter(models.EvenementEcheance.id_utilisateur == current_user_id).filter(models.EvenementEcheance.id_entite == id_entite).all()

        evenements_array = []
        for evenement in query:
            evenements_array.append(evenement.format())

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return evenements_array


########################################################
# Evenement impression by id
########################################################
@view_config(route_name='evenement_impression_by_id', request_method='GET', renderer='json')
def evenement_impression_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']
        query = request.dbsession.query(models.EvenementImpression).filter(models.EvenementImpression.id == id).first()

        if not query:
            raise Exception(id_not_found_exception)

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return query.format()


########################################################
# Evenement_perturbations impression by id
########################################################
@view_config(route_name='evenement_perturbations_impression_by_id', request_method='GET', renderer='json')
def evenement_perturbations_impression_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']
        query_evenement = request.dbsession.query(models.EvenementImpression).filter(models.EvenementImpression.id == id).first()

        if not query_evenement:
            raise Exception(id_not_found_exception)

        # Get perturbations related to the evenement
        perturbations_ids = []
        perturbations_impression = []
        query_perturbations = request.dbsession.query(models.Perturbation).filter(models.Perturbation.id_evenement == id).all()

        for item in query_perturbations:
            perturbations_ids.append(item.id)

        query_perturbations_impression = request.dbsession.query(models.PerturbationImpression).filter(models.PerturbationImpression.id.in_(perturbations_ids)).all()

        if query_perturbations_impression:
            for item in query_perturbations_impression:
                perturbations_impression.append(item.format())

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'evenement': query_evenement.format(), 'perturbations' : perturbations_impression}


########################################################
# Get Evenement edition by id view
########################################################
@view_config(route_name='evenement_edition_by_id', request_method='GET', renderer='json')
def evenement_edition_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        id = request.matchdict['id']

        #Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)

        # Check if the user has permission to add evenement
        user_can_read_evenement = Utils.user_can_read_evenement(request, current_user_id, id)

        if not user_can_read_evenement:
            raise HTTPForbidden()


        related_type = None
        categories_chantiers = []
        plans_types_fouille = []

        # Evenement
        query_evenement = request.dbsession.query(models.Evenement)
        evenement = query_evenement.filter(models.Evenement.id == id).first()

        # Utilisateur ajout
        contact_utilisateur_ajout = request.dbsession.query(models.Contact).filter(
            models.Contact.id == evenement.id_utilisateur_ajout).first()

        # Utilisateur modification
        contact_utilisateur_modification = request.dbsession.query(models.Contact).filter(
            models.Contact.id == evenement.id_utilisateur_modification).first()

        if not evenement:
            raise Exception(id_not_found_exception)

        # Type evenement : autre
        if evenement.type == int(settings['autre_evenement_id']):
            query = request.dbsession.query(models.AutreEvenement)
            related_type = query.filter(models.AutreEvenement.id_evenement == id).first()

        # Type evenement : Chantier
        elif evenement.type == int(settings['chantier_evenement_id']):
            query = request.dbsession.query(models.Chantier)
            related_type = query.filter(models.Chantier.id_evenement == id).first()

            # Categories chatier
            for lcc, cc in request.dbsession.query(models.LienChantierCategorieChantier,
                                                   models.CategorieChantier).filter(
                    models.LienChantierCategorieChantier.id_chantier == related_type.id).filter(
                    models.CategorieChantier.id == models.LienChantierCategorieChantier.categorie).all():
                categories_chantiers.append(cc)


        # Type evenement : Fouille
        elif evenement.type == int(settings['fouille_evenement_id']):
            query = request.dbsession.query(models.Fouille)
            related_type = query.filter(models.Fouille.id_evenement == id).first()

            #Plan type
            for lfp, pf in request.dbsession.query(models.LienFouillePlanType,
                                                   models.PlanTypeFouille).filter(
                    models.LienFouillePlanType.id_evenement == id).filter(
                    models.PlanTypeFouille.id == models.LienFouillePlanType.id_plan_type).all():
                plans_types_fouille.append(pf)

        # Type evenement : Manifestation
        elif evenement.type == int(settings['manifestation_evenement_id']):
            query = request.dbsession.query(models.Manifestation)
            related_type = query.filter(models.Manifestation.id_evenement == id).first()

        # Geometries
        geometries_array = []
        query_geom_point = request.dbsession.query(models.EvenementPoint.id,
                                                   func.public.ST_AsGeoJSON(models.EvenementPoint.geometry).label(
                                                       "geometry")).filter(
            models.EvenementPoint.id_evenement == id).all()

        query_geom_ligne = request.dbsession.query(models.EvenementLigne.id,
                                                   func.public.ST_AsGeoJSON(models.EvenementLigne.geometry).label(
                                                       "geometry")).filter(
            models.EvenementLigne.id_evenement == id).all()

        query_geom_polygone = request.dbsession.query(models.EvenementPolygone.id,
                                                      func.public.ST_AsGeoJSON(models.EvenementPolygone.geometry).label(
                                                          "geometry")).filter(
            models.EvenementPolygone.id_evenement == id).all()

        for item in query_geom_point + query_geom_ligne + query_geom_polygone:
            geometries_array.append({'id': item.id, 'geometry': item.geometry})

        # Reperage
        reperages = []
        evenement_lignes_ids = []

        for item in query_geom_ligne:
            evenement_lignes_ids.append(item.id)

        if len(evenement_lignes_ids) > 0:
            query_reperage = request.dbsession.query(models.Reperage).filter(
                models.Reperage.id_evenement_ligne.in_(evenement_lignes_ids)).all()

            if query_reperage:
                for item in query_reperage:
                    reperages.append(item.format())

        # Format evenement
        evenement = evenement.format()

        if contact_utilisateur_ajout:
            evenement[
                'nom_utilisateur_ajout'] = contact_utilisateur_ajout.prenom + ' ' + contact_utilisateur_ajout.nom

        if contact_utilisateur_modification:
            evenement[
                'nom_utilisateur_modification'] = contact_utilisateur_modification.prenom + ' ' + contact_utilisateur_modification.nom

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'evenement': evenement, 'reperages': reperages,
            'infos': {} if not related_type else related_type.format(), 'categories_chantiers': categories_chantiers, 'plans_types_fouille': plans_types_fouille, 'geometries': geometries_array}


########################################################
# Add Evenement edition
########################################################
@view_config(route_name='evenement_edition', request_method='POST', renderer='json')
@view_config(route_name='evenement_edition_slash', request_method='POST', renderer='json')
def add_evenement_edition(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        # Check if the user has permission to add evenement
        user_can_add_evenement = Utils.user_can_add_evenement(request, current_user_id)

        if not user_can_add_evenement:
            raise HTTPForbidden()

        max_event_id = None
        categories_array = []
        plan_types_array = []

        # Default params value

        """Evenement"""
        idEntite = None
        idResponsable = None
        idRequerant = None
        type = None
        numeroDossier = None
        division = None
        libelle = None
        description = None
        prevision = None
        #urgence = None
        dateDebut = None
        heureDebut = None
        dateFin = None
        heureFin = None
        localisation = None
        # localite = None
        # lieuDit = None
        # reperageEffectif = None
        nomRequerant = None
        rueRequerant = None
        localiteRequerant = None
        telephoneRequerant = None
        faxRequerant = None
        courrielRequerant = None
        nomContact = None
        prenomContact = None
        mobileContact = None
        telephoneContact = None
        faxContact = None
        courrielContact = None
        remarque = None
        dateDemande = None
        dateOctroi = None
        #ajoutePar = None
        # dateAjout = None
        # modifiePar = None
        # dateModification = None
        # dateSuppression = None

        # Geometries reperages
        geometries_reperages = None

        """Autre evenement"""
        _idMaitreOuvrage = None
        _idDirectionLocale = None
        _idEntrepreneur = None
        _idResponsableTravaux = None
        _cause = None
        _nomMaitreOuvrage = None
        _rueMaitreOuvrage = None
        _localiteMaitreOuvrage = None
        _telephoneMaitreOuvrage = None
        _faxMaitreOuvrage = None
        _courrielMaitreOuvrage = None
        _nomDirectionLocale = None
        _prenomDirectionLocale = None
        _mobileDirectionLocale = None
        _telephoneDirectionLocale = None
        _faxDirectionLocale = None
        _courrielDirectionLocale = None
        _nomEntrepreneur = None
        _rueEntrepreneur = None
        _localiteEntrepreneur = None
        _telephoneEntrepreneur = None
        _faxEntrepreneur = None
        _courrielEntrepreneur = None
        _nomResponsableTravaux = None
        _prenomResponsableTravaux = None
        _mobileResponsableTravaux = None
        _telephoneResponsableTravaux = None
        _faxResponsableTravaux = None
        _courrielResponsableTravaux = None
        _facturation = None
        # _coordonnesX = None
        # _coordonnesY = None
        # _commune = None
        # _cadastre = None
        # _bienFonds = None
        # _autre_cadastre = None
        # _autre_bienFonds = None
        # _lieuDit = None
        _dateDebutValide = None
        _dateFinValide = None
        _dateMajValide = None
        _numeroFacture = None
        _dateFacture = None
        _reserveEventuelle = None

        """Chantier"""
        _idMaitreOuvrage = None
        _idDirectionLocale = None
        _idEntrepreneur = None
        _idResponsableTravaux = None
        _projet = None
        _longueurEtape = None
        _surface = None
        _idCentraleEnrobage = None
        _epaisseurCaisson = None
        _qualiteCaisson = None
        _epaisseurSupport = None
        _qualiteSupport = None
        _epaisseurRevetement = None
        _qualiteRevetement = None
        _qualiteEncollage = None
        _boucleInduction = None
        _faucherAccotement = None
        _curerDepotoirs = None
        _nettoyer_bords = None
        _colmater_fissure = None
        _prTouches = None
        _autre = None
        _lieuSeance = None
        _jourSeance = None
        _heureSeance = None
        _categories = None
        _reperageEffectif = None

        """Fouille"""
        _idMaitreOuvrage = None
        _idDirectionLocale = None
        _idEntrepreneur = None
        _idResponsableTravaux = None
        _nomMaitreOuvrage = None
        _rueMaitreOuvrage = None
        _localiteMaitreOuvrage = None
        _telephoneMaitreOuvrage = None
        _faxMaitreOuvrage = None
        _courrielMaitreOuvrage = None
        _nomDirectionLocale = None
        _prenomDirectionLocale = None
        _mobileDirectionLocale = None
        _telephoneDirectionLocale = None
        _faxDirectionLocale = None
        _courrielDirectionLocale = None
        _nomEntrepreneur = None
        _rueEntrepreneur = None
        _localiteEntrepreneur = None
        _telephoneEntrepreneur = None
        _faxEntrepreneur = None
        _courrielEntrepreneur = None
        _nomResponsableTravaux = None
        _prenomResponsableTravaux = None
        _mobileResponsableTravaux = None
        _telephoneResponsableTravaux = None
        _faxResponsableTravaux = None
        _courrielResponsableTravaux = None
        _facturation = None
        '''
        _coordonnesX = None
        _coordonnesY = None
        _commune = None
        _cadastre = None
        _bienFonds = None
        _autreCadastre = None
        _autreBienFonds = None
        _lieuDit = None
        '''
        _prTouches = None
        _longueurEtape = None
        _epaisseurCaisson = None
        _qualiteCaisson = None
        _epaisseurSupport = None
        _qualiteSupport = None
        _epaisseurRevetement = None
        _qualiteRevetement = None
        _qualiteEncollage = None
        _dateDebutValide = None
        _dateFinValide = None
        _dateMajValide = None
        _numeroFacture = None
        _dateFacture = None
        _reserveEventuelle = None
        _planTypes = None
        _reperageEffectif = None

        """Manifestation"""
        _parcours = None

        # Read params evenement
        if 'idEntite' in request.params:
            idEntite = request.params['idEntite']

        if 'idResponsable' in request.params:
            idResponsable = request.params['idResponsable']

        if 'idRequerant' in request.params:
            idRequerant = request.params['idRequerant']

        if 'type' in request.params:
            type = request.params['type']
            numeroDossier = Utils.generate_numero_dossier(request, type)

        if 'division' in request.params:
            division = request.params['division']

        if 'libelle' in request.params:
            libelle = request.params['libelle']

        if 'description' in request.params:
            description = request.params['description']

        if 'prevision' in request.params:
            prevision = request.params['prevision']

            if prevision == 'true':
                prevision = True
            elif prevision == 'false':
                prevision = False
            else:
                prevision = None

        """
        if 'urgence' in request.params:
            urgence = request.params['urgence']

            if urgence == 'true':
                urgence = True
            elif urgence == 'false':
                urgence = False
            else:
                urgence = None
        """

        if 'dateDebut' in request.params:
            dateDebut = request.params['dateDebut']

        if 'heureDebut' in request.params:
            heureDebut = request.params['heureDebut']

        if 'dateFin' in request.params:
            dateFin = request.params['dateFin']

        if 'heureFin' in request.params:
            heureFin = request.params['heureFin']

        if 'localisation' in request.params:
            localisation = request.params['localisation']

        '''
        if 'localite' in request.params:
            localite = request.params['localite']

        if 'lieuDit' in request.params:
            lieuDit = request.params['lieuDit']

        if 'reperageEffectif' in request.params:
            reperageEffectif = request.params['reperageEffectif']

            if reperageEffectif == 'true':
                reperageEffectif = True
            elif reperageEffectif == 'false':
                reperageEffectif = False
            else:
                reperageEffectif = None
        '''

        if 'nomRequerant' in request.params:
            nomRequerant = request.params['nomRequerant']

        if 'rueRequerant' in request.params:
            rueRequerant = request.params['rueRequerant']

        if 'localiteRequerant' in request.params:
            localiteRequerant = request.params['localiteRequerant']

        if 'telephoneRequerant' in request.params:
            telephoneRequerant = request.params['telephoneRequerant']

        if 'faxRequerant' in request.params:
            faxRequerant = request.params['faxRequerant']

        if 'courrielRequerant' in request.params:
            courrielRequerant = request.params['courrielRequerant']

        if 'nomContact' in request.params:
            nomContact = request.params['nomContact']

        if 'prenomContact' in request.params:
            prenomContact = request.params['prenomContact']

        if 'mobileContact' in request.params:
            mobileContact = request.params['mobileContact']

        if 'telephoneContact' in request.params:
            telephoneContact = request.params['telephoneContact']

        if 'faxContact' in request.params:
            faxContact = request.params['faxContact']

        if 'courrielContact' in request.params:
            courrielContact = request.params['courrielContact']

        if 'remarque' in request.params:
            remarque = request.params['remarque']

        if 'dateDemande' in request.params:
            dateDemande = request.params['dateDemande']

        if 'dateOctroi' in request.params:
            dateOctroi = request.params['dateOctroi']

        """
        if 'ajoutePar' in request.params:
            ajoutePar = request.params['ajoutePar']

        
        if 'dateAjout' in request.params:
            dateAjout = request.params['dateAjout']

        if 'modifiePar' in request.params:
            modifiePar = request.params['modifiePar']

        if 'dateModification' in request.params:
            dateModification = request.params['dateModification']

        if 'dateSuppression' in request.params:
            dateSuppression = request.params['dateSuppression']
        """

        # Check date_debut, if less than 24h, urgence=true
        """
        if not urgence and dateDebut != None and heureDebut != None:
            date_time_str = str(dateDebut) + ' ' + str(heureDebut)
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()

            if date_time_obj >= now and date_time_obj <= now + timedelta(days=1):
                urgence = True
        """

        # Geometries_reperages
        if 'geometries_reperages' in request.params:
            geometries_reperages = request.params['geometries_reperages']

        # Read params autre evenement
        if '_idMaitreOuvrage' in request.params:
            _idMaitreOuvrage = request.params['_idMaitreOuvrage']

        if '_idDirectionLocale' in request.params:
            _idDirectionLocale = request.params['_idDirectionLocale']

        if '_idEntrepreneur' in request.params:
            _idEntrepreneur = request.params['_idEntrepreneur']

        if '_idResponsableTravaux' in request.params:
            _idResponsableTravaux = request.params['_idResponsableTravaux']

        if '_cause' in request.params:
            _cause = request.params['_cause']

        if '_nomMaitreOuvrage' in request.params:
            _nomMaitreOuvrage = request.params['_nomMaitreOuvrage']

        if '_rueMaitreOuvrage' in request.params:
            _rueMaitreOuvrage = request.params['_rueMaitreOuvrage']

        if '_localiteMaitreOuvrage' in request.params:
            _localiteMaitreOuvrage = request.params['_localiteMaitreOuvrage']

        if '_telephoneMaitreOuvrage' in request.params:
            _telephoneMaitreOuvrage = request.params['_telephoneMaitreOuvrage']

        if '_faxMaitreOuvrage' in request.params:
            _faxMaitreOuvrage = request.params['_faxMaitreOuvrage']

        if '_courrielMaitreOuvrage' in request.params:
            _courrielMaitreOuvrage = request.params['_courrielMaitreOuvrage']

        if '_nomDirectionLocale' in request.params:
            _nomDirectionLocale = request.params['_nomDirectionLocale']

        if '_prenomDirectionLocale' in request.params:
            _prenomDirectionLocale = request.params['_prenomDirectionLocale']

        if '_mobileDirectionLocale' in request.params:
            _mobileDirectionLocale = request.params['_mobileDirectionLocale']

        if '_telephoneDirectionLocale' in request.params:
            _telephoneDirectionLocale = request.params['_telephoneDirectionLocale']

        if '_faxDirectionLocale' in request.params:
            _faxDirectionLocale = request.params['_faxDirectionLocale']

        if '_courrielDirectionLocale' in request.params:
            _courrielDirectionLocale = request.params['_courrielDirectionLocale']

        if '_nomEntrepreneur' in request.params:
            _nomEntrepreneur = request.params['_nomEntrepreneur']

        if '_rueEntrepreneur' in request.params:
            _rueEntrepreneur = request.params['_rueEntrepreneur']

        if '_localiteEntrepreneur' in request.params:
            _localiteEntrepreneur = request.params['_localiteEntrepreneur']

        if '_telephoneEntrepreneur' in request.params:
            _telephoneEntrepreneur = request.params['_telephoneEntrepreneur']

        if '_faxEntrepreneur' in request.params:
            _faxEntrepreneur = request.params['_faxEntrepreneur']

        if '_courrielEntrepreneur' in request.params:
            _courrielEntrepreneur = request.params['_courrielEntrepreneur']

        if '_nomResponsableTravaux' in request.params:
            _nomResponsableTravaux = request.params['_nomResponsableTravaux']

        if '_prenomResponsableTravaux' in request.params:
            _prenomResponsableTravaux = request.params['_prenomResponsableTravaux']

        if '_mobileResponsableTravaux' in request.params:
            _mobileResponsableTravaux = request.params['_mobileResponsableTravaux']

        if '_telephoneResponsableTravaux' in request.params:
            _telephoneResponsableTravaux = request.params['_telephoneResponsableTravaux']

        if '_faxResponsableTravaux' in request.params:
            _faxResponsableTravaux = request.params['_faxResponsableTravaux']

        if '_courrielResponsableTravaux' in request.params:
            _courrielResponsableTravaux = request.params['_courrielResponsableTravaux']

        if '_facturation' in request.params:
            _facturation = request.params['_facturation']
        '''
        if '_coordonnesX' in request.params:
            _coordonnesX = request.params['_coordonnesX']

        if '_coordonnesY' in request.params:
            _coordonnesY = request.params['_coordonnesY']

        if '_commune' in request.params:
            _commune = request.params['_commune']

        if '_cadastre' in request.params:
            _cadastre = request.params['_cadastre']

        if '_bienFonds' in request.params:
            _bienFonds = request.params['_bienFonds']

        if '_autre_cadastre' in request.params:
            _autre_cadastre = request.params['_autre_cadastre']

        if '_autre_bienFonds' in request.params:
            _autre_bienFonds = request.params['_autre_bienFonds']

        if '_lieuDit' in request.params:
            _lieuDit = request.params['_lieuDit']
        '''
        if '_dateDebutValide' in request.params:
            _dateDebutValide = request.params['_dateDebutValide']

        if '_dateFinValide' in request.params:
            _dateFinValide = request.params['_dateFinValide']

        if '_dateMajValide' in request.params:
            _dateMajValide = request.params['_dateMajValide']

        if '_numeroFacture' in request.params:
            _numeroFacture = request.params['_numeroFacture']

        if '_dateFacture' in request.params:
            _dateFacture = request.params['_dateFacture']

        if '_reserveEventuelle' in request.params:
            _reserveEventuelle = request.params['_reserveEventuelle']

        # Read params chantier
        if '_idMaitreOuvrage' in request.params:
            _idMaitreOuvrage = request.params['_idMaitreOuvrage']

        if '_idDirectionLocale' in request.params:
            _idDirectionLocale = request.params['_idDirectionLocale']

        if '_idEntrepreneur' in request.params:
            _idEntrepreneur = request.params['_idEntrepreneur']

        if '_idResponsableTravaux' in request.params:
            _idResponsableTravaux = request.params['_idResponsableTravaux']

        if '_projet' in request.params:
            _projet = request.params['_projet']

        if '_longueurEtape' in request.params:
            _longueurEtape = request.params['_longueurEtape']

        if '_surface' in request.params:
            _surface = request.params['_surface']

        if '_idCentraleEnrobage' in request.params:
            _idCentraleEnrobage = request.params['_idCentraleEnrobage']

        if '_epaisseurCaisson' in request.params:
            _epaisseurCaisson = request.params['_epaisseurCaisson']

        if '_qualiteCaisson' in request.params:
            _qualiteCaisson = request.params['_qualiteCaisson']

        if '_epaisseurSupport' in request.params:
            _epaisseurSupport = request.params['_epaisseurSupport']

        if '_qualiteSupport' in request.params:
            _qualiteSupport = request.params['_qualiteSupport']

        if '_epaisseurRevetement' in request.params:
            _epaisseurRevetement = request.params['_epaisseurRevetement']

        if '_qualiteRevetement' in request.params:
            _qualiteRevetement = request.params['_qualiteRevetement']

        if '_qualiteEncollage' in request.params:
            _qualiteEncollage = request.params['_qualiteEncollage']

        if '_boucleInduction' in request.params:
            _boucleInduction = request.params['_boucleInduction']

            if _boucleInduction == 'true':
                _boucleInduction = True
            elif _boucleInduction == 'false':
                _boucleInduction = False
            else:
                _boucleInduction = None

        if '_faucherAccotement' in request.params:
            _faucherAccotement = request.params['_faucherAccotement']

            if _faucherAccotement == 'true':
                _faucherAccotement = True
            elif _faucherAccotement == 'false':
                _faucherAccotement = False
            else:
                _faucherAccotement = None

        if '_curerDepotoirs' in request.params:
            _curerDepotoirs = request.params['_curerDepotoirs']

            if _curerDepotoirs == 'true':
                _curerDepotoirs = True
            elif _curerDepotoirs == 'false':
                _curerDepotoirs = False
            else:
                _curerDepotoirs = None

        if '_nettoyer_bords' in request.params:
            _nettoyer_bords = request.params['_nettoyer_bords']

            if _nettoyer_bords == 'true':
                _nettoyer_bords = True
            elif _nettoyer_bords == 'false':
                _nettoyer_bords = False
            else:
                _nettoyer_bords = None

        if '_colmater_fissure' in request.params:
            _colmater_fissure = request.params['_colmater_fissure']

            if _colmater_fissure == 'true':
                _colmater_fissure = True
            elif _colmater_fissure == 'false':
                _colmater_fissure = False
            else:
                _colmater_fissure = None

        if '_prTouches' in request.params:
            _prTouches = request.params['_prTouches']

            if _prTouches == 'true':
                _prTouches = True
            elif _prTouches == 'false':
                _prTouches = False
            else:
                _prTouches = None

        if '_autre' in request.params:
            _autre = request.params['_autre']

        if '_lieuSeance' in request.params:
            _lieuSeance = request.params['_lieuSeance']

        if '_jourSeance' in request.params:
            _jourSeance = request.params['_jourSeance']

        if '_heureSeance' in request.params:
            _heureSeance = request.params['_heureSeance']

        if '_categories' in request.params:
            _categories = request.params['_categories']

            if _categories:
                categories_array = json.loads(_categories)

        if '_reperageEffectif' in request.params:
            _reperageEffectif = request.params['_reperageEffectif']

            if _reperageEffectif == 'true':
                _reperageEffectif = True
            elif _reperageEffectif == 'false':
                _reperageEffectif = False
            else:
                _reperageEffectif = None

        # Read params fouille
        if '_idMaitreOuvrage' in request.params:
            _idMaitreOuvrage = request.params['_idMaitreOuvrage']

        if '_idDirectionLocale' in request.params:
            _idDirectionLocale = request.params['_idDirectionLocale']

        if '_idEntrepreneur' in request.params:
            _idEntrepreneur = request.params['_idEntrepreneur']

        if '_idResponsableTravaux' in request.params:
            _idResponsableTravaux = request.params['_idResponsableTravaux']

        if '_nomMaitreOuvrage' in request.params:
            _nomMaitreOuvrage = request.params['_nomMaitreOuvrage']

        if '_rueMaitreOuvrage' in request.params:
            _rueMaitreOuvrage = request.params['_rueMaitreOuvrage']

        if '_localiteMaitreOuvrage' in request.params:
            _localiteMaitreOuvrage = request.params['_localiteMaitreOuvrage']

        if '_telephoneMaitreOuvrage' in request.params:
            _telephoneMaitreOuvrage = request.params['_telephoneMaitreOuvrage']

        if '_faxMaitreOuvrage' in request.params:
            _faxMaitreOuvrage = request.params['_faxMaitreOuvrage']

        if '_courrielMaitreOuvrage' in request.params:
            _courrielMaitreOuvrage = request.params['_courrielMaitreOuvrage']

        if '_nomDirectionLocale' in request.params:
            _nomDirectionLocale = request.params['_nomDirectionLocale']

        if '_prenomDirectionLocale' in request.params:
            _prenomDirectionLocale = request.params['_prenomDirectionLocale']

        if '_mobileDirectionLocale' in request.params:
            _mobileDirectionLocale = request.params['_mobileDirectionLocale']

        if '_telephoneDirectionLocale' in request.params:
            _telephoneDirectionLocale = request.params['_telephoneDirectionLocale']

        if '_faxDirectionLocale' in request.params:
            _faxDirectionLocale = request.params['_faxDirectionLocale']

        if '_courrielDirectionLocale' in request.params:
            _courrielDirectionLocale = request.params['_courrielDirectionLocale']

        if '_nomEntrepreneur' in request.params:
            _nomEntrepreneur = request.params['_nomEntrepreneur']

        if '_rueEntrepreneur' in request.params:
            _rueEntrepreneur = request.params['_rueEntrepreneur']

        if '_localiteEntrepreneur' in request.params:
            _localiteEntrepreneur = request.params['_localiteEntrepreneur']

        if '_telephoneEntrepreneur' in request.params:
            _telephoneEntrepreneur = request.params['_telephoneEntrepreneur']

        if '_faxEntrepreneur' in request.params:
            _faxEntrepreneur = request.params['_faxEntrepreneur']

        if '_courrielEntrepreneur' in request.params:
            _courrielEntrepreneur = request.params['_courrielEntrepreneur']

        if '_nomResponsableTravaux' in request.params:
            _nomResponsableTravaux = request.params['_nomResponsableTravaux']

        if '_prenomResponsableTravaux' in request.params:
            _prenomResponsableTravaux = request.params['_prenomResponsableTravaux']

        if '_mobileResponsableTravaux' in request.params:
            _mobileResponsableTravaux = request.params['_mobileResponsableTravaux']

        if '_telephoneResponsableTravaux' in request.params:
            _telephoneResponsableTravaux = request.params['_telephoneResponsableTravaux']

        if '_faxResponsableTravaux' in request.params:
            _faxResponsableTravaux = request.params['_faxResponsableTravaux']

        if '_courrielResponsableTravaux' in request.params:
            _courrielResponsableTravaux = request.params['_courrielResponsableTravaux']

        if '_facturation' in request.params:
            _facturation = request.params['_facturation']

        if '_coordonnesX' in request.params:
            _coordonnesX = request.params['_coordonnesX']

        if '_coordonnesY' in request.params:
            _coordonnesY = request.params['_coordonnesY']

        if '_commune' in request.params:
            _commune = request.params['_commune']

        if '_cadastre' in request.params:
            _cadastre = request.params['_cadastre']

        if '_bienFonds' in request.params:
            _bienFonds = request.params['_bienFonds']

        if '_autreCadastre' in request.params:
            _autreCadastre = request.params['_autreCadastre']

        if '_autreBienFonds' in request.params:
            _autreBienFonds = request.params['_autreBienFonds']

        if '_lieuDit' in request.params:
            _lieuDit = request.params['_lieuDit']

        if '_prTouches' in request.params:
            _prTouches = request.params['_prTouches']

            if _prTouches == 'true':
                _prTouches = True
            elif _prTouches == 'false':
                _prTouches = False
            else:
                _prTouches = None

        if '_longueurEtape' in request.params:
            _longueurEtape = request.params['_longueurEtape']

        if '_epaisseurCaisson' in request.params:
            _epaisseurCaisson = request.params['_epaisseurCaisson']

        if '_qualiteCaisson' in request.params:
            _qualiteCaisson = request.params['_qualiteCaisson']

        if '_epaisseurSupport' in request.params:
            _epaisseurSupport = request.params['_epaisseurSupport']

        if '_qualiteSupport' in request.params:
            _qualiteSupport = request.params['_qualiteSupport']

        if '_epaisseurRevetement' in request.params:
            _epaisseurRevetement = request.params['_epaisseurRevetement']

        if '_qualiteRevetement' in request.params:
            _qualiteRevetement = request.params['_qualiteRevetement']

        if '_qualiteEncollage' in request.params:
            _qualiteEncollage = request.params['_qualiteEncollage']

        if '_dateDebutValide' in request.params:
            _dateDebutValide = request.params['_dateDebutValide']

        if '_dateFinValide' in request.params:
            _dateFinValide = request.params['_dateFinValide']

        if '_dateMajValide' in request.params:
            _dateMajValide = request.params['_dateMajValide']

        if '_numeroFacture' in request.params:
            _numeroFacture = request.params['_numeroFacture']

        if '_dateFacture' in request.params:
            _dateFacture = request.params['_dateFacture']

        if '_reserveEventuelle' in request.params:
            _reserveEventuelle = request.params['_reserveEventuelle']

        if '_planTypes' in request.params:
            _planTypes = request.params['_planTypes']

            if _planTypes:
                plan_types_array = json.loads(_planTypes)

        if '_reperageEffectif' in request.params:
            _reperageEffectif = request.params['_reperageEffectif']

            if _reperageEffectif == 'true':
                _reperageEffectif = True
            elif _reperageEffectif == 'false':
                _reperageEffectif = False
            else:
                _reperageEffectif = None

        # Read params manifestation
        if '_parcours' in request.params:
            _parcours = request.params['_parcours']

        with transaction.manager:
            evenement_model = models.Evenement(
                id_entite=idEntite,
                id_responsable=idResponsable,
                id_requerant=idRequerant,
                type=type,
                numero_dossier=numeroDossier,
                division=division,
                libelle=libelle,
                description=description,
                prevision=prevision,
                #urgence=urgence,
                date_debut=dateDebut,
                heure_debut=heureDebut,
                date_fin=dateFin,
                heure_fin=heureFin,
                localisation=localisation,
                # localite=localite,
                # lieu_dit=lieuDit,
                # reperage_effectif=reperageEffectif,
                nom_requerant=nomRequerant,
                rue_requerant=rueRequerant,
                localite_requerant=localiteRequerant,
                telephone_requerant=telephoneRequerant,
                fax_requerant=faxRequerant,
                courriel_requerant=courrielRequerant,
                nom_contact=nomContact,
                prenom_contact=prenomContact,
                mobile_contact=mobileContact,
                telephone_contact=telephoneContact,
                fax_contact=faxContact,
                courriel_contact=courrielContact,
                remarque=remarque,
                date_demande=dateDemande,
                date_octroi=dateOctroi,
                id_utilisateur_ajout=current_user_id,
                # date_ajout=dateAjout
                id_utilisateur_modification=current_user_id
                # date_modification=dateModification,
                # date_suppression=dateSuppression
            )

            request.dbsession.add(evenement_model)
            request.dbsession.flush()
            max_event_id = evenement_model.id

            # Related model
            related_model = None
            # evenement_point_model = None
            # evenement_ligne_model = None
            # evenement_polygone_model = None

            # Type evenement : autre
            if int(type) == int(settings['autre_evenement_id']):

                related_model = models.AutreEvenement(
                    id_evenement=max_event_id,
                    id_maitre_ouvrage=_idMaitreOuvrage,
                    id_direction_locale=_idDirectionLocale,
                    id_entrepreneur=_idEntrepreneur,
                    id_responsable_travaux=_idResponsableTravaux,
                    cause=_cause,
                    nom_maitre_ouvrage=_nomMaitreOuvrage,
                    rue_maitre_ouvrage=_rueMaitreOuvrage,
                    localite_maitre_ouvrage=_localiteMaitreOuvrage,
                    telephone_maitre_ouvrage=_telephoneMaitreOuvrage,
                    fax_maitre_ouvrage=_faxMaitreOuvrage,
                    courriel_maitre_ouvrage=_courrielMaitreOuvrage,
                    nom_direction_locale=_nomDirectionLocale,
                    prenom_direction_locale=_prenomDirectionLocale,
                    mobile_direction_locale=_mobileDirectionLocale,
                    telephone_direction_locale=_telephoneDirectionLocale,
                    fax_direction_locale=_faxDirectionLocale,
                    courriel_direction_locale=_courrielDirectionLocale,
                    nom_entrepreneur=_nomEntrepreneur,
                    rue_entrepreneur=_rueEntrepreneur,
                    localite_entrepreneur=_localiteEntrepreneur,
                    telephone_entrepreneur=_telephoneEntrepreneur,
                    fax_entrepreneur=_faxEntrepreneur,
                    courriel_entrepreneur=_courrielEntrepreneur,
                    nom_responsable_travaux=_nomResponsableTravaux,
                    prenom_responsable_travaux=_prenomResponsableTravaux,
                    mobile_responsable_travaux=_mobileResponsableTravaux,
                    telephone_responsable_travaux=_telephoneResponsableTravaux,
                    fax_responsable_travaux=_faxResponsableTravaux,
                    courriel_responsable_travaux=_courrielResponsableTravaux,
                    facturation=_facturation,
                    # coordonnes_x=_coordonnesX,
                    # coordonnes_y=_coordonnesY,
                    # commune=_commune,
                    # cadastre=_cadastre,
                    # bien_fonds=_bienFonds,
                    # autre_cadastre=_autre_cadastre,
                    # autre_bien_fonds=_autre_bienFonds,
                    # lieu_dit=_lieuDit,
                    date_debut_valide=_dateDebutValide,
                    date_fin_valide=_dateFinValide,
                    date_maj_valide=_dateMajValide,
                    numero_facture=_numeroFacture,
                    date_facture=_dateFacture,
                    reserve_eventuelle=_reserveEventuelle
                )

            # Type evenement : Chantier
            elif int(type) == int(settings['chantier_evenement_id']):
                related_model = models.Chantier(
                    id_evenement=max_event_id,
                    id_maitre_ouvrage=_idMaitreOuvrage,
                    id_direction_locale=_idDirectionLocale,
                    id_entrepreneur=_idEntrepreneur,
                    id_responsable_travaux=_idResponsableTravaux,
                    projet=_projet,
                    longueur_etape=_longueurEtape,
                    surface=_surface,
                    id_centrale_enrobage=_idCentraleEnrobage,
                    epaisseur_caisson=_epaisseurCaisson,
                    qualite_caisson=_qualiteCaisson,
                    epaisseur_support=_epaisseurSupport,
                    qualite_support=_qualiteSupport,
                    epaisseur_revetement=_epaisseurRevetement,
                    qualite_revetement=_qualiteRevetement,
                    qualite_encollage=_qualiteEncollage,
                    boucle_induction=_boucleInduction,
                    faucher_accotement=_faucherAccotement,
                    curer_depotoirs=_curerDepotoirs,
                    nettoyer_bords=_nettoyer_bords,
                    colmater_fissure=_colmater_fissure,
                    pr_touches=_prTouches,
                    autre=_autre,
                    lieu_seance=_lieuSeance,
                    jour_seance=_jourSeance,
                    heure_seance=_heureSeance,
                    reperage_effectif=_reperageEffectif
                )

            # Type evenement : Fouille
            elif int(type) == int(settings['fouille_evenement_id']):

                related_model = models.Fouille(
                    id_evenement=max_event_id,
                    id_maitre_ouvrage=_idMaitreOuvrage,
                    id_direction_locale=_idDirectionLocale,
                    id_entrepreneur=_idEntrepreneur,
                    id_responsable_travaux=_idResponsableTravaux,
                    nom_maitre_ouvrage=_nomMaitreOuvrage,
                    rue_maitre_ouvrage=_rueMaitreOuvrage,
                    localite_maitre_ouvrage=_localiteMaitreOuvrage,
                    telephone_maitre_ouvrage=_telephoneMaitreOuvrage,
                    fax_maitre_ouvrage=_faxMaitreOuvrage,
                    courriel_maitre_ouvrage=_courrielMaitreOuvrage,
                    nom_direction_locale=_nomDirectionLocale,
                    prenom_direction_locale=_prenomDirectionLocale,
                    mobile_direction_locale=_mobileDirectionLocale,
                    telephone_direction_locale=_telephoneDirectionLocale,
                    fax_direction_locale=_faxDirectionLocale,
                    courriel_direction_locale=_courrielDirectionLocale,
                    nom_entrepreneur=_nomEntrepreneur,
                    rue_entrepreneur=_rueEntrepreneur,
                    localite_entrepreneur=_localiteEntrepreneur,
                    telephone_entrepreneur=_telephoneEntrepreneur,
                    fax_entrepreneur=_faxEntrepreneur,
                    courriel_entrepreneur=_courrielEntrepreneur,
                    nom_responsable_travaux=_nomResponsableTravaux,
                    prenom_responsable_travaux=_prenomResponsableTravaux,
                    mobile_responsable_travaux=_mobileResponsableTravaux,
                    telephone_responsable_travaux=_telephoneResponsableTravaux,
                    fax_responsable_travaux=_faxResponsableTravaux,
                    courriel_responsable_travaux=_courrielResponsableTravaux,
                    facturation=_facturation,
                    # coordonnes_x=_coordonnesX,
                    # coordonnes_y=_coordonnesY,
                    # commune=_commune,
                    # cadastre=_cadastre,
                    # bien_fonds=_bienFonds,
                    # autre_cadastre=_autreCadastre,
                    # autre_bien_fonds=_autreBienFonds,
                    # lieu_dit=_lieuDit,
                    pr_touches=_prTouches,
                    longueur_etape=_longueurEtape,
                    epaisseur_caisson=_epaisseurCaisson,
                    qualite_caisson=_qualiteCaisson,
                    epaisseur_support=_epaisseurSupport,
                    qualite_support=_qualiteSupport,
                    epaisseur_revetement=_epaisseurRevetement,
                    qualite_revetement=_qualiteRevetement,
                    qualite_encollage=_qualiteEncollage,
                    # plan_type=_planType,
                    date_debut_valide=_dateDebutValide,
                    date_fin_valide=_dateFinValide,
                    date_maj_valide=_dateMajValide,
                    numero_facture=_numeroFacture,
                    date_facture=_dateFacture,
                    reserve_eventuelle=_reserveEventuelle,
                    reperage_effectif=_reperageEffectif
                )

            # Type evenement : Manifestation
            elif int(type) == int(settings['manifestation_evenement_id']):
                related_model = models.Manifestation(
                    id_evenement=max_event_id,
                    parcours=_parcours)

            # Geometries_reperages
            if geometries_reperages != None:
                json_geometries_reperages = json.loads(geometries_reperages)

                for onegeojson in json_geometries_reperages:

                    # Geometry
                    if 'geometry' in onegeojson:
                        geometry = onegeojson['geometry']

                        if 'type' in geometry:
                            type_geom = geometry['type']

                            # Point
                            if type_geom == 'Point':
                                evenement_point_model = models.EvenementPoint(id_evenement=max_event_id)
                                evenement_point_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(evenement_point_model)

                            # Line
                            elif type_geom == 'LineString' or type_geom == 'MultiLineString' or type_geom == 'GeometryCollection':
                                evenement_ligne_model = models.EvenementLigne(id_evenement=max_event_id)
                                evenement_ligne_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(evenement_ligne_model)

                                if 'reperage' in onegeojson:
                                    request.dbsession.flush()

                                    reperage = onegeojson['reperage']
                                    reperage_model = models.Reperage(
                                        id_evenement_ligne=evenement_ligne_model.id,
                                        id_deviation=reperage['idDeviation'],
                                        proprietaire=reperage['proprietaire'],
                                        axe=reperage['axe'],
                                        sens=reperage['sens'],
                                        pr_debut=reperage['prDebut'],
                                        pr_debut_distance=reperage['prDebutDistance'],
                                        pr_fin=reperage['prFin'],
                                        pr_fin_distance=reperage['prFinDistance'],
                                        ecartd=reperage['ecartd'],
                                        ecartf=reperage['ecartf'],
                                        usage_neg=reperage['usageNeg'],
                                        f_surf=reperage['fSurf'],
                                        f_long=reperage['fLong']
                                    )
                                    request.dbsession.add(reperage_model)

                            # Polygon
                            elif type_geom == 'Polygon':
                                evenement_polygon_model = models.EvenementPolygone(id_evenement=max_event_id)
                                evenement_polygon_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(evenement_polygon_model)

            # Commit transaction
            request.dbsession.add(related_model)
            request.dbsession.flush()

        # Reperage

        # Categories chantiers / plan type fouille
        #with transaction.manager:
            # Type evenement : Chantier
            if int(type) == int(settings['chantier_evenement_id']):
                if categories_array and len(categories_array) > 0:
                    for category_id in categories_array:
                        lien_categ_chant = models.LienChantierCategorieChantier(
                            id_chantier=related_model.id,
                            categorie=category_id
                        )
                        request.dbsession.add(lien_categ_chant)


            # Type evenement : Fouille
            elif int(type) == int(settings['fouille_evenement_id']):
                if plan_types_array and len(plan_types_array) > 0:
                    for plan_type_id in plan_types_array:
                        lien_fouille_plan = models.LienFouillePlanType(
                            id_evenement=max_event_id,
                            id_plan_type=plan_type_id
                        )
                        request.dbsession.add(lien_fouille_plan)

            #Commit transaction
            transaction.commit()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        # transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'id': max_event_id, 'message': 'Data successfully saved'}


########################################################
# Update Evenement edition
########################################################
@view_config(route_name='evenement_edition', request_method='PUT', renderer='json')
@view_config(route_name='evenement_edition_slash', request_method='PUT', renderer='json')
def update_evenement_edition(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

         # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id is None:
            raise HTTPForbidden()

        plan_types_array = []
        categories_array = []

        # Default params value

        """Evenement"""
        idEvenement = None
        idEntite = None
        idResponsable = None
        idRequerant = None
        type = None
        numeroDossier = None
        division = None
        libelle = None
        description = None
        prevision = None
        #urgence = None
        dateDebut = None
        heureDebut = None
        dateFin = None
        heureFin = None
        localisation = None
        # localite = None
        # lieuDit = None
        # reperageEffectif = None
        nomRequerant = None
        rueRequerant = None
        localiteRequerant = None
        telephoneRequerant = None
        faxRequerant = None
        courrielRequerant = None
        nomContact = None
        prenomContact = None
        mobileContact = None
        telephoneContact = None
        faxContact = None
        courrielContact = None
        remarque = None
        dateDemande = None
        dateOctroi = None
        # ajoutePar = None
        # dateAjout = None
        #modifiePar = None
        # dateModification = None
        # dateSuppression = None
        geometries_reperages = None

        """Autre evenement"""
        _idMaitreOuvrage = None
        _idDirectionLocale = None
        _idEntrepreneur = None
        _idResponsableTravaux = None
        _cause = None
        _nomMaitreOuvrage = None
        _rueMaitreOuvrage = None
        _localiteMaitreOuvrage = None
        _telephoneMaitreOuvrage = None
        _faxMaitreOuvrage = None
        _courrielMaitreOuvrage = None
        _nomDirectionLocale = None
        _prenomDirectionLocale = None
        _mobileDirectionLocale = None
        _telephoneDirectionLocale = None
        _faxDirectionLocale = None
        _courrielDirectionLocale = None
        _nomEntrepreneur = None
        _rueEntrepreneur = None
        _localiteEntrepreneur = None
        _telephoneEntrepreneur = None
        _faxEntrepreneur = None
        _courrielEntrepreneur = None
        _nomResponsableTravaux = None
        _prenomResponsableTravaux = None
        _mobileResponsableTravaux = None
        _telephoneResponsableTravaux = None
        _faxResponsableTravaux = None
        _courrielResponsableTravaux = None
        _facturation = None
        '''
        _coordonnesX = None
        _coordonnesY = None
        _commune = None
        _cadastre = None
        _bienFonds = None
        _autre_cadastre = None
        _autre_bienFonds = None
        _lieuDit = None
        '''
        _dateDebutValide = None
        _dateFinValide = None
        _dateMajValide = None
        _numeroFacture = None
        _dateFacture = None
        _reserveEventuelle = None

        """Chantier"""
        _idMaitreOuvrage = None
        _idDirectionLocale = None
        _idEntrepreneur = None
        _idResponsableTravaux = None
        _projet = None
        _longueurEtape = None
        _surface = None
        _idCentraleEnrobage = None
        _epaisseurCaisson = None
        _qualiteCaisson = None
        _epaisseurSupport = None
        _qualiteSupport = None
        _epaisseurRevetement = None
        _qualiteRevetement = None
        _qualiteEncollage = None
        _boucleInduction = None
        _faucherAccotement = None
        _curerDepotoirs = None
        _nettoyer_bords = None
        _colmater_fissure = None
        _prTouches = None
        _autre = None
        _lieuSeance = None
        _jourSeance = None
        _heureSeance = None
        _categories = None
        _reperageEffectif = None

        """Fouille"""
        _idMaitreOuvrage = None
        _idDirectionLocale = None
        _idEntrepreneur = None
        _idResponsableTravaux = None
        _nomMaitreOuvrage = None
        _rueMaitreOuvrage = None
        _localiteMaitreOuvrage = None
        _telephoneMaitreOuvrage = None
        _faxMaitreOuvrage = None
        _courrielMaitreOuvrage = None
        _nomDirectionLocale = None
        _prenomDirectionLocale = None
        _mobileDirectionLocale = None
        _telephoneDirectionLocale = None
        _faxDirectionLocale = None
        _courrielDirectionLocale = None
        _nomEntrepreneur = None
        _rueEntrepreneur = None
        _localiteEntrepreneur = None
        _telephoneEntrepreneur = None
        _faxEntrepreneur = None
        _courrielEntrepreneur = None
        _nomResponsableTravaux = None
        _prenomResponsableTravaux = None
        _mobileResponsableTravaux = None
        _telephoneResponsableTravaux = None
        _faxResponsableTravaux = None
        _courrielResponsableTravaux = None
        _facturation = None
        '''
        _coordonnesX = None
        _coordonnesY = None
        _commune = None
        _cadastre = None
        _bienFonds = None
        _autreCadastre = None
        _autreBienFonds = None
        _lieuDit = None
        '''
        _prTouches = None
        _longueurEtape = None
        _epaisseurCaisson = None
        _qualiteCaisson = None
        _epaisseurSupport = None
        _qualiteSupport = None
        _epaisseurRevetement = None
        _qualiteRevetement = None
        _qualiteEncollage = None
        _dateDebutValide = None
        _dateFinValide = None
        _dateMajValide = None
        _numeroFacture = None
        _dateFacture = None
        _reserveEventuelle = None
        _planTypes = None
        _reperageEffectif = None

        """Manifestation"""
        _parcours = None

        # Read params evenement

        # Read perturbation params
        if 'idEvenement' in request.params:
            idEvenement = request.params['idEvenement']

        if not idEvenement:
            raise Exception('Id evenement is null')

        # Check if the user has permission to update evenement
        user_can_update_evenement = Utils.user_can_update_evenement(request, current_user_id, idEvenement)

        if not user_can_update_evenement:
            raise HTTPForbidden()

        if 'idEntite' in request.params:
            idEntite = request.params['idEntite']

        if 'idResponsable' in request.params:
            idResponsable = request.params['idResponsable']

        if 'idRequerant' in request.params:
            idRequerant = request.params['idRequerant']

        if 'type' in request.params:
            type = request.params['type']

        if 'numeroDossier' in request.params:
            numeroDossier = request.params['numeroDossier']

        if 'division' in request.params:
            division = request.params['division']

        if 'libelle' in request.params:
            libelle = request.params['libelle']

        if 'description' in request.params:
            description = request.params['description']

        if 'prevision' in request.params:
            prevision = request.params['prevision']

            if prevision == 'true':
                prevision = True
            elif prevision == 'false':
                prevision = False
            else:
                prevision = None

        """
        if 'urgence' in request.params:
            urgence = request.params['urgence']

            if urgence == 'true':
                urgence = True
            elif urgence == 'false':
                urgence = False
            else:
                urgence = None
        """

        if 'dateDebut' in request.params:
            dateDebut = request.params['dateDebut']

        if 'heureDebut' in request.params:
            heureDebut = request.params['heureDebut']

        if 'dateFin' in request.params:
            dateFin = request.params['dateFin']

        if 'heureFin' in request.params:
            heureFin = request.params['heureFin']

        if 'localisation' in request.params:
            localisation = request.params['localisation']
        '''
        if 'localite' in request.params:
            localite = request.params['localite']

        if 'lieuDit' in request.params:
            lieuDit = request.params['lieuDit']

        if 'reperageEffectif' in request.params:
            reperageEffectif = request.params['reperageEffectif']

            if reperageEffectif == 'true':
                reperageEffectif = True
            elif reperageEffectif == 'false':
                reperageEffectif = False
            else:
                reperageEffectif = None
        '''
        if 'nomRequerant' in request.params:
            nomRequerant = request.params['nomRequerant']

        if 'rueRequerant' in request.params:
            rueRequerant = request.params['rueRequerant']

        if 'localiteRequerant' in request.params:
            localiteRequerant = request.params['localiteRequerant']

        if 'telephoneRequerant' in request.params:
            telephoneRequerant = request.params['telephoneRequerant']

        if 'faxRequerant' in request.params:
            faxRequerant = request.params['faxRequerant']

        if 'courrielRequerant' in request.params:
            courrielRequerant = request.params['courrielRequerant']

        if 'nomContact' in request.params:
            nomContact = request.params['nomContact']

        if 'prenomContact' in request.params:
            prenomContact = request.params['prenomContact']

        if 'mobileContact' in request.params:
            mobileContact = request.params['mobileContact']

        if 'telephoneContact' in request.params:
            telephoneContact = request.params['telephoneContact']

        if 'faxContact' in request.params:
            faxContact = request.params['faxContact']

        if 'courrielContact' in request.params:
            courrielContact = request.params['courrielContact']

        if 'remarque' in request.params:
            remarque = request.params['remarque']

        if 'dateDemande' in request.params:
            dateDemande = request.params['dateDemande']

        if 'dateOctroi' in request.params:
            dateOctroi = request.params['dateOctroi']

        """
        if 'ajoutePar' in request.params:
            ajoutePar = request.params['ajoutePar']

        if 'dateAjout' in request.params:
            dateAjout = request.params['dateAjout']
        """

        if 'modifiePar' in request.params:
            modifiePar = request.params['modifiePar']
        """

        if 'dateModification' in request.params:
            dateModification = request.params['dateModification']


        if 'dateSuppression' in request.params:
            dateSuppression = request.params['dateSuppression']
        """

        # Check date_debut, if less than 24h, urgence=true
        """"
        if not urgence and dateDebut != None and heureDebut != None:
            date_time_str = str(dateDebut) + ' ' + str(heureDebut)
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()

            if date_time_obj >= now and date_time_obj <= now + timedelta(days=1):
                urgence = True
        """

        if 'geometries_reperages' in request.params:
            geometries_reperages = request.params['geometries_reperages']

        # Read params autre evenement
        if '_idMaitreOuvrage' in request.params:
            _idMaitreOuvrage = request.params['_idMaitreOuvrage']

        if '_idDirectionLocale' in request.params:
            _idDirectionLocale = request.params['_idDirectionLocale']

        if '_idEntrepreneur' in request.params:
            _idEntrepreneur = request.params['_idEntrepreneur']

        if '_idResponsableTravaux' in request.params:
            _idResponsableTravaux = request.params['_idResponsableTravaux']

        if '_cause' in request.params:
            _cause = request.params['_cause']

        if '_nomMaitreOuvrage' in request.params:
            _nomMaitreOuvrage = request.params['_nomMaitreOuvrage']

        if '_rueMaitreOuvrage' in request.params:
            _rueMaitreOuvrage = request.params['_rueMaitreOuvrage']

        if '_localiteMaitreOuvrage' in request.params:
            _localiteMaitreOuvrage = request.params['_localiteMaitreOuvrage']

        if '_telephoneMaitreOuvrage' in request.params:
            _telephoneMaitreOuvrage = request.params['_telephoneMaitreOuvrage']

        if '_faxMaitreOuvrage' in request.params:
            _faxMaitreOuvrage = request.params['_faxMaitreOuvrage']

        if '_courrielMaitreOuvrage' in request.params:
            _courrielMaitreOuvrage = request.params['_courrielMaitreOuvrage']

        if '_nomDirectionLocale' in request.params:
            _nomDirectionLocale = request.params['_nomDirectionLocale']

        if '_prenomDirectionLocale' in request.params:
            _prenomDirectionLocale = request.params['_prenomDirectionLocale']

        if '_mobileDirectionLocale' in request.params:
            _mobileDirectionLocale = request.params['_mobileDirectionLocale']

        if '_telephoneDirectionLocale' in request.params:
            _telephoneDirectionLocale = request.params['_telephoneDirectionLocale']

        if '_faxDirectionLocale' in request.params:
            _faxDirectionLocale = request.params['_faxDirectionLocale']

        if '_courrielDirectionLocale' in request.params:
            _courrielDirectionLocale = request.params['_courrielDirectionLocale']

        if '_nomEntrepreneur' in request.params:
            _nomEntrepreneur = request.params['_nomEntrepreneur']

        if '_rueEntrepreneur' in request.params:
            _rueEntrepreneur = request.params['_rueEntrepreneur']

        if '_localiteEntrepreneur' in request.params:
            _localiteEntrepreneur = request.params['_localiteEntrepreneur']

        if '_telephoneEntrepreneur' in request.params:
            _telephoneEntrepreneur = request.params['_telephoneEntrepreneur']

        if '_faxEntrepreneur' in request.params:
            _faxEntrepreneur = request.params['_faxEntrepreneur']

        if '_courrielEntrepreneur' in request.params:
            _courrielEntrepreneur = request.params['_courrielEntrepreneur']

        if '_nomResponsableTravaux' in request.params:
            _nomResponsableTravaux = request.params['_nomResponsableTravaux']

        if '_prenomResponsableTravaux' in request.params:
            _prenomResponsableTravaux = request.params['_prenomResponsableTravaux']

        if '_mobileResponsableTravaux' in request.params:
            _mobileResponsableTravaux = request.params['_mobileResponsableTravaux']

        if '_telephoneResponsableTravaux' in request.params:
            _telephoneResponsableTravaux = request.params['_telephoneResponsableTravaux']

        if '_faxResponsableTravaux' in request.params:
            _faxResponsableTravaux = request.params['_faxResponsableTravaux']

        if '_courrielResponsableTravaux' in request.params:
            _courrielResponsableTravaux = request.params['_courrielResponsableTravaux']

        if '_facturation' in request.params:
            _facturation = request.params['_facturation']

        '''
        if '_coordonnesX' in request.params:
            _coordonnesX = request.params['_coordonnesX']

        if '_coordonnesY' in request.params:
            _coordonnesY = request.params['_coordonnesY']

        if '_commune' in request.params:
            _commune = request.params['_commune']

        if '_cadastre' in request.params:
            _cadastre = request.params['_cadastre']

        if '_bienFonds' in request.params:
            _bienFonds = request.params['_bienFonds']

        if '_autre_cadastre' in request.params:
            _autre_cadastre = request.params['_autre_cadastre']

        if '_autre_bienFonds' in request.params:
            _autre_bienFonds = request.params['_autre_bienFonds']

        if '_lieuDit' in request.params:
            _lieuDit = request.params['_lieuDit']
        '''

        if '_dateDebutValide' in request.params:
            _dateDebutValide = request.params['_dateDebutValide']

        if '_dateFinValide' in request.params:
            _dateFinValide = request.params['_dateFinValide']

        if '_dateMajValide' in request.params:
            _dateMajValide = request.params['_dateMajValide']

        if '_numeroFacture' in request.params:
            _numeroFacture = request.params['_numeroFacture']

        if '_dateFacture' in request.params:
            _dateFacture = request.params['_dateFacture']

        if '_reserveEventuelle' in request.params:
            _reserveEventuelle = request.params['_reserveEventuelle']

        # Read params chantier
        if '_idMaitreOuvrage' in request.params:
            _idMaitreOuvrage = request.params['_idMaitreOuvrage']

        if '_idDirectionLocale' in request.params:
            _idDirectionLocale = request.params['_idDirectionLocale']

        if '_idEntrepreneur' in request.params:
            _idEntrepreneur = request.params['_idEntrepreneur']

        if '_idResponsableTravaux' in request.params:
            _idResponsableTravaux = request.params['_idResponsableTravaux']

        if '_projet' in request.params:
            _projet = request.params['_projet']

        if '_longueurEtape' in request.params:
            _longueurEtape = request.params['_longueurEtape']

        if '_surface' in request.params:
            _surface = request.params['_surface']

        if '_idCentraleEnrobage' in request.params:
            _idCentraleEnrobage = request.params['_idCentraleEnrobage']

        if '_epaisseurCaisson' in request.params:
            _epaisseurCaisson = request.params['_epaisseurCaisson']

        if '_qualiteCaisson' in request.params:
            _qualiteCaisson = request.params['_qualiteCaisson']

        if '_epaisseurSupport' in request.params:
            _epaisseurSupport = request.params['_epaisseurSupport']

        if '_qualiteSupport' in request.params:
            _qualiteSupport = request.params['_qualiteSupport']

        if '_epaisseurRevetement' in request.params:
            _epaisseurRevetement = request.params['_epaisseurRevetement']

        if '_qualiteRevetement' in request.params:
            _qualiteRevetement = request.params['_qualiteRevetement']

        if '_qualiteEncollage' in request.params:
            _qualiteEncollage = request.params['_qualiteEncollage']

        if '_boucleInduction' in request.params:
            _boucleInduction = request.params['_boucleInduction']

            if _boucleInduction == 'true':
                _boucleInduction = True
            elif _boucleInduction == 'false':
                _boucleInduction = False
            else:
                _boucleInduction = None

        if '_faucherAccotement' in request.params:
            _faucherAccotement = request.params['_faucherAccotement']

            if _faucherAccotement == 'true':
                _faucherAccotement = True
            elif _faucherAccotement == 'false':
                _faucherAccotement = False
            else:
                _faucherAccotement = None

        if '_curerDepotoirs' in request.params:
            _curerDepotoirs = request.params['_curerDepotoirs']

            if _curerDepotoirs == 'true':
                _curerDepotoirs = True
            elif _curerDepotoirs == 'false':
                _curerDepotoirs = False
            else:
                _curerDepotoirs = None

        if '_nettoyer_bords' in request.params:
            _nettoyer_bords = request.params['_nettoyer_bords']

            if _nettoyer_bords == 'true':
                _nettoyer_bords = True
            elif _nettoyer_bords == 'false':
                _nettoyer_bords = False
            else:
                _nettoyer_bords = None

        if '_colmater_fissure' in request.params:
            _colmater_fissure = request.params['_colmater_fissure']

            if _colmater_fissure == 'true':
                _colmater_fissure = True
            elif _colmater_fissure == 'false':
                _colmater_fissure = False
            else:
                _colmater_fissure = None

        if '_prTouches' in request.params:
            _prTouches = request.params['_prTouches']

            if _prTouches == 'true':
                _prTouches = True
            elif _prTouches == 'false':
                _prTouches = False
            else:
                _prTouches = None

        if '_autre' in request.params:
            _autre = request.params['_autre']

        if '_lieuSeance' in request.params:
            _lieuSeance = request.params['_lieuSeance']

        if '_jourSeance' in request.params:
            _jourSeance = request.params['_jourSeance']

        if '_heureSeance' in request.params:
            _heureSeance = request.params['_heureSeance']

        if '_reperageEffectif' in request.params:
            _reperageEffectif = request.params['_reperageEffectif']

            if _reperageEffectif == 'true':
                _reperageEffectif = True
            elif _reperageEffectif == 'false':
                _reperageEffectif = False
            else:
                _reperageEffectif = None

        if '_categories' in request.params:
            _categories = request.params['_categories']

            if _categories:
                categories_array = json.loads(_categories)

        # Read params fouille
        if '_idMaitreOuvrage' in request.params:
            _idMaitreOuvrage = request.params['_idMaitreOuvrage']

        if '_idDirectionLocale' in request.params:
            _idDirectionLocale = request.params['_idDirectionLocale']

        if '_idEntrepreneur' in request.params:
            _idEntrepreneur = request.params['_idEntrepreneur']

        if '_idResponsableTravaux' in request.params:
            _idResponsableTravaux = request.params['_idResponsableTravaux']

        if '_nomMaitreOuvrage' in request.params:
            _nomMaitreOuvrage = request.params['_nomMaitreOuvrage']

        if '_rueMaitreOuvrage' in request.params:
            _rueMaitreOuvrage = request.params['_rueMaitreOuvrage']

        if '_localiteMaitreOuvrage' in request.params:
            _localiteMaitreOuvrage = request.params['_localiteMaitreOuvrage']

        if '_telephoneMaitreOuvrage' in request.params:
            _telephoneMaitreOuvrage = request.params['_telephoneMaitreOuvrage']

        if '_faxMaitreOuvrage' in request.params:
            _faxMaitreOuvrage = request.params['_faxMaitreOuvrage']

        if '_courrielMaitreOuvrage' in request.params:
            _courrielMaitreOuvrage = request.params['_courrielMaitreOuvrage']

        if '_nomDirectionLocale' in request.params:
            _nomDirectionLocale = request.params['_nomDirectionLocale']

        if '_prenomDirectionLocale' in request.params:
            _prenomDirectionLocale = request.params['_prenomDirectionLocale']

        if '_mobileDirectionLocale' in request.params:
            _mobileDirectionLocale = request.params['_mobileDirectionLocale']

        if '_telephoneDirectionLocale' in request.params:
            _telephoneDirectionLocale = request.params['_telephoneDirectionLocale']

        if '_faxDirectionLocale' in request.params:
            _faxDirectionLocale = request.params['_faxDirectionLocale']

        if '_courrielDirectionLocale' in request.params:
            _courrielDirectionLocale = request.params['_courrielDirectionLocale']

        if '_nomEntrepreneur' in request.params:
            _nomEntrepreneur = request.params['_nomEntrepreneur']

        if '_rueEntrepreneur' in request.params:
            _rueEntrepreneur = request.params['_rueEntrepreneur']

        if '_localiteEntrepreneur' in request.params:
            _localiteEntrepreneur = request.params['_localiteEntrepreneur']

        if '_telephoneEntrepreneur' in request.params:
            _telephoneEntrepreneur = request.params['_telephoneEntrepreneur']

        if '_faxEntrepreneur' in request.params:
            _faxEntrepreneur = request.params['_faxEntrepreneur']

        if '_courrielEntrepreneur' in request.params:
            _courrielEntrepreneur = request.params['_courrielEntrepreneur']

        if '_nomResponsableTravaux' in request.params:
            _nomResponsableTravaux = request.params['_nomResponsableTravaux']

        if '_prenomResponsableTravaux' in request.params:
            _prenomResponsableTravaux = request.params['_prenomResponsableTravaux']

        if '_mobileResponsableTravaux' in request.params:
            _mobileResponsableTravaux = request.params['_mobileResponsableTravaux']

        if '_telephoneResponsableTravaux' in request.params:
            _telephoneResponsableTravaux = request.params['_telephoneResponsableTravaux']

        if '_faxResponsableTravaux' in request.params:
            _faxResponsableTravaux = request.params['_faxResponsableTravaux']

        if '_courrielResponsableTravaux' in request.params:
            _courrielResponsableTravaux = request.params['_courrielResponsableTravaux']

        if '_facturation' in request.params:
            _facturation = request.params['_facturation']

        '''
        if '_coordonnesX' in request.params:
            _coordonnesX = request.params['_coordonnesX']

        if '_coordonnesY' in request.params:
            _coordonnesY = request.params['_coordonnesY']

        if '_commune' in request.params:
            _commune = request.params['_commune']

        if '_cadastre' in request.params:
            _cadastre = request.params['_cadastre']

        if '_bienFonds' in request.params:
            _bienFonds = request.params['_bienFonds']

        if '_autreCadastre' in request.params:
            _autreCadastre = request.params['_autreCadastre']

        if '_autreBienFonds' in request.params:
            _autreBienFonds = request.params['_autreBienFonds']

        if '_lieuDit' in request.params:
            _lieuDit = request.params['_lieuDit']
        '''

        if '_prTouches' in request.params:
            _prTouches = request.params['_prTouches']

            if _prTouches == 'true':
                _prTouches = True
            elif _prTouches == 'false':
                _prTouches = False
            else:
                _prTouches = None

        if '_longueurEtape' in request.params:
            _longueurEtape = request.params['_longueurEtape']

        if '_epaisseurCaisson' in request.params:
            _epaisseurCaisson = request.params['_epaisseurCaisson']

        if '_qualiteCaisson' in request.params:
            _qualiteCaisson = request.params['_qualiteCaisson']

        if '_epaisseurSupport' in request.params:
            _epaisseurSupport = request.params['_epaisseurSupport']

        if '_qualiteSupport' in request.params:
            _qualiteSupport = request.params['_qualiteSupport']

        if '_epaisseurRevetement' in request.params:
            _epaisseurRevetement = request.params['_epaisseurRevetement']

        if '_qualiteRevetement' in request.params:
            _qualiteRevetement = request.params['_qualiteRevetement']

        if '_qualiteEncollage' in request.params:
            _qualiteEncollage = request.params['_qualiteEncollage']

        if '_dateDebutValide' in request.params:
            _dateDebutValide = request.params['_dateDebutValide']

        if '_dateFinValide' in request.params:
            _dateFinValide = request.params['_dateFinValide']

        if '_dateMajValide' in request.params:
            _dateMajValide = request.params['_dateMajValide']

        if '_numeroFacture' in request.params:
            _numeroFacture = request.params['_numeroFacture']

        if '_dateFacture' in request.params:
            _dateFacture = request.params['_dateFacture']

        if '_reserveEventuelle' in request.params:
            _reserveEventuelle = request.params['_reserveEventuelle']

        if '_reperageEffectif' in request.params:
            _reperageEffectif = request.params['_reperageEffectif']

            if _reperageEffectif == 'true':
                _reperageEffectif = True
            elif _reperageEffectif == 'false':
                _reperageEffectif = False
            else:
                _reperageEffectif = None

        if '_planTypes' in request.params:
            _planTypes = request.params['_planTypes']

            if _planTypes:
                plan_types_array = json.loads(_planTypes)

        # Read params manifestation
        if '_parcours' in request.params:
            _parcours = request.params['_parcours']

        # Read params Reperage
        if '_idReperage' in request.params:
            _idReperage = request.params['_idReperage']

        if '_idDeviation' in request.params and request.params['_idDeviation'] != '':
            _idDeviation = request.params['_idDeviation']

        if '_proprietaire' in request.params:
            _proprietaire = request.params['_proprietaire']

        if '_axe' in request.params:
            _axe = request.params['_axe']

        if '_sens' in request.params:
            _sens = request.params['_sens']

        if '_prDebut' in request.params:
            _prDebut = request.params['_prDebut']

        if '_prDebutDistance' in request.params:
            _prDebutDistance = request.params['_prDebutDistance']

        if '_prFin' in request.params:
            _prFin = request.params['_prFin']

        if '_prFinDistance' in request.params:
            _prFinDistance = request.params['_prFinDistance']

        if '_ecartd' in request.params:
            _ecartd = request.params['_ecartd']

        if '_ecartf' in request.params:
            _ecartf = request.params['_ecartf']

        if '_usageNeg' in request.params:
            _usageNeg = request.params['_usageNeg']

            if _usageNeg == 'true':
                _usageNeg = True

            elif _usageNeg == 'false':
                _usageNeg = False
            else:
                _usageNeg = None

        if '_fSurf' in request.params and request.params['_fSurf'] != '':
            _fSurf = request.params['_fSurf']

        if '_fLong' in request.params and request.params['_fLong'] != '':
            _fLong = request.params['_fLong']

        with transaction.manager:

            evenement_query = request.dbsession.query(models.Evenement).filter(
                models.Evenement.id == idEvenement)

            if evenement_query.count() == 0:
                raise CustomError('{} with id {} not found'.format(models.Evenement.__tablename__, idEvenement))

            evenement_record = evenement_query.first()
            evenement_record.id_responsable = idResponsable
            evenement_record.id_requerant = idRequerant
            evenement_record.type = type
            evenement_record.numero_dossier = numeroDossier
            evenement_record.division = division
            evenement_record.libelle = libelle
            evenement_record.description = description
            evenement_record.prevision = prevision
            #evenement_record.urgence = urgence
            evenement_record.date_debut = dateDebut
            evenement_record.heure_debut = heureDebut
            evenement_record.date_fin = dateFin
            evenement_record.heure_fin = heureFin
            evenement_record.localisation = localisation
            # evenement_record.localite = localite
            # evenement_record.lieu_dit = lieuDit
            # evenement_record.reperage_effectif = reperageEffectif
            evenement_record.nom_requerant = nomRequerant
            evenement_record.rue_requerant = rueRequerant
            evenement_record.localite_requerant = localiteRequerant
            evenement_record.telephone_requerant = telephoneRequerant
            evenement_record.fax_requerant = faxRequerant
            evenement_record.courriel_requerant = courrielRequerant
            evenement_record.nom_contact = nomContact
            evenement_record.prenom_contact = prenomContact
            evenement_record.mobile_contact = mobileContact
            evenement_record.telephone_contact = telephoneContact
            evenement_record.fax_contact = faxContact
            evenement_record.courriel_contact = courrielContact
            evenement_record.remarque = remarque
            evenement_record.date_demande = dateDemande
            evenement_record.date_octroi = dateOctroi
            # evenement_record.id_utilisateur_ajout = ajoutePar
            # evenement_record.date_ajout = dateAjout
            evenement_record.id_utilisateur_modification = current_user_id,
            # evenement_record.date_modification = dateModification
            # evenement_record.date_suppression = dateSuppression

            # Type evenement : autre
            if int(type) == int(settings['autre_evenement_id']):
                autre_evenement_query = request.dbsession.query(models.AutreEvenement).filter(
                    models.AutreEvenement.id_evenement == idEvenement)

                if autre_evenement_query.count() == 0:
                    raise CustomError(
                        '{} with id_evenement {} not found'.format(models.AutreEvenement.__tablename__, idEvenement))

                autre_evenement_record = autre_evenement_query.first()
                autre_evenement_record.id_maitre_ouvrage = _idMaitreOuvrage
                autre_evenement_record.id_direction_locale = _idDirectionLocale
                autre_evenement_record.id_entrepreneur = _idEntrepreneur
                autre_evenement_record.id_responsable_travaux = _idResponsableTravaux
                autre_evenement_record.cause = _cause
                autre_evenement_record.nom_maitre_ouvrage = _nomMaitreOuvrage
                autre_evenement_record.rue_maitre_ouvrage = _rueMaitreOuvrage
                autre_evenement_record.localite_maitre_ouvrage = _localiteMaitreOuvrage
                autre_evenement_record.telephone_maitre_ouvrage = _telephoneMaitreOuvrage
                autre_evenement_record.fax_maitre_ouvrage = _faxMaitreOuvrage
                autre_evenement_record.courriel_maitre_ouvrage = _courrielMaitreOuvrage
                autre_evenement_record.nom_direction_locale = _nomDirectionLocale
                autre_evenement_record.prenom_direction_locale = _prenomDirectionLocale
                autre_evenement_record.mobile_direction_locale = _mobileDirectionLocale
                autre_evenement_record.telephone_direction_locale = _telephoneDirectionLocale
                autre_evenement_record.fax_direction_locale = _faxDirectionLocale
                autre_evenement_record.courriel_direction_locale = _courrielDirectionLocale
                autre_evenement_record.nom_entrepreneur = _nomEntrepreneur
                autre_evenement_record.rue_entrepreneur = _rueEntrepreneur
                autre_evenement_record.localite_entrepreneur = _localiteEntrepreneur
                autre_evenement_record.telephone_entrepreneur = _telephoneEntrepreneur
                autre_evenement_record.fax_entrepreneur = _faxEntrepreneur
                autre_evenement_record.courriel_entrepreneur = _courrielEntrepreneur
                autre_evenement_record.nom_responsable_travaux = _nomResponsableTravaux
                autre_evenement_record.prenom_responsable_travaux = _prenomResponsableTravaux
                autre_evenement_record.mobile_responsable_travaux = _mobileResponsableTravaux
                autre_evenement_record.telephone_responsable_travaux = _telephoneResponsableTravaux
                autre_evenement_record.fax_responsable_travaux = _faxResponsableTravaux
                autre_evenement_record.courriel_responsable_travaux = _courrielResponsableTravaux
                autre_evenement_record.facturation = _facturation
                '''               
                autre_evenement_record.coordonnes_x = _coordonnesX
                autre_evenement_record.coordonnes_y = _coordonnesY
                autre_evenement_record.commune = _commune
                autre_evenement_record.cadastre = _cadastre
                autre_evenement_record.bien_fonds = _bienFonds
                autre_evenement_record.autre_cadastre = _autre_cadastre
                autre_evenement_record.autre_bien_fonds = _autre_bienFonds
                autre_evenement_record.lieu_dit = _lieuDit
                '''
                autre_evenement_record.date_debut_valide = _dateDebutValide
                autre_evenement_record.date_fin_valide = _dateFinValide
                autre_evenement_record.date_maj_valide = _dateMajValide
                autre_evenement_record.numero_facture = _numeroFacture
                autre_evenement_record.date_facture = _dateFacture
                autre_evenement_record.reserve_eventuelle = _reserveEventuelle

            # Type evenement : Chantier
            elif int(type) == int(settings['chantier_evenement_id']):
                chantier_query = request.dbsession.query(models.Chantier).filter(
                    models.Chantier.id_evenement == idEvenement)

                if chantier_query.count() == 0:
                    raise CustomError(
                        '{} with id_evenement {} not found'.format(models.Chantier.__tablename__, idEvenement))

                chantier_record = chantier_query.first()
                chantier_record.id_maitre_ouvrage = _idMaitreOuvrage
                chantier_record.id_direction_locale = _idDirectionLocale
                chantier_record.id_entrepreneur = _idEntrepreneur
                chantier_record.id_responsable_travaux = _idResponsableTravaux
                chantier_record.projet = _projet
                chantier_record.longueur_etape = _longueurEtape
                chantier_record.surface = _surface
                chantier_record.id_centrale_enrobage = _idCentraleEnrobage
                chantier_record.epaisseur_caisson = _epaisseurCaisson
                chantier_record.qualite_caisson = _qualiteCaisson
                chantier_record.epaisseur_support = _epaisseurSupport
                chantier_record.qualite_support = _qualiteSupport
                chantier_record.epaisseur_revetement = _epaisseurRevetement
                chantier_record.qualite_revetement = _qualiteRevetement
                chantier_record.qualite_encollage = _qualiteEncollage
                chantier_record.boucle_induction = _boucleInduction
                chantier_record.faucher_accotement = _faucherAccotement
                chantier_record.curer_depotoirs = _curerDepotoirs
                chantier_record.nettoyer_bords = _nettoyer_bords
                chantier_record.colmater_fissure = _colmater_fissure
                chantier_record.pr_touches = _prTouches
                chantier_record.autre = _autre
                chantier_record.lieu_seance = _lieuSeance
                chantier_record.jour_seance = _jourSeance
                chantier_record.heure_seance = _heureSeance


                # Delete old categories
                request.dbsession.query(models.LienChantierCategorieChantier).filter(
                    models.LienChantierCategorieChantier.id_chantier == chantier_record.id).delete(synchronize_session=False)

                if categories_array and len(categories_array) > 0:
                    for category_id in categories_array:
                        lien_categ_chant = models.LienChantierCategorieChantier(
                            id_chantier=chantier_record.id,
                            categorie=category_id
                        )
                        request.dbsession.add(lien_categ_chant)


            # Type evenement : Fouille
            elif int(type) == int(settings['fouille_evenement_id']):
                fouille_query = request.dbsession.query(models.Fouille).filter(
                    models.Fouille.id_evenement == idEvenement)

                if fouille_query.count() == 0:
                    raise CustomError(
                        '{} with id_evenement {} not found'.format(models.Fouille.__tablename__, idEvenement))

                fouille_record = fouille_query.first()
                fouille_record.id_maitre_ouvrage = _idMaitreOuvrage
                fouille_record.id_direction_locale = _idDirectionLocale
                fouille_record.id_entrepreneur = _idEntrepreneur
                fouille_record.id_responsable_travaux = _idResponsableTravaux
                fouille_record.nom_maitre_ouvrage = _nomMaitreOuvrage
                fouille_record.rue_maitre_ouvrage = _rueMaitreOuvrage
                fouille_record.localite_maitre_ouvrage = _localiteMaitreOuvrage
                fouille_record.telephone_maitre_ouvrage = _telephoneMaitreOuvrage
                fouille_record.fax_maitre_ouvrage = _faxMaitreOuvrage
                fouille_record.courriel_maitre_ouvrage = _courrielMaitreOuvrage
                fouille_record.nom_direction_locale = _nomDirectionLocale
                fouille_record.prenom_direction_locale = _prenomDirectionLocale
                fouille_record.mobile_direction_locale = _mobileDirectionLocale
                fouille_record.telephone_direction_locale = _telephoneDirectionLocale
                fouille_record.fax_direction_locale = _faxDirectionLocale
                fouille_record.courriel_direction_locale = _courrielDirectionLocale
                fouille_record.nom_entrepreneur = _nomEntrepreneur
                fouille_record.rue_entrepreneur = _rueEntrepreneur
                fouille_record.localite_entrepreneur = _localiteEntrepreneur
                fouille_record.telephone_entrepreneur = _telephoneEntrepreneur
                fouille_record.fax_entrepreneur = _faxEntrepreneur
                fouille_record.courriel_entrepreneur = _courrielEntrepreneur
                fouille_record.nom_responsable_travaux = _nomResponsableTravaux
                fouille_record.prenom_responsable_travaux = _prenomResponsableTravaux
                fouille_record.mobile_responsable_travaux = _mobileResponsableTravaux
                fouille_record.telephone_responsable_travaux = _telephoneResponsableTravaux
                fouille_record.fax_responsable_travaux = _faxResponsableTravaux
                fouille_record.courriel_responsable_travaux = _courrielResponsableTravaux
                fouille_record.facturation = _facturation
                # fouille_record.coordonnes_x = _coordonnesX
                # fouille_record.coordonnes_y = _coordonnesY
                # fouille_record.commune = _commune
                # fouille_record.cadastre = _cadastre
                # fouille_record.bien_fonds = _bienFonds
                # fouille_record.autre_cadastre = _autreCadastre
                # fouille_record.autre_bien_fonds = _autreBienFonds
                # fouille_record.lieu_dit = _lieuDit
                fouille_record.pr_touches = _prTouches
                fouille_record.longueur_etape = _longueurEtape
                fouille_record.epaisseur_caisson = _epaisseurCaisson
                fouille_record.qualite_caisson = _qualiteCaisson
                fouille_record.epaisseur_support = _epaisseurSupport
                fouille_record.qualite_support = _qualiteSupport
                fouille_record.epaisseur_revetement = _epaisseurRevetement
                fouille_record.qualite_revetement = _qualiteRevetement
                fouille_record.qualite_encollage = _qualiteEncollage
                fouille_record.date_debut_valide = _dateDebutValide
                fouille_record.date_fin_valide = _dateFinValide
                fouille_record.date_maj_valide = _dateMajValide
                fouille_record.numero_facture = _numeroFacture
                fouille_record.date_facture = _dateFacture
                fouille_record.reserve_eventuelle = _reserveEventuelle

                # Plan types
                # Delete old plan types
                request.dbsession.query(models.LienFouillePlanType).filter(
                    models.LienFouillePlanType.id_evenement == idEvenement).delete(synchronize_session=False)

                if plan_types_array and len(plan_types_array) > 0:
                    for plan_type_id in plan_types_array:
                        lien_fouille_plan = models.LienFouillePlanType(
                            id_evenement=idEvenement,
                            id_plan_type=plan_type_id
                        )
                        request.dbsession.add(lien_fouille_plan)

            # Type evenement : Manifestation
            elif int(type) == int(settings['manifestation_evenement_id']):
                manifestation_query = request.dbsession.query(models.Manifestation).filter(
                    models.Manifestation.id_evenement == idEvenement)

                if manifestation_query.count() == 0:
                    raise CustomError(
                        '{} with id_evenement {} not found'.format(models.Manifestation.__tablename__, idEvenement))

                manifestation_record = manifestation_query.first()
                manifestation_record.parcours = _parcours

            # Geometries_reperages
            # Delete old geometries
            ev_ligne_ids = []
            for item in request.dbsession.query(models.EvenementLigne.id).filter(
                    models.EvenementLigne.id_evenement == idEvenement).all():
                ev_ligne_ids.append(item.id)

            request.dbsession.query(models.Reperage).filter(
                models.Reperage.id_evenement_ligne.in_(ev_ligne_ids)).delete(synchronize_session=False)
            request.dbsession.query(models.EvenementPoint).filter(
                models.EvenementPoint.id_evenement == idEvenement).delete()
            request.dbsession.query(models.EvenementLigne).filter(
                models.EvenementLigne.id_evenement == idEvenement).delete()
            request.dbsession.query(models.EvenementPolygone).filter(
                models.EvenementPolygone.id_evenement == idEvenement).delete()

            # Add new geometries
            if geometries_reperages != None:
                json_geometries_reperages = json.loads(geometries_reperages)

                for onegeojson in json_geometries_reperages:

                    # Geometry
                    if 'geometry' in onegeojson:
                        geometry = onegeojson['geometry']

                        if 'type' in geometry:
                            type_geom = geometry['type']

                            # Point
                            if type_geom == 'Point':
                                evenement_point_model = models.EvenementPoint(id_evenement=idEvenement)
                                evenement_point_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(evenement_point_model)

                            # Line
                            elif type_geom == 'LineString' or type_geom == 'MultiLineString' or type_geom == 'GeometryCollection':
                                evenement_ligne_model = models.EvenementLigne(id_evenement=idEvenement)
                                evenement_ligne_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(evenement_ligne_model)

                                if 'reperage' in onegeojson:
                                    request.dbsession.flush()

                                    reperage = onegeojson['reperage']
                                    reperage_model = models.Reperage(
                                        id_evenement_ligne=evenement_ligne_model.id,
                                        id_deviation=reperage['idDeviation'],
                                        proprietaire=reperage['proprietaire'],
                                        axe=reperage['axe'],
                                        sens=reperage['sens'],
                                        pr_debut=reperage['prDebut'],
                                        pr_debut_distance=reperage['prDebutDistance'],
                                        pr_fin=reperage['prFin'],
                                        pr_fin_distance=reperage['prFinDistance'],
                                        ecartd=reperage['ecartd'],
                                        ecartf=reperage['ecartf'],
                                        usage_neg=reperage['usageNeg'],
                                        f_surf=reperage['fSurf'],
                                        f_long=reperage['fLong']
                                    )
                                    request.dbsession.add(reperage_model)


                            # Polygon
                            elif type_geom == 'Polygon':
                                evenement_polygon_model = models.EvenementPolygone(id_evenement=idEvenement)
                                evenement_polygon_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(evenement_polygon_model)

            # Commit transaction
            transaction.commit()
            request.dbsession.flush()

            # Send mail to SRB touché
            if _prTouches:
                subject = 'subject'
                body = 'body'
                query = request.dbsession.query(models.ContactAvisPrTouche.id_contact).all()
                conatct_ids = []
                for c in query:
                    conatct_ids.append(c.id_contact)
                contact_mails = Utils.get_contacts_mails_by_ids(request, conatct_ids)
                PTMailer.send_mail(request, contact_mails, subject, body)

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except CustomError as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Type perturbation by id view
########################################################
@view_config(route_name='types_perturbation_by_id', request_method='GET', renderer='json')
def type_perturbation_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.TypePerturbation)
        result = query.filter(models.TypePerturbation.id == request.matchdict['id']).first()

        if not result:
            raise Exception(id_not_found_exception)



    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Delete perturbation by id view
########################################################
@view_config(route_name='perturbation_by_id', request_method='DELETE', renderer='json')
def delete_perturbation_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        id = request.matchdict['id']

        # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id is None:
            raise HTTPForbidden()

        # Check if the user has permission to delete evenement
        user_can_delete_perturbation = Utils.user_can_delete_perturbation(request, current_user_id, id)
        
        if not user_can_delete_perturbation:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Perturbation)
        perturbation = query.filter(models.Perturbation.id == id).first()

        if not perturbation:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            perturbation.date_suppression = func.now()
            # Commit transaction
            transaction.commit()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Types perturbations view
########################################################
@view_config(route_name='types_perturbations', request_method='GET', renderer='json')
@view_config(route_name='types_perturbations_slash', request_method='GET', renderer='json')
def types_perturbations_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.TypePerturbation).all()


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return query


########################################################
# Perturbation by id view
########################################################
@view_config(route_name='perturbation_by_id', request_method='GET', renderer='json')
def perturbation_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query_perturbation = request.dbsession.query(models.Perturbation)
        perturbation = query_perturbation.filter(models.Perturbation.id == request.matchdict['id']).first()

        # Get type evenement
        query_evenement = request.dbsession.query(models.Evenement)
        evenement = query_evenement.filter(models.Evenement.id == perturbation.id_evenement).first()

        if not perturbation:
            raise Exception(id_not_found_exception)

    except (exc.SQLAlchemyError, exc.DBAPIError, Exception) as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return perturbation.format_with_type_evenement(evenement.type)


########################################################
# Perturbations view
########################################################
@view_config(route_name='perturbations', request_method='GET', renderer='json')
@view_config(route_name='perturbations_slash', request_method='GET', renderer='json')
def perturbations_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Perturbation).all()

        formattedResult = []

        for perturbation in query:
            formattedResult.append(perturbation.format())


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return formattedResult


########################################################
# Get Perturbation edition by id view
########################################################
@view_config(route_name='perturbation_edition_by_id', request_method='GET', renderer='json')
def perturbation_edition_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)

        # Check if the user has permission to read perturbation
        user_can_read_perturbation = Utils.user_can_read_perturbation(request, current_user_id, id)

        if not user_can_read_perturbation:
            raise HTTPForbidden()

        relatedtype = None

        # Perturbation
        query_perturbation = request.dbsession.query(models.Perturbation)
        perturbation = query_perturbation.filter(models.Perturbation.id == id).first()

        if not perturbation:
            raise Exception(id_not_found_exception)

        # Utilisateur ajout
        contact_utilisateur_ajout = request.dbsession.query(models.Contact).filter(
            models.Contact.id == perturbation.id_utilisateur_ajout).first()

        # Utilisateur modification
        contact_utilisateur_modification = request.dbsession.query(models.Contact).filter(
            models.Contact.id == perturbation.id_utilisateur_modification).first()

        # Utilisateur validation
        contact_utilisateur_validation = request.dbsession.query(models.Contact).filter(
            models.Contact.id == perturbation.id_utilisateur_validation).first()

        # Type perturbation : Fermeture
        if perturbation.type == int(settings['fermeture_perturbation_id']):
            query = request.dbsession.query(models.Fermeture)
            relatedtype = query.filter(models.Fermeture.id_perturbation == id).first()

        # Type perturbation : Occupation
        elif perturbation.type == int(settings['occupation_perturbation_id']):
            query = request.dbsession.query(models.Occupation)
            relatedtype = query.filter(models.Occupation.id_perturbation == id).first()

        # Geometries
        geometries_array = []
        query_geom_point = request.dbsession.query(models.PerturbationPoint.id,
                                                   func.public.ST_AsGeoJSON(models.PerturbationPoint.geometry).label(
                                                       "geometry")).filter(
            models.PerturbationPoint.id_perturbation == id).all()
        query_geom_ligne = request.dbsession.query(models.PerturbationLigne.id,
                                                   func.public.ST_AsGeoJSON(models.PerturbationLigne.geometry).label(
                                                       "geometry")).filter(
            models.PerturbationLigne.id_perturbation == id).all()

        for item in query_geom_point + query_geom_ligne:
            geometries_array.append({'id': item.id, 'geometry': item.geometry})

        # Contacts à aviser
        contacts_a_aviser = []

        for ap, c in request.dbsession.query(models.AvisPerturbation, models.Contact).filter(
                models.AvisPerturbation.id_perturbation == id).filter(models.AvisPerturbation.id_contact == models.Contact.id).all():
            contacts_a_aviser.append(c)

        # Reperage
        reperages = []
        evenement_lignes_ids = []

        for item in query_geom_ligne:
            evenement_lignes_ids.append(item.id)

        if len(evenement_lignes_ids) > 0:
            query_reperage = request.dbsession.query(models.Reperage).filter(models.Reperage.id_perturbation_ligne.in_(evenement_lignes_ids)).all()

            if query_reperage:
                for item in query_reperage:
                    reperages.append(item.format())


        # Deviations
        deviations = []
        query_deviations = request.dbsession.query(models.Deviation.id,
                                                   func.public.ST_AsGeoJSON(models.Deviation.geometry).label(
                                                       "geometry")).filter(
                                                   models.Deviation.id_perturbation == id).all()

        for item in query_deviations:
            deviations.append({'id': item.id, 'geometry': item.geometry})

        # Format perturbation
        perturbation = perturbation.format()

        if contact_utilisateur_ajout:
            perturbation['nom_utilisateur_ajout'] = contact_utilisateur_ajout.prenom + ' ' +  contact_utilisateur_ajout.nom

        if contact_utilisateur_modification:
            perturbation['nom_utilisateur_modification'] = contact_utilisateur_modification.prenom + ' ' +  contact_utilisateur_modification.nom

        if contact_utilisateur_validation:
            perturbation['nom_utilisateur_validation'] = contact_utilisateur_validation.prenom + ' ' + contact_utilisateur_validation.nom

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'perturbation': perturbation, 'reperages': reperages,
            'infos': {} if not relatedtype else relatedtype, 'contacts_a_aviser': contacts_a_aviser, 'geometries': geometries_array, 'deviations': deviations}



########################################################
# Add perturbation edition
########################################################
@view_config(route_name='perturbation_edition', request_method='POST', renderer='json')
@view_config(route_name='perturbation_edition_slash', request_method='POST', renderer='json')
def add_perturbation_edition(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        evenement_record = None
        contacts_a_aviser_ids_array = []

        # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id is None:
            raise HTTPForbidden()

        # Default params value
        idEvenement = None
        idEntite = None
        idResponsableTrafic = None
        type = None
        trancheHoraire = None
        description = None
        dateDebut = None
        heureDebut = None
        dateFin = None
        heureFin = None
        localisation = None
        nomResponsableTrafic = None
        prenomResponsableTrafic = None
        mobileResponsableTrafic = None
        telephoneResponsableTrafic = None
        faxResponsableTrafic = None
        courrielResponsableTrafic = None
        remarque = None
        urgence = None
        etat = int(settings['perturbation_etat_attente_code'])
        dateValidation = None
        utilisateurValidation = None
        decision = None
        dateDecision = None
        #ajoutePar = None
        # dateAjout = None
        # modifiePar = None
        # dateModification = None
        # dateSuppression = None
        geometries_reperages = None

        """Contacts à aviser"""
        contacts_a_aviser = None

        """Fermeture"""
        _deviation = None
        _idResponsable = None

        """Occupation"""
        _idResponsableRegulation = None
        _typeOccupation = None
        _typeRegulation = None
        _voiesCondamnees = None
        _largeurGabarit = None
        _hauteurGabarit = None
        _heurePointe = None
        _weekEnd = None

        """Reperage"""
        _idDeviation = None
        _proprietaire = None
        _axe = None
        _sens = None
        _prDebut = None
        _prDebutDistance = None
        _prFin = None
        _prFinDistance = None
        _ecartd = None
        _ecartf = None
        _usageNeg = None
        _fSurf = None
        _fLong = None


        """Deviations"""
        geometries_deviations = None

        # Read perturbation params
        if 'idEvenement' in request.params:
            idEvenement = request.params['idEvenement']

            evenement_record = request.dbsession.query(models.Evenement).filter(models.Evenement.id == idEvenement).first()

            if not evenement_record:
                raise Exception('Evenement not found')

        if 'idEntite' in request.params:
            idEntite = request.params['idEntite']

        # Check if the user has permission to add perturbation
        user_can_add_perturbation = Utils.user_can_add_perturbation(request, current_user_id, idEvenement, idEntite)

        if not user_can_add_perturbation:
            raise HTTPForbidden()

        if 'idResponsableTrafic' in request.params:
            idResponsableTrafic = request.params['idResponsableTrafic']

        if 'type' in request.params:
            type = request.params['type']

        if 'trancheHoraire' in request.params:
            trancheHoraire = request.params['trancheHoraire']

            if trancheHoraire == 'true':
                trancheHoraire = True
            elif trancheHoraire == 'false':
                trancheHoraire = False
            else:
                trancheHoraire = None

        if 'description' in request.params:
            description = request.params['description']

        if 'dateDebut' in request.params:
            dateDebut = request.params['dateDebut']

        if 'heureDebut' in request.params:
            heureDebut = request.params['heureDebut']

        if 'dateFin' in request.params:
            dateFin = request.params['dateFin']

        if 'heureFin' in request.params:
            heureFin = request.params['heureFin']

        if 'localisation' in request.params:
            localisation = request.params['localisation']

        if 'nomResponsableTrafic' in request.params:
            nomResponsableTrafic = request.params['nomResponsableTrafic']

        if 'prenomResponsableTrafic' in request.params:
            prenomResponsableTrafic = request.params['prenomResponsableTrafic']

        if 'mobileResponsableTrafic' in request.params:
            mobileResponsableTrafic = request.params['mobileResponsableTrafic']

        if 'telephoneResponsableTrafic' in request.params:
            telephoneResponsableTrafic = request.params['telephoneResponsableTrafic']

        if 'faxResponsableTrafic' in request.params:
            faxResponsableTrafic = request.params['faxResponsableTrafic']

        if 'courrielResponsableTrafic' in request.params:
            courrielResponsableTrafic = request.params['courrielResponsableTrafic']

        if 'remarque' in request.params:
            remarque = request.params['remarque']

        """
        if 'urgence' in request.params:
            urgence = request.params['urgence']

            if urgence == 'true':
                urgence = True
            elif urgence == 'false':
                urgence = False
            else:
                urgence = None
        """

        # Check date_debut, if less than 24h, urgence=true
        urgence = False
        if dateDebut != None and heureDebut != None:
            date_time_str = str(dateDebut) + ' ' + str(heureDebut)
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()

            if date_time_obj >= now and date_time_obj <= now + timedelta(days=1):
                urgence = True

        if 'etat' in request.params:
            etat = request.params['etat']
            etat = int(etat) if etat != None and etat != '' else int(settings['perturbation_etat_attente_code'])


        # If urgence == true, etat = accepté
        if urgence == True:
            etat = settings['perturbation_etat_acceptee_code']

        # If urgence == False, Check role Trafic
        else:
            user_can_update_etat_perturbation_creation = Utils.user_can_update_etat_perturbation_creation(request, current_user_id)

            # If not authorized, force default etat (en attente)
            if not user_can_update_etat_perturbation_creation:
                etat = int(settings['perturbation_etat_attente_code'])


        if int(etat) == int(settings['perturbation_etat_acceptee_code']):
            dateValidation = datetime.datetime.today().strftime('%Y-%m-%d')
            utilisateurValidation = current_user_id

        """
        if 'dateValidation' in request.params:
            dateValidation = request.params['dateValidation']

        if 'utilisateurValidation' in request.params:
            utilisateurValidation = request.params['utilisateurValidation']
        """

        if 'decision' in request.params:
            decision = request.params['decision']

        if 'dateDecision' in request.params:
            dateDecision = request.params['dateDecision']

        """
        if 'ajoutePar' in request.params:
            ajoutePar = request.params['ajoutePar']
        
        if 'dateAjout' in request.params:
            dateAjout = request.params['dateAjout']

        if 'modifiePar' in request.params:
            modifiePar = request.params['modifiePar']

        if 'dateModification' in request.params:
            dateModification = request.params['dateModification']

        if 'dateSuppression' in request.params:
            dateSuppression = request.params['dateSuppression']
        """

        if 'geometries_reperages' in request.params:
            geometries_reperages = request.params['geometries_reperages']

        #Read contacts à aviser
        if 'contacts_a_aviser' in request.params:
            contacts_a_aviser = request.params['contacts_a_aviser']

        # Read fermeture params
        if '_deviation' in request.params:
            _deviation = request.params['_deviation']

        if '_idResponsable' in request.params:
            _idResponsable = request.params['_idResponsable']

        # Read occupation params
        if '_idResponsableRegulation' in request.params:
            _idResponsableRegulation = request.params['_idResponsableRegulation']

        if '_typeOccupation' in request.params:
            _typeOccupation = request.params['_typeOccupation']

        if '_typeRegulation' in request.params:
            _typeRegulation = request.params['_typeRegulation']

        if '_voiesCondamnees' in request.params:
            _voiesCondamnees = request.params['_voiesCondamnees']

        if '_largeurGabarit' in request.params:
            _largeurGabarit = request.params['_largeurGabarit']

        if '_hauteurGabarit' in request.params:
            _hauteurGabarit = request.params['_hauteurGabarit']

        if '_heurePointe' in request.params:
            _heurePointe = request.params['_heurePointe']

            if _heurePointe == 'true':
                _heurePointe = True
            elif _heurePointe == 'false':
                _heurePointe = False
            else:
                _heurePointe = None

        if '_weekEnd' in request.params:
            _weekEnd = request.params['_weekEnd']

            if _weekEnd == 'true':
                _weekEnd = True
            elif _weekEnd == 'false':
                _weekEnd = False
            else:
                _weekEnd = None

        # Read params Reperage

        if '_idDeviation' in request.params and request.params['_idDeviation'] != '':
            _idDeviation = request.params['_idDeviation']

        if '_proprietaire' in request.params:
            _proprietaire = request.params['_proprietaire']

        if '_axe' in request.params:
            _axe = request.params['_axe']

        if '_sens' in request.params:
            _sens = request.params['_sens']

        if '_prDebut' in request.params:
            _prDebut = request.params['_prDebut']

        if '_prDebutDistance' in request.params:
            _prDebutDistance = request.params['_prDebutDistance']

        if '_prFin' in request.params:
            _prFin = request.params['_prFin']

        if '_prFinDistance' in request.params:
            _prFinDistance = request.params['_prFinDistance']

        if '_ecartd' in request.params:
            _ecartd = request.params['_ecartd']

        if '_ecartf' in request.params:
            _ecartf = request.params['_ecartf']

        if '_usageNeg' in request.params:
            _usageNeg = request.params['_usageNeg']

            if _usageNeg == 'true':
                _usageNeg = True

            elif _usageNeg == 'false':
                _usageNeg = False
            else:
                _usageNeg = None

        if '_fSurf' in request.params and request.params['_fSurf'] != '':
            _fSurf = request.params['_fSurf']

        if '_fLong' in request.params and request.params['_fLong'] != '':
            _fLong = request.params['_fLong']


        #Read params deviations
        if 'geometries_deviations' in request.params and request.params['geometries_deviations'] != '':
            geometries_deviations = request.params['geometries_deviations']

        with transaction.manager:
            perturbation_model = models.Perturbation(
                id_evenement=idEvenement,
                id_responsable_trafic=idResponsableTrafic,
                type=type,
                tranche_horaire=trancheHoraire,
                description=description,
                date_debut=dateDebut,
                heure_debut=heureDebut,
                date_fin=dateFin,
                heure_fin=heureFin,
                localisation=localisation,
                nom_responsable_trafic=nomResponsableTrafic,
                prenom_responsable_trafic=prenomResponsableTrafic,
                mobile_responsable_trafic=mobileResponsableTrafic,
                telephone_responsable_trafic=telephoneResponsableTrafic,
                fax_responsable_trafic=faxResponsableTrafic,
                courriel_responsable_trafic=courrielResponsableTrafic,
                remarque=remarque,
                urgence=urgence,
                etat=etat,
                date_validation=dateValidation,
                id_utilisateur_validation=utilisateurValidation,
                decision=decision,
                date_decision=dateDecision,
                id_utilisateur_ajout=current_user_id,
                # date_ajout=dateAjout,
                id_utilisateur_modification=current_user_id
                # date_modification=dateModification,
                # date_suppression=dateSuppression
            )

            request.dbsession.add(perturbation_model)
            request.dbsession.flush()
            max_perturb_id = perturbation_model.id

            # Historiser les changements d'état
            Utils.add_historique_etat_perturbation(request, current_user_id, max_perturb_id, etat)


            # Contacts à aviser
            if contacts_a_aviser != None:

                json_contacts_a_aviser = json.loads(contacts_a_aviser)

                for onecontactid in json_contacts_a_aviser:
                    contacts_a_aviser_ids_array.append(onecontactid)
                    avis_perturbation_model = models.AvisPerturbation(
                        id_perturbation=max_perturb_id,
                        id_contact=onecontactid)

                    request.dbsession.add(avis_perturbation_model)

            # Related model
            related_model = None

            # Type perturbation : Fermeture
            if int(type) == int(settings['fermeture_perturbation_id']):
                related_model = models.Fermeture(
                    id_perturbation=max_perturb_id,
                    deviation=_deviation,
                    id_responsable=_idResponsable)

            # Type perturbation : Occupation
            elif int(type) == int(settings['occupation_perturbation_id']):
                related_model = models.Occupation(
                    id_perturbation=max_perturb_id,
                    id_responsable_regulation=_idResponsableRegulation,
                    type_regulation=_typeRegulation,
                    voies_condamnees=_voiesCondamnees,
                    largeur_gabarit=_largeurGabarit,
                    hauteur_gabarit=_hauteurGabarit,
                    heure_pointe=_heurePointe,
                    week_end=_weekEnd,
                    type_occupation= _typeOccupation)

            request.dbsession.add(related_model)
            request.dbsession.flush()


            # Geometries_reperages
            reperages_list = []
            if geometries_reperages != None:
                json_geometries_reperages = json.loads(geometries_reperages)

                for onegeojson in json_geometries_reperages:

                    # Geometry
                    if 'geometry' in onegeojson:
                        geometry = onegeojson['geometry']

                        if 'type' in geometry:
                            type_geom = geometry['type']

                            # Point
                            if type_geom == 'Point':
                                perturbation_point_model = models.PerturbationPoint(id_perturbation=max_perturb_id)
                                perturbation_point_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(perturbation_point_model)

                            # Line
                            elif type_geom == 'LineString' or type_geom == 'MultiLineString' or type_geom == 'GeometryCollection':
                                perturbation_ligne_model = models.PerturbationLigne(id_perturbation=max_perturb_id)
                                perturbation_ligne_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(perturbation_ligne_model)

                                if 'reperage' in onegeojson:
                                    request.dbsession.flush()

                                    reperage = onegeojson['reperage']
                                    reperage_model = models.Reperage(
                                        id_perturbation_ligne=perturbation_ligne_model.id,
                                        id_deviation=reperage['idDeviation'],
                                        proprietaire=reperage['proprietaire'],
                                        axe=reperage['axe'],
                                        sens=reperage['sens'],
                                        pr_debut=reperage['prDebut'],
                                        pr_debut_distance=reperage['prDebutDistance'],
                                        pr_fin=reperage['prFin'],
                                        pr_fin_distance=reperage['prFinDistance'],
                                        ecartd=reperage['ecartd'],
                                        ecartf=reperage['ecartf'],
                                        usage_neg=reperage['usageNeg'],
                                        f_surf=reperage['fSurf'],
                                        f_long=reperage['fLong']
                                    )
                                    request.dbsession.add(reperage_model)
                                    reperages_list.append(reperage_model)


            # Geometries_deviations
            if geometries_deviations != None:
                json_geometries_deviations = json.loads(geometries_deviations)

                for onegeojson in json_geometries_deviations:
                    deviation_model = models.Deviation(id_perturbation=max_perturb_id)
                    deviation_model.set_json_geometry(str(onegeojson), settings['srid'])
                    request.dbsession.add(deviation_model)

            transaction.commit()


            # Prepare mail to send
            mail_dict = Utils.create_perturbation_mail_dict(request, perturbation_model, evenement_record,
                                                            _deviation)

            # Reperages list
            reperages_string = ''
            for reperage_model in reperages_list:
                reperages_string += '<td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td>'.format(
                    '???', reperage_model.axe, reperage_model.pr_debut, reperage_model.pr_debut_distance,
                    reperage_model.pr_fin, reperage_model.pr_fin_distance)

            # Envoi email si fermeture d'urgence
            #	Envoi à la liste des personnes concernées par les fermetures d’urgence
            if perturbation_model.urgence:
                mails_contacts_mails_fermeture_urgence = Utils.get_mails_contacts_mails_fermeture_urgence(
                    request)

                if mails_contacts_mails_fermeture_urgence and len(mails_contacts_mails_fermeture_urgence) > 0:
                    PTMailer.send_templated_mail(request, mails_contacts_mails_fermeture_urgence,
                                                 settings['mail_fermeture_urgence_subject'],
                                                 'email_templates:fermeture_urgence', mail_dict,
                                                 reperages_string)


            # Envoi d’emails régulier lors d’une fermeture et occupation
            contacts_a_aviser_mails_array = []

            # Envoi à la liste des personnes sélectionnées dans le formulaire
            if len(contacts_a_aviser_ids_array) > 0:
                contacts_a_aviser_mails_array = Utils.get_contacts_mails_by_ids(request, contacts_a_aviser_ids_array)

            # If Accepté → Envoi au créateur
            if int(etat) == int(settings['perturbation_etat_acceptee_code']):
                connected_user = LDAPQuery.get_connected_user(request)
                mail_att_name = settings['ldap_user_attribute_mail']
                if connected_user and mail_att_name in connected_user:
                    connected_user_mail = connected_user[mail_att_name]

                    if not connected_user_mail in contacts_a_aviser_mails_array:
                        contacts_a_aviser_mails_array.append(connected_user_mail)


            # If En attente → Envoi à l’approbateur = rôle trafic
            elif int(etat) == int(settings['perturbation_etat_attente_code']):
                contacts_a_aviser_mails_array += Utils.get_mails_of_contacts_belonging_to_a_group(request, settings['ldap_trafic_group_name'])

            #Delete duplicates from array
            contacts_a_aviser_mails_array = list(dict.fromkeys(contacts_a_aviser_mails_array))

            if contacts_a_aviser_mails_array and len(contacts_a_aviser_mails_array) > 0:
                PTMailer.send_templated_mail(request, contacts_a_aviser_mails_array,
                                             'FERMETURE' if int(perturbation_model.type) == int(settings['fermeture_perturbation_id']) else "OCCUPATION" if int(perturbation_model.type) == int(settings['occupation_perturbation_id']) else 'Info',
                                             'email_templates:fermeture_occupation', mail_dict,
                                             reperages_string)

            # Envoi d’email en cas de SRB touché
            #   Envoi à la liste des personnes GMAR
            evenement_pr_touche = Utils.check_evenement_pr_touche(request, idEvenement)

            if evenement_pr_touche:
                contacts_pr_touche = Utils.get_mails_contacts_pr_touche(request)

                if contacts_pr_touche and len(contacts_pr_touche) > 0:
                    PTMailer.send_templated_mail(request, contacts_pr_touche,
                                                 settings['mail_srb_touche_subject'],
                                                 'email_templates:srb_touche', mail_dict,
                                                 reperages_string)

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        # tm.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Update perturbation edition
########################################################
@view_config(route_name='perturbation_edition', request_method='PUT', renderer='json')
@view_config(route_name='perturbation_edition_slash', request_method='PUT', renderer='json')
def update_perturbation_edition(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id is None:
            raise HTTPForbidden()

        evenement_record = None
        etat_updated = False
        urgence_updated = False
        contacts_a_aviser_ids_array = []

        # Default params value
        idPerturbation = None
        idEvenement = None
        idResponsableTrafic = None
        type = None
        trancheHoraire = None
        description = None
        dateDebut = None
        heureDebut = None
        dateFin = None
        heureFin = None
        localisation = None
        nomResponsableTrafic = None
        prenomResponsableTrafic = None
        mobileResponsableTrafic = None
        telephoneResponsableTrafic = None
        faxResponsableTrafic = None
        courrielResponsableTrafic = None
        remarque = None
        urgence = None
        etat = None
        dateValidation = None
        utilisateurValidation = None
        decision = None
        dateDecision = None
        # ajoutePar = None
        # dateAjout = None
        # modifiePar = None
        dateModification = None
        # dateSuppression = None
        geometries_reperages = None

        """Contacts à aviser"""
        contacts_a_aviser = None

        """Common"""
        _idPerturbation = None

        """Fermeture"""
        _deviation = None
        _idResponsable = None

        """Occupation"""
        _idResponsableRegulation = None
        _typeOccupation = None
        _typeRegulation = None
        _voiesCondamnees = None
        _largeurGabarit = None
        _hauteurGabarit = None
        _heurePointe = None
        _weekEnd = None

        """geometries_deviations"""
        geometries_deviations = None


        # Read perturbation params
        if 'idPerturbation' in request.params:
            idPerturbation = request.params['idPerturbation']

        if not idPerturbation:
            raise Exception('Id perturbation is null')

        # Check if the user has permission to update perturbation
        user_can_update_perturbation = Utils.user_can_update_perturbation(request, current_user_id, idPerturbation)

        if not user_can_update_perturbation:
            raise HTTPForbidden()

        if 'idEvenement' in request.params:
            idEvenement = request.params['idEvenement']

            evenement_record = request.dbsession.query(models.Evenement).filter(
                models.Evenement.id == idEvenement).first()

            if not evenement_record:
                raise Exception('Evenement not found')

        if 'idResponsableTrafic' in request.params:
            idResponsableTrafic = request.params['idResponsableTrafic']

        if 'type' in request.params:
            type = request.params['type']

        if 'trancheHoraire' in request.params:
            trancheHoraire = request.params['trancheHoraire']

            if trancheHoraire == 'true':
                trancheHoraire = True
            elif trancheHoraire == 'false':
                trancheHoraire = False
            else:
                trancheHoraire = None

        if 'description' in request.params:
            description = request.params['description']

        if 'dateDebut' in request.params:
            dateDebut = request.params['dateDebut']

        if 'heureDebut' in request.params:
            heureDebut = request.params['heureDebut']

        if 'dateFin' in request.params:
            dateFin = request.params['dateFin']

        if 'heureFin' in request.params:
            heureFin = request.params['heureFin']

        if 'localisation' in request.params:
            localisation = request.params['localisation']

        if 'nomResponsableTrafic' in request.params:
            nomResponsableTrafic = request.params['nomResponsableTrafic']

        if 'prenomResponsableTrafic' in request.params:
            prenomResponsableTrafic = request.params['prenomResponsableTrafic']

        if 'mobileResponsableTrafic' in request.params:
            mobileResponsableTrafic = request.params['mobileResponsableTrafic']

        if 'telephoneResponsableTrafic' in request.params:
            telephoneResponsableTrafic = request.params['telephoneResponsableTrafic']

        if 'faxResponsableTrafic' in request.params:
            faxResponsableTrafic = request.params['faxResponsableTrafic']

        if 'courrielResponsableTrafic' in request.params:
            courrielResponsableTrafic = request.params['courrielResponsableTrafic']

        if 'remarque' in request.params:
            remarque = request.params['remarque']

        """
        if 'urgence' in request.params:
            urgence = request.params['urgence']

            if urgence == 'true':
                urgence = True
            elif urgence == 'false':
                urgence = False
            else:
                urgence = None
        """

        # Check date_debut, if less than 24h, urgence=true
        urgence = False
        if dateDebut != None and heureDebut != None:
            date_time_str = str(dateDebut) + ' ' + str(heureDebut)
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            now = datetime.datetime.now()

            if date_time_obj >= now and date_time_obj <= now + timedelta(days=1):
                urgence = True

        if 'etat' in request.params:
            etat = request.params['etat']
            etat = int(etat) if etat != None and etat != '' else int(settings['perturbation_etat_attente_code'])

        # If urgence == true, etat = accepté
        if urgence == True:
            etat = settings['perturbation_etat_acceptee_code']

        # If urgence == False, Check role Trafic
        else:
            user_can_update_etat_perturbation = Utils.user_can_update_etat_perturbation(request, current_user_id, idPerturbation)

            # If not authorized, force default etat (en attente)
            if not user_can_update_etat_perturbation:
                etat = int(settings['perturbation_etat_attente_code'])

        if int(etat) == int(settings['perturbation_etat_acceptee_code']):
            dateValidation = datetime.datetime.today().strftime('%Y-%m-%d')
            utilisateurValidation = current_user_id

        """
        if 'dateValidation' in request.params:
            dateValidation = request.params['dateValidation']

        if 'utilisateurValidation' in request.params:
            utilisateurValidation = request.params['utilisateurValidation']
        """

        if 'decision' in request.params:
            decision = request.params['decision']

        if 'dateDecision' in request.params:
            dateDecision = request.params['dateDecision']

        """
        if 'ajoutePar' in request.params:
            ajoutePar = request.params['ajoutePar']

        if 'dateAjout' in request.params:
            dateAjout = request.params['dateAjout']
    

        if 'modifiePar' in request.params:
            modifiePar = request.params['modifiePar']

        if 'dateModification' in request.params:
            dateModification = request.params['dateModification']

       
        if 'dateSuppression' in request.params:
            dateSuppression = request.params['dateSuppression']
        """

        if 'geometries_reperages' in request.params:
            geometries_reperages = request.params['geometries_reperages']

        # Read contacts à aviser
        if 'contacts_a_aviser' in request.params:
            contacts_a_aviser = request.params['contacts_a_aviser']

        # Read fermeture params
        if '_deviation' in request.params:
            _deviation = request.params['_deviation']

        if '_idResponsable' in request.params:
            _idResponsable = request.params['_idResponsable']

        # Read occupation params
        if '_idResponsableRegulation' in request.params:
            _idResponsableRegulation = request.params['_idResponsableRegulation']

        if '_typeOccupation' in request.params:
            _typeOccupation = request.params['_typeOccupation']


        if '_typeRegulation' in request.params:
            _typeRegulation = request.params['_typeRegulation']

        if '_voiesCondamnees' in request.params:
            _voiesCondamnees = request.params['_voiesCondamnees']

        if '_largeurGabarit' in request.params:
            _largeurGabarit = request.params['_largeurGabarit']

        if '_hauteurGabarit' in request.params:
            _hauteurGabarit = request.params['_hauteurGabarit']

        if '_heurePointe' in request.params:
            _heurePointe = request.params['_heurePointe']

            if _heurePointe == 'true':
                _heurePointe = True
            elif _heurePointe == 'false':
                _heurePointe = False
            else:
                _heurePointe = None

        if '_weekEnd' in request.params:
            _weekEnd = request.params['_weekEnd']

            if str(_weekEnd) == 'true':
                _weekEnd = True
            elif str(_weekEnd) == 'false':
                _weekEnd = False
            else:
                _weekEnd = False

        # Read params deviations
        if 'geometries_deviations' in request.params and request.params['geometries_deviations'] != '':
            geometries_deviations = request.params['geometries_deviations']


        with transaction.manager:

            perturbation_query = request.dbsession.query(models.Perturbation).filter(
                models.Perturbation.id == idPerturbation)

            if perturbation_query.count() == 0:
                raise CustomError('{} with id {} not found'.format(models.Perturbation.__tablename__, idPerturbation))

            perturbation_record = perturbation_query.first()


            # If urgence == false, check etat
            if not urgence:

                # Lorsque la date est modifiée, l'état repasse en attente.
                if dateDebut is not None and perturbation_record.date_debut is not None and str(perturbation_record.date_debut) != dateDebut:
                    etat = settings['perturbation_etat_attente_code']


                # Lorsque le tracé est modifié, l'état repasse en attente.
                if int(etat) != int(settings['perturbation_etat_attente_code']):
                    is_geometries_equal = Utils.compare_perturbation_geometries(request, idPerturbation, geometries_reperages)

                    if not is_geometries_equal:
                        etat = settings['perturbation_etat_attente_code']


            # Historiser les changements d'état
            etat_old_str = str(perturbation_record.etat) if perturbation_record.etat is not None else ''
            etat_new_str = str(etat) if etat is not None else ''

            if etat_old_str != etat_new_str:
                Utils.add_historique_etat_perturbation(request, current_user_id, idPerturbation, etat)
                etat_updated = True


            if perturbation_record.urgence != urgence:
                urgence_updated = True

            perturbation_record.id_evenement = idEvenement
            perturbation_record.id_responsable_trafic = idResponsableTrafic
            perturbation_record.type = type
            perturbation_record.tranche_horaire = trancheHoraire
            perturbation_record.description = description
            perturbation_record.date_debut = dateDebut
            perturbation_record.heure_debut = heureDebut
            perturbation_record.date_fin = dateFin
            perturbation_record.heure_fin = heureFin
            perturbation_record.localisation = localisation
            perturbation_record.nom_responsable_trafic = nomResponsableTrafic
            perturbation_record.prenom_responsable_trafic = prenomResponsableTrafic
            perturbation_record.mobile_responsable_trafic = mobileResponsableTrafic
            perturbation_record.telephone_responsable_trafic = telephoneResponsableTrafic
            perturbation_record.fax_responsable_trafic = faxResponsableTrafic
            perturbation_record.courriel_responsable_trafic = courrielResponsableTrafic
            perturbation_record.remarque = remarque
            perturbation_record.urgence = urgence
            perturbation_record.etat = etat
            perturbation_record.date_validation = dateValidation
            perturbation_record.id_utilisateur_validation = utilisateurValidation
            perturbation_record.decision = decision
            perturbation_record.date_decision = dateDecision
            # perturbation_record.id_utilisateur_ajout = ajoutePar
            # perturbation_record.date_ajout = dateAjout
            perturbation_record.id_utilisateur_modification = current_user_id
            # perturbation_record.date_modification = func.now()
            # perturbation_record.date_suppression = dateSuppression


            # Contacts à aviser
            # Delete old avis perturbation
            request.dbsession.query(models.AvisPerturbation).filter(
            models.AvisPerturbation.id_perturbation == idPerturbation).delete(synchronize_session=False)

            # Add contacts à aviser
            if contacts_a_aviser != None:
                json_contacts_a_aviser = json.loads(contacts_a_aviser)

                for onecontactid in json_contacts_a_aviser:
                    contacts_a_aviser_ids_array.append(onecontactid)
                    avis_perturbation_model = models.AvisPerturbation(
                        id_perturbation=idPerturbation,
                        id_contact=onecontactid)

                    request.dbsession.add(avis_perturbation_model)


            # Type perturbation : Fermeture
            if int(type) == int(settings['fermeture_perturbation_id']):

                fermeture_query = request.dbsession.query(models.Fermeture).filter(
                    models.Fermeture.id_perturbation == idPerturbation)

                if fermeture_query.count() == 0:
                    raise CustomError(
                        '{} with id_perturbation {} not found'.format(models.Fermeture.__tablename__, idPerturbation))

                fermeture_record = fermeture_query.first()
                fermeture_record.id_perturbation = idPerturbation
                fermeture_record.deviation = _deviation
                fermeture_record.id_responsable = _idResponsable


            # Type perturbation : Occupation
            elif int(type) == int(settings['occupation_perturbation_id']):

                occupation_query = request.dbsession.query(models.Occupation).filter(
                    models.Occupation.id_perturbation == idPerturbation)

                if occupation_query.count() == 0:
                    raise CustomError(
                        '{} with id perturbation {} not found'.format(models.Occupation.__tablename__, idPerturbation))

                occupation_record = occupation_query.first()
                occupation_record.id_perturbation = idPerturbation
                occupation_record.id_responsable_regulation = _idResponsableRegulation
                occupation_record.type_regulation = _typeRegulation
                occupation_record.voies_condamnees = _voiesCondamnees
                occupation_record.largeur_gabarit = _largeurGabarit
                occupation_record.hauteur_gabarit = _hauteurGabarit
                occupation_record.heure_pointe = _heurePointe
                occupation_record.week_end = _weekEnd
                occupation_record.type_occupation = _typeOccupation


            # Geometries_reperages

            # Get perturbations id having lines
            perturbation_ligne_ids = []
            for item in request.dbsession.query(models.PerturbationLigne.id).filter(
                    models.PerturbationLigne.id_perturbation == idPerturbation).all():
                perturbation_ligne_ids.append(item.id)

            # Delete old geometries and reperages
            request.dbsession.query(models.Reperage).filter(
                models.Reperage.id_perturbation_ligne.in_(perturbation_ligne_ids)).delete(synchronize_session=False)
            request.dbsession.query(models.PerturbationPoint).filter(
                models.PerturbationPoint.id_perturbation == idPerturbation).delete()
            request.dbsession.query(models.PerturbationLigne).filter(
                models.PerturbationLigne.id_perturbation == idPerturbation).delete()

            # Add new geometries
            reperages_list = []
            if geometries_reperages != None:
                json_geometries_reperages = json.loads(geometries_reperages)

                for onegeojson in json_geometries_reperages:

                    # Geometry
                    if 'geometry' in onegeojson:
                        geometry = onegeojson['geometry']

                        if 'type' in geometry:
                            type_geom = geometry['type']

                            # Point
                            if type_geom == 'Point':
                                perturbation_point_model = models.PerturbationPoint(id_perturbation=idPerturbation)
                                perturbation_point_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(perturbation_point_model)

                            # Line
                            elif type_geom == 'LineString' or type_geom == 'MultiLineString' or type_geom == 'GeometryCollection':
                                perturbation_ligne_model = models.PerturbationLigne(id_perturbation=idPerturbation)
                                perturbation_ligne_model.set_json_geometry(str(geometry), settings['srid'])
                                request.dbsession.add(perturbation_ligne_model)

                                if 'reperage' in onegeojson:
                                    request.dbsession.flush()

                                    reperage = onegeojson['reperage']
                                    reperage_model = models.Reperage(
                                        id_perturbation_ligne=perturbation_ligne_model.id,
                                        id_deviation=reperage['idDeviation'],
                                        proprietaire=reperage['proprietaire'],
                                        axe=reperage['axe'],
                                        sens=reperage['sens'],
                                        pr_debut=reperage['prDebut'],
                                        pr_debut_distance=reperage['prDebutDistance'],
                                        pr_fin=reperage['prFin'],
                                        pr_fin_distance=reperage['prFinDistance'],
                                        ecartd=reperage['ecartd'],
                                        ecartf=reperage['ecartf'],
                                        usage_neg=reperage['usageNeg'],
                                        f_surf=reperage['fSurf'],
                                        f_long=reperage['fLong']
                                    )
                                    request.dbsession.add(reperage_model)
                                    reperages_list.append(reperage_model)


            # Geometries_deviations
            request.dbsession.query(models.Deviation).filter(models.Deviation.id_perturbation == idPerturbation).delete(synchronize_session=False)
            if geometries_deviations != None:
                json_geometries_deviations = json.loads(geometries_deviations)

                for onegeojson in json_geometries_deviations:
                    deviation_model = models.Deviation(id_perturbation=idPerturbation)
                    deviation_model.set_json_geometry(str(onegeojson), settings['srid'])
                    request.dbsession.add(deviation_model)

            # Commit transaction
            transaction.commit()


            # Prepare mail to send
            mail_dict = Utils.create_perturbation_mail_dict(request, perturbation_record, evenement_record,
                                                            _deviation)

            # Reperages list
            reperages_string = ''
            for reperage_model in reperages_list:
                reperages_string += '<td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td>'.format(
                    '???', reperage_model.axe, reperage_model.pr_debut, reperage_model.pr_debut_distance,
                    reperage_model.pr_fin, reperage_model.pr_fin_distance)

            # Envoi email si fermeture d'urgence
            #	Envoi à la liste des personnes concernées par les fermetures d’urgence
            if urgence_updated and perturbation_record.urgence:
                mails_contacts_mails_fermeture_urgence = Utils.get_mails_contacts_mails_fermeture_urgence(
                    request)

                if mails_contacts_mails_fermeture_urgence and len(mails_contacts_mails_fermeture_urgence) > 0:
                    PTMailer.send_templated_mail(request, mails_contacts_mails_fermeture_urgence,
                                                 settings['mail_fermeture_urgence_subject'],
                                                 'email_templates:fermeture_urgence', mail_dict,
                                                 reperages_string)

            # Envoi d’emails régulier lors d’une fermeture et occupation
            contacts_a_aviser_mails_array = []

            # Envoi à la liste des personnes sélectionnées dans le formulaire
            if len(contacts_a_aviser_ids_array) > 0:
                contacts_a_aviser_mails_array = Utils.get_contacts_mails_by_ids(request, contacts_a_aviser_ids_array)

            # If Accepté → Envoi au créateur
            if etat_updated and int(etat) == int(settings['perturbation_etat_acceptee_code']):
                connected_user = LDAPQuery.get_connected_user(request)
                mail_att_name = settings['ldap_user_attribute_mail']
                if connected_user and mail_att_name in connected_user:
                    connected_user_mail = connected_user[mail_att_name]

                    if not connected_user_mail in contacts_a_aviser_mails_array:
                        contacts_a_aviser_mails_array.append(connected_user_mail)


            # If En attente → Envoi à l’approbateur = rôle trafic
            elif etat_updated and int(etat) == int(settings['perturbation_etat_attente_code']):
                contacts_a_aviser_mails_array += Utils.get_mails_of_contacts_belonging_to_a_group(request, settings[
                    'ldap_trafic_group_name'])

            # Delete duplicates from array
            contacts_a_aviser_mails_array = list(dict.fromkeys(contacts_a_aviser_mails_array))

            if contacts_a_aviser_mails_array and len(contacts_a_aviser_mails_array) > 0:
                PTMailer.send_templated_mail(request, contacts_a_aviser_mails_array,
                                             'FERMETURE' if int(perturbation_record.type) == int(
                                                 settings['fermeture_perturbation_id']) else "OCCUPATION" if int(
                                                 perturbation_record.type) == int(
                                                 settings['occupation_perturbation_id']) else 'Info',
                                             'email_templates:fermeture_occupation', mail_dict,
                                             reperages_string)

            # Envoi d’email en cas de SRB touché
            #   Envoi à la liste des personnes GMAR
            evenement_pr_touche = Utils.check_evenement_pr_touche(request, idEvenement)

            if evenement_pr_touche:
                contacts_pr_touche = Utils.get_mails_contacts_pr_touche(request)

                if contacts_pr_touche and len(contacts_pr_touche) > 0:
                    PTMailer.send_templated_mail(request, contacts_pr_touche,
                                                 settings['mail_srb_touche_subject'],
                                                 'email_templates:srb_touche', mail_dict,
                                                 reperages_string)

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except CustomError as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Etat perturbation by id view
########################################################
@view_config(route_name='etat_perturbation_by_id', request_method='GET', renderer='json')
def etat_perturbation_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.EtatPerturbation)
        result = query.filter(models.EtatPerturbation.id == request.matchdict['id']).first()

        if not result:
            raise Exception(id_not_found_exception)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Etats perturbations view
########################################################
@view_config(route_name='etats_perturbations', request_method='GET', renderer='json')
@view_config(route_name='etats_perturbations_slash', request_method='GET', renderer='json')
def etats_perturbations_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.EtatPerturbation).all()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return query



########################################################
# Perturbations impression by id
########################################################
@view_config(route_name='perturbation_impression_by_id', request_method='GET', renderer='json')
def perturbation_impression_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Check authorization
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        id = request.matchdict['id']

        # Check if the user has permission to read perturbation
        user_can_read_perturbation = Utils.user_can_read_perturbation(request, current_user_id, id)

        if not user_can_read_perturbation:
            raise HTTPForbidden()

        query = request.dbsession.query(models.PerturbationImpression).filter(models.PerturbationImpression.id == id).first()

        if not query:
            raise Exception(id_not_found_exception)

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return query.format()



########################################################
# Destinataire facturation by id view
########################################################
@view_config(route_name='destinataire_facturation_by_id', request_method='GET', renderer='json')
def destinataire_facturation_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.DestinataireFacturation)
        result = query.filter(models.DestinataireFacturation.id == request.matchdict['id']).first()

        if not result:
            raise Exception(id_not_found_exception)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Destinataires facturation view
########################################################
@view_config(route_name='destinataires_facturation', request_method='GET', renderer='json')
@view_config(route_name='destinataires_facturation_slash', request_method='GET', renderer='json')
def destinataires_facturation_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.DestinataireFacturation).all()


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return query


########################################################
# Categorie chantier by id view
########################################################
@view_config(route_name='categorie_chantier_by_id', request_method='GET', renderer='json')
def categorie_chantier_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.CategorieChantier)
        result = query.filter(models.CategorieChantier.id == request.matchdict['id']).first()

        if not result:
            raise Exception(id_not_found_exception)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Categories chantiers view
########################################################
@view_config(route_name='categories_chantiers', request_method='GET', renderer='json')
@view_config(route_name='categories_chantiers_slash', request_method='GET', renderer='json')
def categories_chantiers_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.CategorieChantier).all()


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return query


########################################################
# Type reperage by id view
########################################################
@view_config(route_name='type_reperage_by_id', request_method='GET', renderer='json')
def type_reperage_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.TypeReperage)
        result = query.filter(models.TypeReperage.id == request.matchdict['id']).first()

        if not result:
            raise Exception(id_not_found_exception)



    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Types reperages view
########################################################
@view_config(route_name='types_reperages', request_method='GET', renderer='json')
@view_config(route_name='types_reperages_slash', request_method='GET', renderer='json')
def types_reperages_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.TypeReperage).all()


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return query


########################################################
# Contact by id view
########################################################
@view_config(route_name='contact_by_id', request_method='GET', renderer='json')
def contact_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Contact)
        result = query.filter(models.Contact.id == request.matchdict['id']).first()

        if not result:
            raise Exception(id_not_found_exception)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Contacts view
########################################################
@view_config(route_name='contacts', request_method='GET', renderer='json')
@view_config(route_name='contacts_slash', request_method='GET', renderer='json')
def contacts_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Contact).all()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return query


########################################################
# Add Contact view
########################################################
@view_config(route_name='contacts', request_method='POST', renderer='json')
@view_config(route_name='contacts_slash', request_method='POST', renderer='json')
def add_contact_view(request):
    try:
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        #Check if the user has permission to add contact
        if current_user_id:
            query_permission = request.dbsession.query(models.AutorisationFonction).filter(models.AutorisationFonction.id_utilisateur == current_user_id and models.AutorisationFonction.ajouter_contact == True).first()
            if not query_permission:
                raise HTTPForbidden()


        # Default params value
        nom = None
        prenom = None
        idOrganisme = None
        mobile = None
        telephone = None
        courriel = None
        login = None
        forcerAjout = None

        # Read params
        if ('nom' in request.params):
            nom = request.params['nom']

        if ('prenom' in request.params):
            prenom = request.params['prenom']

        if ('idOrganisme' in request.params):
            idOrganisme = request.params['idOrganisme']

        if ('mobile' in request.params):
            mobile = request.params['mobile']

        if ('telephone' in request.params):
            telephone = request.params['telephone']

        if ('courriel' in request.params):
            courriel = request.params['courriel']

        if ('login' in request.params):
            login = request.params['login']

        if ('forcerAjout' in request.params):
            forcerAjout = request.params['forcerAjout']

            if forcerAjout == 'true':
                forcerAjout = True
            elif forcerAjout == 'false':
                forcerAjout = False

        # Check if contact already exists
        if not forcerAjout:
            query = request.dbsession.query(models.Contact).filter(and_(func.lower(models.Contact.prenom) == func.lower(prenom), func.lower(models.Contact.nom) == func.lower(nom), models.Contact.mobile == mobile, func.lower(models.Contact.courriel) == func.lower(courriel), func.lower(models.Contact.login) == func.lower(login))).all()

            if len(query) > 0:
                return {'error': 'true', 'code': 500, 'message': 'Contact already exists'}


        with transaction.manager as tm:
            model = models.Contact(
                id_organisme=idOrganisme,
                login=login,
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                mobile=mobile,
                courriel=courriel)

            request.dbsession.add(model)
            transaction.commit()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Update Contact view
########################################################
@view_config(route_name='contacts', request_method='PUT', renderer='json')
@view_config(route_name='contacts_slash', request_method='PUT', renderer='json')
def update_contact_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id is None:
            raise HTTPForbidden()

        # Check if the user has permission to modify contact
        query_permission = request.dbsession.query(models.AutorisationFonction).filter(
            models.AutorisationFonction.id_utilisateur == current_user_id and models.AutorisationFonction.modifier_contact == True).first()
        if not query_permission:
            raise HTTPForbidden()


        # Default params value
        id = None
        nom = None
        prenom = None
        idOrganisme = None
        mobile = None
        telephone = None
        courriel = None
        login = None

        # Read params
        if ('id' in request.params and request.params['id'] != ''):
            id = request.params['id']

        if ('nom' in request.params):
            nom = request.params['nom']

        if ('prenom' in request.params):
            prenom = request.params['prenom']

        if ('idOrganisme' in request.params):
            idOrganisme = request.params['idOrganisme']

        if ('mobile' in request.params):
            mobile = request.params['mobile']

        if ('telephone' in request.params):
            telephone = request.params['telephone']

        if ('courriel' in request.params):
            courriel = request.params['courriel']

        if ('login' in request.params):
            login = request.params['login']

        with transaction.manager as tm:
            contact_query = request.dbsession.query(models.Contact).filter(models.Contact.id == id)

            if contact_query.count() > 0:
                contact_record = contact_query.first()
                contact_record.id_organisme = idOrganisme
                contact_record.login = login
                contact_record.nom = nom
                contact_record.prenom = prenom
                contact_record.telephone = telephone
                contact_record.courriel = courriel

                transaction.commit()
            else:
                raise Exception(id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Delete contact by id view
########################################################
@view_config(route_name='contact_by_id', request_method='DELETE', renderer='json')
def delete_contact_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id is None:
            raise HTTPForbidden()

        # Check if the user has permission to delete contact
        query_permission = request.dbsession.query(models.AutorisationFonction).filter(
            models.AutorisationFonction.id_utilisateur == current_user_id and models.AutorisationFonction.supprimer_contact == True).first()
        if not query_permission:
            raise HTTPForbidden()


        id = request.matchdict['id']

        query = request.dbsession.query(models.Contact)
        contact = query.filter(models.Contact.id == id).first()

        if not contact:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Contact having login
########################################################
@view_config(route_name='contacts_having_login', request_method='GET', renderer='json')
@view_config(route_name='contacts_having_login_slash', request_method='GET', renderer='json')
def contacts_having_login_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Contact, models.Organisme).filter(models.Contact.id_organisme == models.Organisme.id).filter(models.Contact.login.isnot(None)).all()
        result = []

        for contact, organisme in query:
            contact_json = contact.format()
            contact_json['nom_organisme'] = organisme.nom

            # Entites
            query_entites = request.dbsession.query(models.LienContactEntite, models.Entite).filter(models.LienContactEntite.id_contact == contact.id).filter(models.LienContactEntite.id_entite == models.Entite.id).all()

            entites = []
            for le, e in query_entites:
                entites.append(e.nom)


            #Roles
            query_roles = request.dbsession.query(models.FonctionContact.fonction).filter(
                models.FonctionContact.id_contact == contact.id).all()

            roles = []
            for fc in query_roles:
                roles.append(fc.fonction)

            contact_json['entites'] = entites
            contact_json['roles'] = roles
            result.append(contact_json)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return result

########################################################
# Contacts by entite view
########################################################
@view_config(route_name='contacts_entite', request_method='GET', renderer='json')
@view_config(route_name='contacts_entite_slash', request_method='GET', renderer='json')
def contacts_entite_view(request):
    entite_err_msg = 'idEntite parameter is empty'
    result = []
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        idEntite = None

        if ('idEntite' in request.params):
            idEntite = request.params['idEntite']

        if idEntite is None:
            raise Exception(entite_err_msg)


        query = request.dbsession.query(models.Contact, models.LienContactEntite).filter(models.Contact.id == models.LienContactEntite.id_contact).filter(models.LienContactEntite.id_entite == idEntite).all()

        for c, lce in query:
            result.append(c.format())

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': entite_err_msg if str(e) == entite_err_msg else general_exception}

    return result


########################################################
# Get Contact_potentiel_avis_perturbation view
########################################################
@view_config(route_name='contacts_potentiels_avis_perturbation', request_method='GET', renderer='json')
@view_config(route_name='contacts_potentiels_avis_perturbation_slash', request_method='GET', renderer='json')
def contact_potentiel_avis_perturbation_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        result = []

        for cp, c, o in request.dbsession.query(models.ContactPotentielAvisPerturbation, models.Contact, models.Organisme).filter(
                models.ContactPotentielAvisPerturbation.id_contact == models.Contact.id).filter(
                models.Contact.id_organisme == models.Organisme.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return result


########################################################
# Add Contact_potentiel_avis_perturbation view
########################################################
@view_config(route_name='contacts_potentiels_avis_perturbation', request_method='POST', renderer='json')
@view_config(route_name='contacts_potentiels_avis_perturbation_slash', request_method='POST', renderer='json')
def add_contact_potentiel_avis_perturbation_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        idEntite = None
        idContact = None
        envoiAutoOccupation = None
        envoiAutoFermeture = None

        # Read params
        if ('idEntite' in request.params):
            idEntite = request.params['idEntite']

        if ('idContact' in request.params):
            idContact = request.params['idContact']

        if ('envoiAutoOccupation' in request.params):
            envoiAutoOccupation = request.params['envoiAutoOccupation']

            if envoiAutoOccupation == 'true':
                envoiAutoOccupation = True
            elif envoiAutoOccupation == 'false':
                envoiAutoOccupation = False

        if ('envoiAutoFermeture' in request.params):
            envoiAutoFermeture = request.params['envoiAutoFermeture']

            if envoiAutoFermeture == 'true':
                envoiAutoFermeture = True
            elif envoiAutoFermeture == 'false':
                envoiAutoFermeture = False

        with transaction.manager as tm:
            model = models.ContactPotentielAvisPerturbation(
                id_entite=idEntite,
                id_contact=idContact,
                envoi_auto_occupation=envoiAutoOccupation,
                envoi_auto_fermeture=envoiAutoFermeture)

            request.dbsession.add(model)
            transaction.commit()


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Update Contact_potentiel_avis_perturbation view
########################################################
@view_config(route_name='contacts_potentiels_avis_perturbation', request_method='PUT', renderer='json')
@view_config(route_name='contacts_potentiels_avis_perturbation_slash', request_method='PUT', renderer='json')
def update_contact_potentiel_avis_perturbation_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        id = None
        idEntite = None
        idContact = None
        envoiAutoOccupation = None
        envoiAutoFermeture = None

        # Read params
        if ('id' in request.params and request.params['id'] != ''):
            id = request.params['id']

        if ('idEntite' in request.params):
            idEntite = request.params['idEntite']

        if ('idContact' in request.params):
            idContact = request.params['idContact']

        if ('envoiAutoOccupation' in request.params):
            envoiAutoOccupation = request.params['envoiAutoOccupation']

            if envoiAutoOccupation == 'true':
                envoiAutoOccupation = True
            elif envoiAutoOccupation == 'false':
                envoiAutoOccupation = False

        if ('envoiAutoFermeture' in request.params):
            envoiAutoFermeture = request.params['envoiAutoFermeture']

            if envoiAutoFermeture == 'true':
                envoiAutoFermeture = True
            elif envoiAutoFermeture == 'false':
                envoiAutoFermeture = False

        with transaction.manager as tm:
            contact_query = request.dbsession.query(models.ContactPotentielAvisPerturbation).filter(
                models.ContactPotentielAvisPerturbation.id == id)

            if contact_query.count() > 0:
                contact_record = contact_query.first()
                contact_record.id_entite = idEntite
                contact_record.id_contact = idContact
                contact_record.envoi_auto_occupation = envoiAutoOccupation
                contact_record.envoi_auto_fermeture = envoiAutoFermeture

                transaction.commit()
            else:
                raise Exception(id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Delete Contact_potentiel_avis_perturbation by id view
########################################################
@view_config(route_name='contacts_potentiels_avis_perturbation_by_id', request_method='DELETE', renderer='json')
def delete_contact_potentiels_avis_perturbation_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        query = request.dbsession.query(models.ContactPotentielAvisPerturbation)
        contact = query.filter(models.ContactPotentielAvisPerturbation.id == id).first()

        if not contact:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Get Contact_potentiel_avis_perturbation view
########################################################
@view_config(route_name='contacts_avis_fermeture_urgence', request_method='GET', renderer='json')
@view_config(route_name='contacts_avis_fermeture_urgence_slash', request_method='GET', renderer='json')
def contact_avis_fermeture_urgence_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        result = []

        for cp, c, o in request.dbsession.query(models.ContactAvisFermetureUrgence, models.Contact, models.Organisme).filter(
                models.ContactAvisFermetureUrgence.id_contact == models.Contact.id).filter(
                models.Contact.id_organisme == models.Organisme.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return result


########################################################
# Add Contact_avis_fermeture_urgence view
########################################################
@view_config(route_name='contacts_avis_fermeture_urgence', request_method='POST', renderer='json')
@view_config(route_name='contacts_avis_fermeture_urgence_slash', request_method='POST', renderer='json')
def add_avis_fermeture_urgence_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        idContact = None

        # Read params
        if ('idContact' in request.params):
            idContact = request.params['idContact']

        #Check if contact already exists
        contact_query = request.dbsession.query(models.ContactAvisFermetureUrgence).filter(
            models.ContactAvisFermetureUrgence.id_contact == idContact)

        if contact_query.count() > 0:
            return {'message': 'Data successfully saved'}

        with transaction.manager as tm:
            model = models.ContactAvisFermetureUrgence(
                id_contact=idContact)

            request.dbsession.add(model)
            transaction.commit()


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Update Contact_avis_fermeture_urgence view
########################################################
@view_config(route_name='contacts_avis_fermeture_urgence', request_method='PUT', renderer='json')
@view_config(route_name='contacts_avis_fermeture_urgence_slash', request_method='PUT', renderer='json')
def update_avis_fermeture_urgence_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        id = None
        idContact = None

        # Read params
        if ('id' in request.params and request.params['id'] != ''):
            id = request.params['id']

        if ('idContact' in request.params):
            idContact = request.params['idContact']

        with transaction.manager as tm:
            contact_query = request.dbsession.query(models.ContactAvisFermetureUrgence).filter(
                models.ContactAvisFermetureUrgence.id == id)

            if contact_query.count() > 0:
                contact_record = contact_query.first()
                contact_record.id_contact = idContact

                transaction.commit()
            else:
                raise Exception(id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Delete contacts_avis_fermeture_urgence by id view
########################################################
@view_config(route_name='contacts_avis_fermeture_urgence_by_id', request_method='DELETE', renderer='json')
def delete_avis_fermeture_urgence_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        query = request.dbsession.query(models.ContactAvisFermetureUrgence)
        contact = query.filter(models.ContactAvisFermetureUrgence.id == id).first()

        if not contact:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Get contact_avis_pr_touche view
########################################################
@view_config(route_name='contact_avis_pr_touche', request_method='GET', renderer='json')
@view_config(route_name='contact_avis_pr_touche_slash', request_method='GET', renderer='json')
def contact_avis_pr_touche_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        result = []

        for cp, c, o in request.dbsession.query(models.ContactAvisPrTouche, models.Contact, models.Organisme).filter(
                models.ContactAvisPrTouche.id_contact == models.Contact.id).filter(
                models.Contact.id_organisme == models.Organisme.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return result


########################################################
# Add Contact_avis_pr_touche view
########################################################
@view_config(route_name='contact_avis_pr_touche', request_method='POST', renderer='json')
@view_config(route_name='contact_avis_pr_touche_slash', request_method='POST', renderer='json')
def add_contact_avis_pr_touche_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        idContact = None

        # Read params
        if ('idContact' in request.params):
            idContact = request.params['idContact']

        # Check if contact already exists
        contact_query = request.dbsession.query(models.ContactAvisPrTouche).filter(
            models.ContactAvisPrTouche.id_contact == idContact)

        if contact_query.count() > 0:
            return {'message': 'Data successfully saved'}

        with transaction.manager as tm:
            model = models.ContactAvisPrTouche(
                id_contact=idContact)

            request.dbsession.add(model)
            transaction.commit()


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Update Contact_avis_pr_touche view
########################################################
@view_config(route_name='contact_avis_pr_touche', request_method='PUT', renderer='json')
@view_config(route_name='contact_avis_pr_touche_slash', request_method='PUT', renderer='json')
def update_avis_fermeture_urgence_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        id = None
        idContact = None

        # Read params
        if ('id' in request.params and request.params['id'] != ''):
            id = request.params['id']

        if ('idContact' in request.params):
            idContact = request.params['idContact']

        with transaction.manager as tm:
            contact_query = request.dbsession.query(models.ContactAvisPrTouche).filter(
                models.ContactAvisPrTouche.id == id)

            if contact_query.count() > 0:
                contact_record = contact_query.first()
                contact_record.id_contact = idContact

                transaction.commit()
            else:
                raise Exception(id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Delete Contact_avis_pr_touche_by_id by id view
########################################################
@view_config(route_name='contact_avis_pr_touche_by_id', request_method='DELETE', renderer='json')
def delete_contact_avis_pr_touche_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        query = request.dbsession.query(models.ContactAvisPrTouche)
        contact = query.filter(models.ContactAvisPrTouche.id == id).first()

        if not contact:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}



########################################################
# Organisme by id view
########################################################
@view_config(route_name='organisme_by_id', request_method='GET', renderer='json')
def organisme_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Organisme)
        result = query.filter(models.Organisme.id == request.matchdict['id']).first()

        if not result:
            raise Exception(id_not_found_exception)

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return result


########################################################
# Suggestion by liste name view
########################################################
@view_config(route_name='suggestion_by_liste_name', request_method='GET', renderer='json')
def suggestion_by_liste_name_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Suggestion).filter(models.Suggestion.liste == request.matchdict['id']).all()

        if not query:
            raise Exception(id_not_found_exception)

        else:
            array = []
            for item in query:
              array.append(item.valeur)
            return array

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return []

########################################################
# Organismes view
########################################################
@view_config(route_name='organismes', request_method='GET', renderer='json')
@view_config(route_name='organismes_slash', request_method='GET', renderer='json')
def organismes_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Organisme).all()


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return query


########################################################
# Add organisme view
########################################################
@view_config(route_name='organismes', request_method='POST', renderer='json')
@view_config(route_name='organismes_slash', request_method='POST', renderer='json')
def add_organisme_view(request):
    try:

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        nom = None
        adresse = None
        localite = None
        telephone = None
        fax = None
        courriel = None
        forcerAjout = None

        # Read params
        if ('nom' in request.params):
            nom = request.params['nom']

        if ('adresse' in request.params):
            adresse = request.params['adresse']

        if ('localite' in request.params):
            localite = request.params['localite']

        if ('telephone' in request.params):
            telephone = request.params['telephone']

        if ('fax' in request.params):
            fax = request.params['fax']

        if ('courriel' in request.params):
            courriel = request.params['courriel']

        # Check if force ajout
        if ('forcerAjout' in request.params):
            forcerAjout = request.params['forcerAjout']

            if forcerAjout == 'true':
                forcerAjout = True
            elif forcerAjout == 'false':
                forcerAjout = False

        # Check if contact already exists
        if not forcerAjout:
            query = request.dbsession.query(models.Organisme).filter(or_(
                func.lower(models.Organisme.nom) == func.lower(nom), and_(models.Organisme.telephone == telephone, models.Organisme.telephone != None), and_(models.Organisme.fax == fax, models.Organisme.fax != None),
                and_(func.lower(models.Organisme.courriel) == func.lower(courriel), models.Organisme.courriel != None))).all()

            if len(query) > 0:
                return {'error': 'true', 'code': 500, 'message': 'Organisme already exists'}

        with transaction.manager as tm:
            model = models.Organisme(
                nom=nom,
                adresse=adresse,
                localite=localite,
                telephone=telephone,
                fax=fax,
                courriel=courriel)

            request.dbsession.add(model)
            transaction.commit()


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Update organisme view
########################################################
@view_config(route_name='organismes', request_method='PUT', renderer='json')
@view_config(route_name='organismes_slash', request_method='PUT', renderer='json')
def update_organisme_view(request):
    try:

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        # Default params value
        id = None
        nom = None
        adresse = None
        localite = None
        telephone = None
        fax = None
        courriel = None

        # Read params
        if ('id' in request.params and request.params['id'] != ''):
            id = request.params['id']

        if ('nom' in request.params):
            nom = request.params['nom']

        if ('adresse' in request.params):
            adresse = request.params['adresse']

        if ('localite' in request.params):
            localite = request.params['localite']

        if ('telephone' in request.params):
            telephone = request.params['telephone']

        if ('fax' in request.params):
            fax = request.params['fax']

        if ('courriel' in request.params):
            courriel = request.params['courriel']

        query = request.dbsession.query(models.Organisme).filter(models.Organisme.id == id)

        with transaction.manager as tm:
            if query.count() > 0:
                record = query.first()
                record.nom = nom
                record.adresse = adresse
                record.localite = localite
                record.telephone = telephone
                record.fax = fax
                record.courriel = courriel

                transaction.commit()
            else:
                raise Exception(id_not_found_exception)

    except Exception as e:
        tm.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Delete organisme by id view
########################################################
@view_config(route_name='organisme_by_id', request_method='DELETE', renderer='json')
def delete_organisme_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        query = request.dbsession.query(models.Organisme)
        organisme = query.filter(models.Organisme.id == id).first()

        if not organisme:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(organisme)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Axes routiers view
########################################################
@view_config(route_name='axes_routiers', request_method='GET', renderer='json')
@view_config(route_name='axes_routiers_slash', request_method='GET', renderer='json')
def axes_routiers_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        return request.dbsession.query(models.Axe).all()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return []


########################################################
# PR par axe routier view
########################################################
@view_config(route_name='pr_par_axe_routier', request_method='GET', renderer='json')
@view_config(route_name='pr_par_axe_routier_slash', request_method='GET', renderer='json')
def pr_par_axe_routier_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        if ('id' in request.params):
            query = request.dbsession.query(models.Secteur).filter(models.Secteur.axe_nom_complet == request.params['id']).all()

            if query:
                result = []

                for item in query:
                    result.append(item.format())

                return result

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return []


########################################################
# Plans types chantiers view
########################################################
@view_config(route_name='plans_types_fouille', request_method='GET', renderer='json')
@view_config(route_name='plans_types_fouille_slash', request_method='GET', renderer='json')
def plans_types_fouille_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.PlanTypeFouille).all()


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return query



########################################################
# Evenements XML
########################################################
@view_config(route_name='evenements_xml', request_method='GET', renderer='json')
@view_config(route_name='evenements_xml_slash', request_method='GET', renderer='json')
def evenements_xml_view(request):
    try:
        files_array = EvenementXML.list_folder_files(request)
        successful_files = []
        failed_files = []

        for file in files_array:
            file_json = EvenementXML.xml_to_json(file)
      
            if file_json:
                is_added = EvenementXML.add_file_data(file_json)

                if is_added:
                    successful_files.append(file)

                    # Remove file if is added
                    EvenementXML.remove_file(request, file)

                else:
                    failed_files.append(file)


    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'successful_files' : successful_files, 'failed_files' : failed_files}


########################################################
# Login
########################################################
@view_config(route_name='login', request_method='POST', renderer='json')
@view_config(route_name='login_slash', request_method='POST', renderer='json')
def login_view(request):
    response = None
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        login = None
        password = None

        if 'login' in request.params:
            login = request.params['login']

        if 'password' in request.params:
            password = request.params['password']

        #Check if user exists in DB
        query = request.dbsession.query(models.Contact)
        contact = query.filter(func.lower(models.Contact.login) == func.lower(login)).first()

        if not contact:
            raise Exception(user_not_found_exception)

        # Check if user exists in LDAP
        else:
            entites = []
            for lce, e in request.dbsession.query(models.LienContactEntite, models.Entite).filter(models.LienContactEntite.id_contact == contact.id).filter(models.Entite.id == models.LienContactEntite.id_entite).all():
                entites.append(e.format())

            response = LDAPQuery.do_login(request, login, password, contact, entites)

    except Exception as error:
        log.error(str(error))
        request.response.status = 403
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return response


########################################################
# Logout
########################################################
@view_config(route_name='logout', request_method='GET', renderer='json')
def logout_view(request):
    response = None
    try:
        response = LDAPQuery.do_logout(request)

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return response



########################################################
# Logged user
########################################################
@view_config(route_name='logged_user', request_method='GET', renderer='json')
@view_config(route_name='logged_user_slash', request_method='GET', renderer='json')
def logged_user_view(request):
    contact_json = None
    try:
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id:
            # Check if user exists in DB
            query = request.dbsession.query(models.Contact)
            contact = query.filter(models.Contact.id == current_user_id).first()

            if not contact:
                raise Exception(user_not_found_exception)

            # Entites
            entites = []
            for lce, e in request.dbsession.query(models.LienContactEntite, models.Entite).filter(
                    models.LienContactEntite.id_contact == contact.id).filter(
                    models.Entite.id == models.LienContactEntite.id_entite).all():
                entites.append(e.format())

            contact_json = contact.format()
            contact_json['entites'] = entites
        else:
            raise Exception(user_not_found_exception)

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return contact_json



########################################################
# Entites
########################################################
@view_config(route_name='entites', request_method='GET', renderer='json')
@view_config(route_name='entites_slash', request_method='GET', renderer='json')
def entites_view(request):
    entites = []
    try:
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id:
            for lce, e in request.dbsession.query(models.LienContactEntite, models.Entite).filter(models.LienContactEntite.id_contact == current_user_id).filter(models.Entite.id == models.LienContactEntite.id_entite).all():
                entites.append(e.format())

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return entites




########################################################
# Get nouveaux contacts AD
########################################################
@view_config(route_name='nouveaux_contacts_ad', request_method='GET', renderer='json')
@view_config(route_name='nouveaux_contacts_ad_slash', request_method='GET', renderer='json')
def get_nouveaux_contacts_ad_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        auth_tkt = request.cookies.get('auth_tkt', default=None)
        group_id_attribute = settings['ldap_group_attribute_id']
        group_name_attribute = settings['ldap_group_attribute_name']
        ldap_entite_groups_prefix = settings['ldap_entite_groups_prefix']
        ldap_fonction_groups_prefix = settings['ldap_fonction_groups_prefix']
        login_attr = settings['ldap_user_attribute_login']

        if not auth_tkt:
            raise HTTPForbidden()

        # Logins from AD
        contacts_ad_json = LDAPQuery.get_users_belonging_to_group_entites(request)

        # Logins from DB
        contacts_bd_logins = []
        contacts_bd_logins_query = request.dbsession.query(models.Contact).distinct(models.Contact.login).filter(models.Contact.login.isnot(None)).all()
        for c in contacts_bd_logins_query:
            contacts_bd_logins.append(c.login.upper())

        result = []

        for one_contact_ad_json in contacts_ad_json:
            if one_contact_ad_json and login_attr in one_contact_ad_json:
                if one_contact_ad_json[login_attr].upper() not in contacts_bd_logins:
                    groups  = LDAPQuery.get_user_groups_by_dn(request, one_contact_ad_json['dn'])

                    entites = [{'id': x[group_id_attribute], 'name': x[group_name_attribute]} for x in groups if
                               group_id_attribute in x and x[group_id_attribute].startswith(ldap_entite_groups_prefix)]

                    roles = [{'id': x[group_id_attribute], 'name': x[group_name_attribute]} for x in groups if
                               group_id_attribute in x and x[group_id_attribute].startswith(ldap_fonction_groups_prefix)]

                    one_contact_ad_json['entites'] = entites
                    one_contact_ad_json['roles'] = roles
                    result.append(one_contact_ad_json)


    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return result


########################################################
# Add nouveaux contacts AD
########################################################
@view_config(route_name='nouveaux_contacts_ad', request_method='POST', renderer='json')
@view_config(route_name='nouveaux_contacts_ad_slash', request_method='POST', renderer='json')
def add_nouveaux_contacts_ad_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        auth_tkt = request.cookies.get('auth_tkt', default=None)
        login_attr = settings['ldap_user_attribute_login']

        if not auth_tkt:
            raise HTTPForbidden()

        contacts_ad_json = None

        if 'contacts' in request.params:
            contacts_ad_json = request.params['contacts']

        if contacts_ad_json is None:
            raise Exception('Parameter contacts is empty')

        # Mise à jour groupes AD
        is_groupes_ad_mis_a_jour = Utils.mise_a_jour_groupes_ad(request)

        if is_groupes_ad_mis_a_jour:

            contacts_ad_json = json.loads(contacts_ad_json)

            # Get all entités
            entites = {}
            entites_query = request.dbsession.query(models.Entite).all()
            for e in entites_query:
                entites[e.nom_groupe_ad] = e.id


            for one_contact_ad_json in contacts_ad_json:

                with transaction.manager as tm:
                    # Add contact to DB
                    contact_model = models.Contact(
                        id_organisme=one_contact_ad_json['id_organisme'],
                        login=one_contact_ad_json[settings['ldap_user_attribute_login']],
                        nom=one_contact_ad_json[settings['ldap_user_attribute_lastname']],
                        prenom=one_contact_ad_json[settings['ldap_user_attribute_firstname']],
                        telephone=one_contact_ad_json[settings['ldap_user_attribute_telephone']],
                        #mobile=one_contact_ad_json[settings['ldap_user_attribute_mobile']],
                        courriel=one_contact_ad_json[settings['ldap_user_attribute_mail']])

                    request.dbsession.add(contact_model)
                    request.dbsession.flush()
                    max_contact_id = contact_model.id

                    # Add entites groups
                    groupes_entites = one_contact_ad_json['entites'] if 'entites' in one_contact_ad_json else None

                    if groupes_entites is not None and len(groupes_entites) > 0:
                        for one_contact_ldap_group_item in groupes_entites:
                            one_contact_ldap_group_id = one_contact_ldap_group_item['id']
                            one_contact_ldap_group_name = one_contact_ldap_group_item['name']

                            #Entite group
                            if one_contact_ldap_group_id.startswith(settings['ldap_entite_groups_prefix']):
                                id_entite = entites[one_contact_ldap_group_id] if entites and one_contact_ldap_group_id in entites else None

                                #If entite does not exist
                                if id_entite is None:
                                    entite_model = models.Entite(
                                        nom=one_contact_ldap_group_name,
                                        id_responsable=settings['id_responsable_entite'],
                                        nom_groupe_ad=one_contact_ldap_group_id
                                    )
                                    request.dbsession.add(entite_model)
                                    request.dbsession.flush()
                                    id_entite = entite_model.id

                                if id_entite is not None:
                                    lien_entite_contact_model = models.LienContactEntite(
                                        id_contact=max_contact_id,
                                        id_entite=id_entite
                                    )
                                    request.dbsession.add(lien_entite_contact_model)

                    # Add Fonction group
                    groupes_fonctions = one_contact_ad_json['roles'] if 'roles' in one_contact_ad_json else None

                    if groupes_fonctions is not None and len(groupes_fonctions) > 0:
                        for one_contact_ldap_group_item in groupes_fonctions:
                            one_contact_ldap_group_id = one_contact_ldap_group_item['id']

                            fonction_contact_model = models.FonctionContact(
                                id_contact=max_contact_id,
                                fonction=one_contact_ldap_group_id
                            )
                            request.dbsession.add(fonction_contact_model)

                    transaction.commit()


    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Mise a jour des groupes AD
########################################################
@view_config(route_name='mise_a_jours_groupes_ad', request_method='GET', renderer='json')
@view_config(route_name='mise_a_jours_groupes_ad_slash', request_method='GET', renderer='json')
def mise_a_jours_groupes_ad_view(request):

    result = {'message': 'AD groups updated'}

    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        """
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()
        """

        is_groupes_ad_mis_a_jour = Utils.mise_a_jour_groupes_ad(request)

        if not is_groupes_ad_mis_a_jour:
            raise Exception('An error occured while updating AD groups')

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return result



########################################################
# Autorisations accordees
########################################################
@view_config(route_name='autorisations_accordees', request_method='GET', renderer='json')
@view_config(route_name='autorisations_accordees_slash', request_method='GET', renderer='json')
def autorisations_accordees_view(request):
    result = []
    entite_err_msg = 'idEntite parameter is empty'
    try:
        auth_tkt = request.cookies.get('auth_tkt', default=None)
        idEntite = None

        if not auth_tkt:
            raise HTTPForbidden()

        if ('idEntite' in request.params):
            idEntite = request.params['idEntite']

        if idEntite is None:
            raise Exception(entite_err_msg)

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id:

            for d, c, o, lce in request.dbsession.query(models.Delegation, models.Contact,
                                                   models.Organisme, models.LienContactEntite).filter(
                models.Delegation.id_delegant == current_user_id).filter(
                models.Contact.id == models.Delegation.id_delegataire).filter(
                models.Contact.id_organisme == models.Organisme.id).filter(
                models.LienContactEntite.id_entite == idEntite).filter(
                models.Delegation.id_delegataire == models.LienContactEntite.id_contact).all():
                result.append(d.format(c.nom, c.prenom, o.nom))

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500,
                'message': entite_err_msg if str(error) == entite_err_msg else general_exception}

    return result


#######################################################
# Autorisations recues
########################################################
@view_config(route_name='autorisations_recues', request_method='GET', renderer='json')
@view_config(route_name='autorisations_recues_slash', request_method='GET', renderer='json')
def autorisations_recues_view(request):
    result = []
    try:
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id:

            for d, c, o in request.dbsession.query(models.Delegation, models.Contact,
                                                    models.Organisme).filter(
                models.Delegation.id_delegataire == current_user_id).filter(
                models.Contact.id == models.Delegation.id_delegant).filter(
                models.Contact.id_organisme == models.Organisme.id).all():
                result.append(d.format(c.nom, c.prenom, o.nom))

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return result



########################################################
# Add autorisation
########################################################
@view_config(route_name='autorisations', request_method='POST', renderer='json')
@view_config(route_name='autorisations_slash', request_method='POST', renderer='json')
def add_autorisations_view(request):
    try:

        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id:

            # Params
            idDelegataire = None
            autorisationLecture = None
            autorisationModification = None
            autorisationSuppression = None


            with transaction.manager:

                if 'idDelegataire' in request.params:
                    idDelegataire = request.params['idDelegataire']

                if 'autorisationLecture' in request.params:
                    autorisationLecture = request.params['autorisationLecture']

                    if autorisationLecture == 'true':
                        autorisationLecture = True
                    elif autorisationLecture == 'false':
                        autorisationLecture = False
                    else:
                        autorisationLecture = None


                if 'autorisationModification' in request.params:
                    autorisationModification = request.params['autorisationModification']

                    if autorisationModification == 'true':
                        autorisationModification = True
                    elif autorisationModification == 'false':
                        autorisationModification = False
                    else:
                        autorisationModification = None


                if 'autorisationSuppression' in request.params:
                    autorisationSuppression = request.params['autorisationSuppression']

                    if autorisationSuppression == 'true':
                        autorisationSuppression = True
                    elif autorisationSuppression == 'false':
                        autorisationSuppression = False
                    else:
                        autorisationSuppression = None

                model =  models.Delegation(
                    id_delegant=current_user_id,
                    id_delegataire=idDelegataire,
                    autorisation_lecture=autorisationLecture,
                    autorisation_modification=autorisationModification,
                    autorisation_suppression=autorisationSuppression)

                request.dbsession.add(model)

                transaction.commit()


    except HTTPForbidden as e:
        raise HTTPForbidden()


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {'message': 'Data successfully saved'}



########################################################
# Update autorisation
########################################################
@view_config(route_name='autorisations', request_method='PUT', renderer='json')
@view_config(route_name='autorisations_slash', request_method='PUT', renderer='json')
def update_autorisations_view(request):
    try:

        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id:

            # Params
            idDelegation = None
            idDelegataire = None
            autorisationLecture = None
            autorisationModification = None
            autorisationSuppression = None

            if 'idDelegation' in request.params:
                idDelegation = request.params['idDelegation']
                delegation_record = request.dbsession.query(models.Delegation).filter(models.Delegation.id == idDelegation).first()

                if delegation_record == None :
                    raise Exception(id_not_found_exception)

                with transaction.manager:

                    if 'idDelegataire' in request.params:
                        idDelegataire = request.params['idDelegataire']
                        delegation_record.id_delegataire = idDelegataire

                    if 'autorisationLecture' in request.params:
                        autorisationLecture = request.params['autorisationLecture']

                        if autorisationLecture == 'true':
                            autorisationLecture = True
                        elif autorisationLecture == 'false':
                            autorisationLecture = False
                        else:
                            autorisationLecture = None

                        delegation_record.autorisation_lecture = autorisationLecture

                    if 'autorisationModification' in request.params:
                        autorisationModification = request.params['autorisationModification']

                        if autorisationModification == 'true':
                            autorisationModification = True
                        elif autorisationModification == 'false':
                            autorisationModification = False
                        else:
                            autorisationModification = None

                        delegation_record.autorisation_modification = autorisationModification

                    if 'autorisationSuppression' in request.params:
                        autorisationSuppression = request.params['autorisationSuppression']

                        if autorisationSuppression == 'true':
                            autorisationSuppression = True
                        elif autorisationSuppression == 'false':
                            autorisationSuppression = False
                        else:
                            autorisationSuppression = None

                        delegation_record.autorisation_suppression = autorisationSuppression

                    transaction.commit()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return {'message': 'Data successfully saved'}


########################################################
# Delete delegation by id
########################################################
@view_config(route_name='autorisation_by_id', request_method='DELETE', renderer='json')
def delete_autorisation_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        id = request.matchdict['id']

        query = request.dbsession.query(models.Delegation)
        delegation = query.filter(models.Delegation.id == id).first()

        if not delegation:
            raise Exception(id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(delegation)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': id_not_found_exception if str(e) == id_not_found_exception else general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Autorisations fonctions
########################################################
@view_config(route_name='autorisations_fonctions', request_method='GET', renderer='json')
@view_config(route_name='autorisations_fonctions_slash', request_method='GET', renderer='json')
def autorisations_fonctions_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)

        query = request.dbsession.query(models.AutorisationFonction).filter(models.AutorisationFonction.id_utilisateur == current_user_id).first()
        return query
    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return {}


########################################################
# LDAP users
########################################################
@view_config(route_name='ldap_users', request_method='GET', renderer='json')
@view_config(route_name='ldap_users_slash', request_method='GET', renderer='json')
def ldap_users_view(request):
    try:
        settings = request.registry.settings


    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return "okkkk"



########################################################
# Localites npa
########################################################
@view_config(route_name='localites_npa', request_method='GET', renderer='json')
@view_config(route_name='localites_npa_slash', request_method='GET', renderer='json')
def localites_npa_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Localite).all()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return query

########################################################
# Localités view
########################################################
@view_config(route_name='localites', request_method='GET', renderer='json')
@view_config(route_name='localites_slash', request_method='GET', renderer='json')
def localites_view(request):
    try:
        settings = request.registry.settings

        # Localités
        typename = settings['localites_typename']
        propertyname = settings['localites_propertyname']
        localites_return_template = settings['localites_return_template']

        query = WFSQuery.do_query_wfs(request,
                                      typename,
                                      propertyname,
                                      None,
                                      localites_return_template,
                                      None)

        if not query:
            return []

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return query


########################################################
# Cadastre view
########################################################
@view_config(route_name='cadastre', request_method='GET', renderer='json')
@view_config(route_name='cadastre_slash', request_method='GET', renderer='json')
def cadastre_view(request):
    try:
        settings = request.registry.settings

        # Cadastre
        typename = settings['cadastre_typename']
        propertyname = settings['cadastre_propertyname']
        cadastre_return_template = settings['cadastre_return_template']

        query = WFSQuery.do_query_wfs(request,
                                      typename,
                                      propertyname,
                                      None,
                                      cadastre_return_template,
                                      None)

        if not query:
            return []

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return query


########################################################
# Communes
########################################################
@view_config(route_name='communes', request_method='GET', renderer='json')
@view_config(route_name='communes_slash', request_method='GET', renderer='json')
def communes_view(request):
    try:
        settings = request.registry.settings

        # Communes
        typename = settings['communes_typename']
        propertyname = settings['communes_propertyname']
        communes_return_template = settings['communes_return_template']

        query = WFSQuery.do_query_wfs(request,
                                      typename,
                                      propertyname,
                                      None,
                                      communes_return_template,
                                      None)

        if not query:
            return []

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500, 'message': general_exception}
    return query


########################################################
# Get geometry from reperage
########################################################
@view_config(route_name='geometry_reperage', request_method='GET', renderer='json')
@view_config(route_name='geometry_reperage_slash', request_method='GET', renderer='json')
def geometry_reperage_view(request):
    try:
        settings = request.registry.settings

        vmdeport_ws_url = settings['vmdeport_ws_url']
        params = "f_prop={1}&f_axe={2}&f_sens={3}&f_pr_d={4}&f_pr_f={5}&f_dist_d={6}&f_dist_f={7}&f_ecart_d={8}&f_ecart_f={9}&f_usaneg={10}"

        f_prop = None
        f_axe = None
        f_sens = None
        f_pr_d = None
        f_pr_f = None
        f_dist_d = None
        f_dist_f = None
        f_ecart_d = None
        f_ecart_f = None
        f_usaneg = None
        f_geomAsBin = None

        if 'f_prop' in request.params:
            f_prop = request.params['f_prop']

        if 'f_axe' in request.params:
            f_axe = request.params['f_axe']

        if 'f_sens' in request.params:
            f_sens = request.params['f_sens']

        if 'f_pr_d' in request.params:
            f_pr_d = request.params['f_pr_d']

        if 'f_pr_f' in request.params:
            f_pr_f = request.params['f_pr_f']

        if 'f_dist_d' in request.params:
            f_dist_d = request.params['f_dist_d']

        if 'f_dist_f' in request.params:
            f_dist_f = request.params['f_dist_f']

        if 'f_ecart_d' in request.params:
            f_ecart_d = request.params['f_ecart_d']

        if 'f_ecart_f' in request.params:
            f_ecart_f = request.params['f_ecart_f']

        if 'f_usaneg' in request.params:
            f_usaneg = request.params['f_usaneg']

        # if 'f_geomAsBin' in request.params:
        # f_geomAsBin = request.params['f_geomAsBin']

        if not f_prop or not f_axe or not f_sens or not f_pr_d or not f_pr_f or not f_dist_d or not f_dist_f or not f_ecart_d or not f_ecart_f or not f_usaneg:  # or not f_geomAsBin:
            raise Exception('Parmaeter(s) empty or not valid')

        params = params.replace('{1}', f_prop).replace('{2}', f_axe).replace('{3}', f_sens).replace('{4}',
                                                                                                    f_pr_d).replace(
            '{5}', f_pr_f).replace('{6}', f_dist_d).replace('{7}', f_dist_f).replace('{8}', f_ecart_d).replace('{9}',
                                                                                                               f_ecart_f).replace(
            '{10}', f_usaneg)
        response = requests.get(vmdeport_ws_url + "?" + params)
        response_code = response.status_code

        if(int(response_code) != 200):
            return {'error': 'true', 'sitn_error': 'true', 'code': response_code, 'message': response.text}

        result = request.dbsession.query(func.public.ST_AsGeoJSON(func.public.ST_Force2D(response.json()))).all()

        if result != None:
            result = str(result).replace("('", "").replace("',)", "")
            result = json.loads(result)

    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'sitn_error': false, 'code': 500, 'message': general_exception}
    return result


########################################################
# Search evenement
########################################################
@view_config(route_name='search_evenements', request_method='POST', renderer='json')
@view_config(route_name='search_evenements_slash', request_method='POST', renderer='json')
def search_evenements_view(request):
    try:

        conditions = []

        id_entite = None
        if 'idEntite' in request.params:
            id_entite = request.params['idEntite']

        conditions.append(models.SearchEvenementView.id_entite == id_entite)

        # Check authorization

        auth_tkt = request.cookies.get('auth_tkt', default=None)
        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None
        conditions.append(models.SearchEvenementView.id_utilisateur == current_user_id)

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        search_limit = int(settings['search_limit'])


        # Read params
        if ('numeroDossier' in request.params and request.params['numeroDossier'] != ""):
            conditions.append(func.lower(models.SearchEvenementView.numero_dossier).like('%' + func.lower(request.params['numeroDossier']) + '%'))
        else:
            if ('type' in request.params and request.params['type'] != ""):
                conditions.append(models.SearchEvenementView.type == request.params['type'])

            if ('prevision' in request.params and request.params['prevision'] != ""):
                conditions.append(models.SearchEvenementView.prevision == request.params['prevision'])

            if ('libelle' in request.params and request.params['libelle'] != ""):
                conditions.append(
                    func.lower(models.SearchEvenementView.libelle).like('%' + func.lower(request.params['libelle']) + '%'))

            if ('dateDebut' in request.params and request.params['dateDebut'] != ""):
                conditions.append(func.DATE(models.SearchEvenementView.date_fin) >= func.DATE(request.params['dateDebut']))


            if ('dateFin' in request.params and request.params['dateFin'] != ""):
                conditions.append(func.DATE(models.SearchEvenementView.date_debut) <= func.DATE(request.params['dateFin']))


            if ('division' in request.params and request.params['division'] != ""):
                conditions.append(
                    func.lower(models.SearchEvenementView.division).like('%' + func.lower(request.params['division']) + '%'))

            if ('idRequerant' in request.params and request.params['idRequerant'] != ""):
                conditions.append(models.SearchEvenementView.id_requerant == request.params['idRequerant'])


            if ('idResponsable' in request.params and request.params['idResponsable'] != ""):
                conditions.append(models.SearchEvenementView.id_responsable == request.params['idResponsable'])


            if ('axe' in request.params and request.params['axe'] != ""):
                conditions.append(models.SearchEvenementView.axe == request.params['axe'])


            if ('prDebut' in request.params and request.params['prDebut'] != ""):
                conditions.append(models.SearchEvenementView.pr_debut >= request.params['prDebut'])


            if ('prFin' in request.params and request.params['prFin'] != ""):
                conditions.append(models.SearchEvenementView.pr_fin <= request.params['prFin'])

            if ('prDebutSegSeq' in request.params and request.params['prDebutSegSeq'] != ""):
                conditions.append(models.SearchEvenementView.pr_debut_seg_seq >= request.params['prDebutSegSeq'])


            if ('prDebutSecSeq' in request.params and request.params['prDebutSecSeq'] != ""):
                conditions.append(models.SearchEvenementView.pr_debut_sec_seq >= request.params['prDebutSecSeq'])


            if ('prFinSegSeq' in request.params and request.params['prFinSegSeq'] != ""):
                conditions.append(models.SearchEvenementView.pr_fin_seg_seq <= request.params['prFinSegSeq'])


            if ('prFinSecSeq' in request.params and request.params['prFinSecSeq'] != ""):
                conditions.append(models.SearchEvenementView.pr_fin_sec_seq <= request.params['prFinSecSeq'])


            if ('ajoutePar' in request.params and request.params['ajoutePar'] != ""):
                conditions.append(models.SearchEvenementView.id_utilisateur_ajout == request.params['ajoutePar'])


            if ('prTouche' in request.params and request.params['prTouche'] != ""):
                conditions.append(models.SearchEvenementView.pr_touches == request.params['prTouche'])

            if ('compteurTouche' in request.params and request.params['compteurTouche'] != ""):
                compteurTouche = request.params['compteurTouche']
                if compteurTouche == 'true':
                    compteurTouche = True
                elif compteurTouche == 'false':
                    compteurTouche = False
                else:
                    compteurTouche = None

                conditions.append(models.SearchEvenementView.compteur_touche == compteurTouche)

        query = request.dbsession.query(models.SearchEvenementView).order_by(models.SearchEvenementView.id.desc())

        if len(conditions) > 2:
            result = query.filter(*conditions).all()
        else:
            result = query.filter(*conditions).all()[:search_limit]

        formattedResult = []

        for evenement in result:
            if evenement != None:
                formattedResult.append(evenement.format())

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return formattedResult


########################################################
# Search perturbations
########################################################
@view_config(route_name='search_perturbations', request_method='POST', renderer='json')
@view_config(route_name='search_perturbations_slash', request_method='POST', renderer='json')
def search_perturbations_view(request):
    try:
        conditions = []

        id_entite = None
        if 'idEntite' in request.params:
            id_entite = request.params['idEntite']

        conditions.append(models.SearchPerturbationView.id_entite == id_entite)

        # Check authorization

        auth_tkt = request.cookies.get('auth_tkt', default=None)
        if not auth_tkt:
            raise HTTPForbidden()

        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None
        conditions.append(models.SearchPerturbationView.id_utilisateur == current_user_id)

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        search_limit = int(settings['search_limit'])

        # Read params
        if ('numeroDossierEvenement' in request.params and request.params['numeroDossierEvenement'] != ""):
            conditions.append(func.lower(models.SearchPerturbationView.numero_dossier_evenement).like(
                '%' + func.lower(request.params['numeroDossierEvenement']) + '%'))
           

        else:
            if 'type' in request.params and request.params['type'] != "":
                conditions.append(models.SearchPerturbationView.type == request.params['type'])

            if ('axe' in request.params and request.params['axe'] != ""):
                conditions.append(models.SearchPerturbationView.axe == request.params['axe'])

            if ('prDebut' in request.params and request.params['prDebut'] != ""):
                conditions.append(models.SearchPerturbationView.pr_debut == request.params['prDebut'])

            if ('prFin' in request.params and request.params['prFin'] != ""):
                conditions.append(models.SearchPerturbationView.pr_fin == request.params['prFin'])

            if ('prDebutSegSeq' in request.params and request.params['prDebutSegSeq'] != ""):
                conditions.append(models.SearchPerturbationView.pr_debut_seg_seq >= request.params['prDebutSegSeq'])

            if ('prDebutSecSeq' in request.params and request.params['prDebutSecSeq'] != ""):
                conditions.append(models.SearchPerturbationView.pr_debut_sec_seq >= request.params['prDebutSecSeq'])

            if ('prFinSegSeq' in request.params and request.params['prFinSegSeq'] != ""):
                conditions.append(models.SearchPerturbationView.pr_fin_seg_seq <= request.params['prFinSegSeq'])

            if ('prFinSecSeq' in request.params and request.params['prFinSecSeq'] != ""):
                conditions.append(models.SearchPerturbationView.pr_fin_sec_seq <= request.params['prFinSecSeq'])
               

            if 'etat' in request.params and request.params['etat'] != "":
                conditions.append(models.SearchPerturbationView.etat == request.params['etat'])
               

            if 'urgence' in request.params and request.params['urgence'] != "":
                conditions.append(models.SearchPerturbationView.urgence == request.params['urgence'])
               

            if ('prDebut' in request.params and request.params['prDebut'] != ""):
                conditions.append(models.SearchPerturbationView.pr_debut == request.params['prDebut'])
               

            if ('prFin' in request.params and request.params['prFin'] != ""):
                conditions.append(models.SearchPerturbationView.pr_fin == request.params['prFin'])
               

            if ('description' in request.params and request.params['description'] != ""):
                conditions.append(func.lower(models.SearchPerturbationView.description).like('%' + func.lower(request.params['description']) + '%'))
               

            if 'typeEvenement' in request.params and request.params['typeEvenement'] != "":
                conditions.append(models.SearchPerturbationView.type_evenement == request.params['typeEvenement'])
               

            if ('dateDebut' in request.params and request.params['dateDebut'] != ""):
                conditions.append(
                    func.DATE(models.SearchPerturbationView.date_fin) >= func.DATE(request.params['dateDebut']))
               

            if ('dateFin' in request.params and request.params['dateFin'] != ""):
                conditions.append(
                    func.DATE(models.SearchPerturbationView.date_debut) <= func.DATE(request.params['dateFin']))
               

            # if ('comptage' in request.params and request.params['comptage'] != ""):
            #    conditions.append(models.SearchPerturbationView.comptage == request.params['comptage'])

            if ('ajoutePar' in request.params and request.params['ajoutePar'] != ""):
                conditions.append(models.SearchPerturbationView.id_utilisateur_ajout == request.params['ajoutePar'])

            if ('compteurTouche' in request.params and request.params['compteurTouche'] != ""):
                compteurTouche = request.params['compteurTouche']
                if compteurTouche == 'true':
                    compteurTouche = True
                elif compteurTouche == 'false':
                    compteurTouche = False
                else:
                    compteurTouche = None

                conditions.append(models.SearchPerturbationView.compteur_touche == compteurTouche)
               

        query = request.dbsession.query(models.SearchPerturbationView).order_by(models.SearchPerturbationView.id.desc())

        if len(conditions) > 2:
            result = query.filter(*conditions).all()
        else:
            result = query.filter(*conditions).all()[:search_limit]

        formattedResult = []
        for perturbation in result:
            if perturbation != None:
                formattedResult.append(perturbation.format())

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return formattedResult


########################################################
# Conflits perturbation by id view
########################################################
@view_config(route_name='conflits_perturabations_by_id', request_method='GET', renderer='json')
def conflits_perturabations_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']
        conflicts_date_buffer = settings['conflicts_date_buffer']
        query_s = 'perturbtrafic.pt_conflits_by_evenement_id_json({0}, {1})'.format(id, conflicts_date_buffer)
        query = request.dbsession.query(query_s).all()

        result = None

        if query and len(query) > 0:
            result = str(query).replace('(', '').replace(',)', '').replace("{'", '{"').replace("':", '":').replace(
                ": '", ': "').replace(", '", ', "').replace("',", '",').replace("'}", '"}').replace('\\"', '"').replace(
                "None", '""')
            result = json.loads(result)

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return result


########################################################
# Conflits perturbation
########################################################
@view_config(route_name='conflits_perturabations', request_method='GET', renderer='json')
@view_config(route_name='conflits_perturabations_slash', request_method='GET', renderer='json')
def conflits_perturabations_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        conflicts_date_buffer = settings['conflicts_date_buffer']
        query_s = 'perturbtrafic.pt_conflits_json({0})'.format(conflicts_date_buffer)
        query = request.dbsession.query(query_s).all()

        result = None

        if query and len(query) > 0:
            result = str(query).replace('(', '').replace(',)', '').replace("{'", '{"').replace("':", '":').replace(
                ": '", ': "').replace(", '", ', "').replace("',", '",').replace("'}", '"}').replace('\\"', '"').replace(
                "None", '""')
            result = json.loads(result)

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': general_exception}

    return result


########################################################
# Common OPTION RESPONSE
########################################################
# @view_config(route_name='search_evenements', request_method='OPTIONS', renderer='json')
# @view_config(route_name='search_evenements_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='evenement_edition', request_method='OPTIONS', renderer='json')
@view_config(route_name='evenement_edition_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='perturbation_edition', request_method='OPTIONS', renderer='json')
@view_config(route_name='perturbation_edition_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='evenement_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='perturbation_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='contact_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='organismes', request_method='OPTIONS', renderer='json')
@view_config(route_name='organismes_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='organisme_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='suggestion_by_liste_name', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts_potentiels_avis_perturbation', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts_potentiels_avis_perturbation_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts_potentiels_avis_perturbation_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts_avis_fermeture_urgence', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts_avis_fermeture_urgence_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='contacts_avis_fermeture_urgence_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='contact_avis_pr_touche', request_method='OPTIONS', renderer='json')
@view_config(route_name='contact_avis_pr_touche_slash', request_method='OPTIONS', renderer='json')
@view_config(route_name='contact_avis_pr_touche_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='autorisation_by_id', request_method='OPTIONS', renderer='json')
@view_config(route_name='autorisations', request_method='OPTIONS', renderer='json')
@view_config(route_name='autorisations_slash', request_method='OPTIONS', renderer='json')
def options_response_view(request):
    return ''


########################################################
# Common IntegrityError return message
########################################################
@view_config(context=exc.IntegrityError, renderer='json')
def integrity_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': str(exc)}


########################################################
# Common StatementError return message
########################################################
@view_config(context=exc.StatementError, renderer='json')
def statement_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': general_exception}


########################################################
# Common ResourceClosedError return message
########################################################
@view_config(context=exc.ResourceClosedError, renderer='json')
def resource_closed_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': general_exception}


########################################################
# Common InternalError return message
########################################################
@view_config(context=exc.InternalError, renderer='json')
def internal_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': general_exception}


########################################################
# Common NoReferenceError return message
########################################################
@view_config(context=exc.NoReferenceError, renderer='json')
def noreference_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': general_exception}



########################################################
# Common InvalidRequestError, return message
########################################################
@view_config(context=exc.InvalidRequestError, renderer='json')
def noreference_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': general_exception}


########################################################
# Common DBAPIError return message
########################################################
@view_config(context=exc.DBAPIError, renderer='json')
def noreference_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': general_exception}


########################################################
# Common SQLAlchemyError return message
########################################################
@view_config(context=exc.SQLAlchemyError, renderer='json')
def noreference_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    return {'error': 'true', 'code': 500, 'message': general_exception}



########################################################
# Common HTTPForbidden return message
########################################################
@view_config(context=HTTPForbidden, renderer='json')
def http_forbidden_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc))
    request.response.status = 403
    return {'error': 'true', 'code': 403, 'message': not_authorized_exception}



db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

