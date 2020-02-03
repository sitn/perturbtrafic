from pyramid.view import view_config
from sqlalchemy import exc
from sqlalchemy import *
from .. import models
from ..scripts.ldap_query import LDAPQuery
from ..scripts.utils import Utils
from ..scripts.pt_mailer import PTMailer
from ..exceptions.custom_error import CustomError
from datetime import datetime, date, timedelta
import transaction
import json
import logging
import datetime
from pyramid.httpexceptions import HTTPForbidden


log = logging.getLogger(__name__)


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
            raise Exception(CustomError.id_not_found_exception)



    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

        with transaction.manager:
            perturbation.date_suppression = func.now()
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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

    except (exc.SQLAlchemyError, exc.DBAPIError, Exception) as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

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
                models.AvisPerturbation.id_perturbation == id).filter(
            models.AvisPerturbation.id_contact == models.Contact.id).all():
            contacts_a_aviser.append(c)

        # Reperage
        reperages = []
        evenement_lignes_ids = []

        for item in query_geom_ligne:
            evenement_lignes_ids.append(item.id)

        if len(evenement_lignes_ids) > 0:
            query_reperage = request.dbsession.query(models.Reperage).filter(
                models.Reperage.id_perturbation_ligne.in_(evenement_lignes_ids)).all()

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
            perturbation[
                'nom_utilisateur_ajout'] = contact_utilisateur_ajout.prenom + ' ' + contact_utilisateur_ajout.nom

        if contact_utilisateur_modification:
            perturbation[
                'nom_utilisateur_modification'] = contact_utilisateur_modification.prenom + ' ' + contact_utilisateur_modification.nom

        if contact_utilisateur_validation:
            perturbation[
                'nom_utilisateur_validation'] = contact_utilisateur_validation.prenom + ' ' + contact_utilisateur_validation.nom

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return {'perturbation': perturbation, 'reperages': reperages,
            'infos': {} if not relatedtype else relatedtype, 'contacts_a_aviser': contacts_a_aviser,
            'geometries': geometries_array, 'deviations': deviations}


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
        # ajoutePar = None
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

            evenement_record = request.dbsession.query(models.Evenement).filter(
                models.Evenement.id == idEvenement).first()

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
            user_can_update_etat_perturbation_creation = Utils.user_can_update_etat_perturbation_creation(request,
                                                                                                          current_user_id)

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

        # Read params deviations
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
                    type_occupation=_typeOccupation)

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
                reperages_string += '<tr><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td></tr>'.format(
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


            # If En attente → Envoi à l’approbateur = rôle trafic (and belonging to current entite)
            elif int(etat) == int(settings['perturbation_etat_attente_code']):
                query_entite_group_ad = request.dbsession.query(models.Entite).filter(
                    models.Entite.id == idEntite).first()

                if query_entite_group_ad:
                    contacts_a_aviser_mails_array += Utils.get_mails_of_contacts_belonging_to_two_groups(request,
                                                                                                         settings[
                                                                                                             'ldap_trafic_group_name'],
                                                                                                         query_entite_group_ad.nom_groupe_ad)

            # Delete duplicates from array
            contacts_a_aviser_mails_array = list(dict.fromkeys(contacts_a_aviser_mails_array))

            if contacts_a_aviser_mails_array and len(contacts_a_aviser_mails_array) > 0:
                PTMailer.send_templated_mail(request, contacts_a_aviser_mails_array,
                                             'FERMETURE' if int(perturbation_model.type) == int(
                                                 settings['fermeture_perturbation_id']) else "OCCUPATION" if int(
                                                 perturbation_model.type) == int(
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

    except Exception as e:
        # tm.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
            user_can_update_etat_perturbation = Utils.user_can_update_etat_perturbation(request, current_user_id,
                                                                                        idPerturbation)

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
                if dateDebut is not None and perturbation_record.date_debut is not None and str(
                        perturbation_record.date_debut) != dateDebut:
                    etat = settings['perturbation_etat_attente_code']

                # Lorsque le tracé est modifié, l'état repasse en attente.
                if int(etat) != int(settings['perturbation_etat_attente_code']):
                    is_geometries_equal = Utils.compare_perturbation_geometries(request, idPerturbation,
                                                                                geometries_reperages)

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
            request.dbsession.query(models.Deviation).filter(models.Deviation.id_perturbation == idPerturbation).delete(
                synchronize_session=False)
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
                reperages_string += '<tr><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td><td><p>{}</p></td></tr>'.format(
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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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

        query = request.dbsession.query(models.PerturbationImpression).filter(
            models.PerturbationImpression.id == id).first()

        if not query:
            raise Exception(CustomError.id_not_found_exception)

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(
                    e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return query.format()


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
                conditions.append(func.lower(models.SearchPerturbationView.description).like(
                    '%' + func.lower(request.params['description']) + '%'))

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return formattedResult


########################################################
# Conflits perturbation by id view
########################################################
@view_config(route_name='conflits_perturabations_by_id', request_method='GET', renderer='json')
def conflits_perturabations_by_id_view(request):

    result = []

    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']

        conflicts_date_buffer = settings['conflicts_date_buffer']
        conflicts_geom_buffer = settings['conflicts_geom_buffer']
        query_s = 'pt_conflits_by_perturbation_id_json({0}, {1}, {2})'.format(id, conflicts_date_buffer,
                                                                                    conflicts_geom_buffer)
        query = request.dbsession.query(query_s).all()

        for item in query:
            if len(item) > 0:
                result.append(item[0])
            else:
                result.append(item)

        """
        result = None

        if query and len(query) > 0:
            result = str(query).replace('(', '').replace(',)', '').replace("{'", '{"').replace("':", '":').replace(
                ": '", ': "').replace(", '", ', "').replace("',", '",').replace("'}", '"}').replace('\\"', '"').replace(
                "None", '""')
            result = json.loads(result)
        """
    except Exception as e:
        log.error(str(e))
        request.response.status = 500
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return result


########################################################
# Conflits evenement by id view
########################################################
@view_config(route_name='conflits_evenement_by_id', request_method='GET', renderer='json')
def conflits_evenement_by_id_view(request):

    result = []

    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        id = request.matchdict['id']
        conflicts_date_buffer = settings['conflicts_date_buffer']
        conflicts_geom_buffer = settings['conflicts_geom_buffer']
        query_s = 'perturbtrafic.pt_conflits_by_evenement_id_json({0}, {1}, {2})'.format(id, conflicts_date_buffer,
                                                                                    conflicts_geom_buffer)
        query = request.dbsession.query(query_s).all()

        for item in query:
            if len(item) > 0:
                result.append(item[0])
            else:
                result.append(item)

        """
        result = None

        if query and len(query) > 0:
            result = str(query).replace('(', '').replace(',)', '').replace("{'", '{"').replace("':", '":').replace(
                ": '", ': "').replace(", '", ', "').replace("',", '",').replace("'}", '"}').replace('\\"', '"').replace(
                "None", '""')
            result = json.loads(result)
        """
    except Exception as e:
        log.error(str(e))
        request.response.status = 500
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return result



########################################################
# Conflits perturbation
########################################################
@view_config(route_name='conflits_perturabations', request_method='GET', renderer='json')
@view_config(route_name='conflits_perturabations_slash', request_method='GET', renderer='json')
def conflits_perturabations_view(request):
    
    result = []

    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        idEntite = request.params['idEntite'] if 'idEntite' in request.params else None

        conflicts_date_buffer = settings['conflicts_date_buffer']
        conflicts_geom_buffer = settings['conflicts_geom_buffer']
        query_s = 'perturbtrafic.pt_conflits_json({0}, {1}, {2})'.format(idEntite, conflicts_date_buffer, conflicts_geom_buffer)

        query = request.dbsession.query(query_s).all()

        for item in query:
            if len(item) > 0:
                result.append(item[0])
            else:
                result.append(item)

        """
        result = None
        
        if query and len(query) > 0:
            result = str(query).replace('(', '').replace(',)', '').replace("{'", '{"').replace("':", '":').replace(
                ": '", ': "').replace(", '", ', "').replace("',", '",').replace("'}", '"}').replace('\\"', '"').replace(
                "None", '""')
            #result = json.loads(result)
        """
    except Exception as e:
        log.error(str(e))
        request.response.status = 500
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return result
