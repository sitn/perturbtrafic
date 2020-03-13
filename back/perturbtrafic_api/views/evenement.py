from pyramid.view import view_config
from sqlalchemy import *
from .. import models
from ..scripts.utils import Utils
from ..scripts.pt_mailer import PTMailer
from ..exceptions.custom_error import CustomError
from ..scripts.evenements_xml import EvenementXML
import transaction
import json
import logging
from pyramid.httpexceptions import HTTPForbidden


log = logging.getLogger(__name__)


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
            raise Exception(CustomError.id_not_found_exception)



    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
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
            raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

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
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
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

        query = request.dbsession.query(models.PerturbationPourUtilisateurAjout).filter(
            models.PerturbationPourUtilisateurAjout.id_utilisateur == current_user_id).filter(
            models.PerturbationPourUtilisateurAjout.id_entite == id_entite).all()



    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
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

        query = request.dbsession.query(models.EvenementEcheance).filter(
            models.EvenementEcheance.id_utilisateur == current_user_id).filter(
            models.EvenementEcheance.id_entite == id_entite).order_by(models.EvenementEcheance.id.desc()).all()

        evenements_array = []
        for evenement in query:
            evenements_array.append(evenement.format())

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        query_evenement = request.dbsession.query(models.EvenementImpression).filter(
            models.EvenementImpression.id == id).first()

        if not query_evenement:
            raise Exception(CustomError.id_not_found_exception)

        # Get perturbations related to the evenement
        perturbations_ids = []
        perturbations_impression = []
        query_perturbations = request.dbsession.query(models.Perturbation).filter(
            models.Perturbation.id_evenement == id).all()

        for item in query_perturbations:
            perturbations_ids.append(item.id)

        query_perturbations_impression = request.dbsession.query(models.PerturbationImpression).filter(
            models.PerturbationImpression.id.in_(perturbations_ids)).all()

        if query_perturbations_impression:
            for item in query_perturbations_impression:
                perturbations_impression.append(item.format())

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return {'evenement': query_evenement.format(), 'perturbations': perturbations_impression}


########################################################
# Get Evenement edition by id view
########################################################
@view_config(route_name='evenement_edition_by_id', request_method='GET', renderer='json')
def evenement_edition_by_id_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        id = request.matchdict['id']

        # Check authorization
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
            raise Exception(CustomError.id_not_found_exception)

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

            # Plan type
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
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return {'evenement': evenement, 'reperages': reperages,
            'infos': {} if not related_type else related_type.format(), 'categories_chantiers': categories_chantiers,
            'plans_types_fouille': plans_types_fouille, 'geometries': geometries_array}


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
        # urgence = None
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
                # urgence=urgence,
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
            # with transaction.manager:
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

            # Commit transaction
            transaction.commit()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        # transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        # urgence = None
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
        # modifiePar = None
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
            # evenement_record.urgence = urgence
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
                chantier_record.reperage_effectif = _reperageEffectif

                # Delete old categories
                request.dbsession.query(models.LienChantierCategorieChantier).filter(
                    models.LienChantierCategorieChantier.id_chantier == chantier_record.id).delete(
                    synchronize_session=False)

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
                fouille_record.reperage_effectif = _reperageEffectif

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return {'message': 'Data successfully saved'}


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

            if ('nomRequerant' in request.params and request.params['nomRequerant'] != ""):
                conditions.append(
                    func.lower(models.SearchEvenementView.nom_requerant).like(
                        '%' + func.lower(request.params['nomRequerant']) + '%'))


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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return formattedResult


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
                log.info('Importing file: ' + file)
                is_added = EvenementXML.add_file_data(file_json)

                if is_added:
                    successful_files.append(file)

                    # Remove file if is added
                    EvenementXML.move_file_to_success_folder(request, file)

                else:
                    failed_files.append(file)


    except Exception as error:
        log.error(str(error))
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return {'successful_files': successful_files, 'failed_files': failed_files}

