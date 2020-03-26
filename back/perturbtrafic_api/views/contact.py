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
            raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return result


########################################################
# Contacts view
########################################################
@view_config(route_name='contacts', request_method='GET', renderer='json')
@view_config(route_name='contacts_slash', request_method='GET', renderer='json')
def contacts_view(request):

    result = []

    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])

        query = request.dbsession.query(models.Contact).all()

        for item in query:
            item = item.format();
            item['nom_organisme'] = Utils.get_contact_organisme(request, item['id_organisme'])
            result.append(item)

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return result


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
        max_contact_id = None

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
        mobile = None
        telephone = None
        courriel = None
        login = None
        idOrganisme = None
        forcerAjout = None
        conditions = []
        check_exist = false

        # Read params
        if ('nom' in request.params):
            nom = request.params['nom']
            conditions.append(func.lower(models.Contact.nom) == func.lower(nom))
            check_exist = True
        else:
            conditions.append(models.Contact.nom.__eq__(null()))

        if ('prenom' in request.params):
            prenom = request.params['prenom']
            conditions.append(func.lower(models.Contact.prenom) == func.lower(prenom))
            check_exist = True
        else:
            conditions.append(models.Contact.prenom.__eq__(null()))

        if ('mobile' in request.params):
            mobile = request.params['mobile']
            conditions.append(models.Contact.mobile == mobile)
            check_exist = True
        else:
            conditions.append(models.Contact.mobile.__eq__(null()))

        if ('telephone' in request.params):
            telephone = request.params['telephone']
            conditions.append(models.Contact.telephone == telephone)
            check_exist = True
        else:
            conditions.append(models.Contact.telephone.__eq__(null()))

        if ('courriel' in request.params):
            courriel = request.params['courriel']
            conditions.append(func.lower(models.Contact.courriel) == func.lower(courriel))
            check_exist = True
        else:
            conditions.append(models.Contact.courriel.__eq__(null()))

        if ('login' in request.params):
            login = request.params['login']
            conditions.append(func.lower(models.Contact.login) == func.lower(login))
            check_exist = True
        else:
            conditions.append(models.Contact.login.__eq__(null()))

        if ('idOrganisme' in request.params):
            idOrganisme = request.params['idOrganisme']
            conditions.append(models.Contact.id_organisme == idOrganisme)
            check_exist = True
        else:
            conditions.append(models.Contact.id_organisme.__eq__(null()))

        if ('forcerAjout' in request.params):
            forcerAjout = request.params['forcerAjout']

            if forcerAjout == 'true':
                forcerAjout = True
            elif forcerAjout == 'false':
                forcerAjout = False

        # Check if contact already exists
        if forcerAjout is None or forcerAjout == False:

            if len(conditions) > 0 and check_exist:
                query = request.dbsession.query(models.Contact).filter(*conditions).all()

            if len(query) > 0:

                return {'error': 'true', 'code': 500, 'message': 'Contact already exists'}


        with transaction.manager as tm:
            model = models.Contact(
                login=login,
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                mobile=mobile,
                courriel=courriel,
                id_organisme=idOrganisme)

            request.dbsession.add(model)
            request.dbsession.flush()
            max_contact_id = model.id

            transaction.commit()

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

    return {'message': 'Data successfully saved', 'id': max_contact_id}


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
        mobile = None
        telephone = None
        courriel = None
        login = None
        idOrganisme = None

        # Read params
        if ('id' in request.params and request.params['id'] != ''):
            id = request.params['id']

        if ('nom' in request.params):
            nom = request.params['nom']

        if ('prenom' in request.params):
            prenom = request.params['prenom']

        if ('mobile' in request.params):
            mobile = request.params['mobile']

        if ('telephone' in request.params):
            telephone = request.params['telephone']

        if ('courriel' in request.params):
            courriel = request.params['courriel']

        if ('login' in request.params):
            login = request.params['login']

        if ('idOrganisme' in request.params):
            idOrganisme = request.params['idOrganisme']

        with transaction.manager as tm:
            contact_query = request.dbsession.query(models.Contact).filter(models.Contact.id == id)

            if contact_query.count() > 0:
                contact_record = contact_query.first()
                contact_record.login = login
                contact_record.nom = nom
                contact_record.prenom = prenom
                contact_record.telephone = telephone
                contact_record.courriel = courriel
                contact_record.id_organisme = idOrganisme

                transaction.commit()
            else:
                raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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

        query = request.dbsession.query(models.Contact).filter(models.Contact.login.isnot(None)).all()

        result = []

        for contact in query:
            contact_json = contact.format();
            contact_json['nom_organisme'] = Utils.get_contact_organisme(request, contact_json['id_organisme'])


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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        auth_tkt = request.cookies.get('auth_tkt', default=None)

        if not auth_tkt:
            raise HTTPForbidden()

        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        current_user_id = Utils.get_connected_user_id(request)
        current_user_id = int(current_user_id) if current_user_id else None

        if current_user_id:
            idEntite = None

            if ('idEntite' in request.params):
                idEntite = request.params['idEntite']

            if idEntite is None:
                raise Exception(entite_err_msg)

            query = request.dbsession.query(models.Contact, models.LienContactEntite).filter(
                models.Contact.id != current_user_id).filter(
                models.Contact.id == models.LienContactEntite.id_contact).filter(
                models.LienContactEntite.id_entite == idEntite).all()

            for c, lce in query:
                result.append(c.format())

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': entite_err_msg if str(e) == entite_err_msg else CustomError.general_exception}

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
        idEntite = None

        if ('idEntite' in request.params):
            idEntite = request.params['idEntite']

        for cp, c, o in request.dbsession.query(models.ContactPotentielAvisPerturbation, models.Contact,
                                                models.Organisme).filter(
                models.ContactPotentielAvisPerturbation.id_entite == idEntite).filter(
                models.ContactPotentielAvisPerturbation.id_contact == models.Contact.id).filter(
            models.Contact.id_organisme == models.Organisme.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
                raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return {'message': 'Data successfully saved'}


########################################################
# Get Contact_avis_fermeture_urgence_view view
########################################################
@view_config(route_name='contacts_avis_fermeture_urgence', request_method='GET', renderer='json')
@view_config(route_name='contacts_avis_fermeture_urgence_slash', request_method='GET', renderer='json')
def contact_avis_fermeture_urgence_view(request):
    try:
        settings = request.registry.settings
        request.dbsession.execute('set search_path to ' + settings['schema_name'])
        result = []

        for cp, c, o in request.dbsession.query(models.ContactAvisFermetureUrgence, models.Contact,
                                                models.Organisme).filter(
                models.ContactAvisFermetureUrgence.id_contact == models.Contact.id).filter(
            models.Contact.id_organisme == models.Organisme.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e), exc_info=True)
        return str(e)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
                raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
                raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(contact)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return {'message': 'Data successfully saved'}


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
        contacts_bd_logins_query = request.dbsession.query(models.Contact).distinct(models.Contact.login).filter(
            models.Contact.login.isnot(None)).all()
        for c in contacts_bd_logins_query:
            contacts_bd_logins.append(c.login.upper())

        result = []

        for one_contact_ad_json in contacts_ad_json:
            if one_contact_ad_json and login_attr in one_contact_ad_json:
                if one_contact_ad_json[login_attr].upper() not in contacts_bd_logins:
                    groups = LDAPQuery.get_user_groups_by_dn(request, one_contact_ad_json['dn'])

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
        log.error(str(error), exc_info=True)
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
                        id_organisme=one_contact_ad_json['id_organisme'] if 'id_organisme' in one_contact_ad_json else None,
                        login=one_contact_ad_json[settings['ldap_user_attribute_login']],
                        nom=one_contact_ad_json[settings['ldap_user_attribute_lastname']],
                        prenom=one_contact_ad_json[settings['ldap_user_attribute_firstname']],
                        telephone=one_contact_ad_json[settings['ldap_user_attribute_telephone']],
                        # mobile=one_contact_ad_json[settings['ldap_user_attribute_mobile']],
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

                            # Entite group
                            if one_contact_ldap_group_id.startswith(settings['ldap_entite_groups_prefix']):
                                id_entite = entites[
                                    one_contact_ldap_group_id] if entites and one_contact_ldap_group_id in entites else None

                                # If entite does not exist
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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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

            for d, c, lce in request.dbsession.query(models.Delegation, models.Contact,
                                                     models.LienContactEntite).filter(
                models.Delegation.id_delegant == current_user_id).filter(
                models.Contact.id == models.Delegation.id_delegataire).filter(
                models.LienContactEntite.id_entite == idEntite).filter(
                models.Delegation.id_delegataire == models.LienContactEntite.id_contact).all():
                result.append(d.format(c.nom, c.prenom, Utils.get_contact_organisme(request, c.id_organisme)))

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': entite_err_msg if str(error) == entite_err_msg else CustomError.general_exception}

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

            for d, c in request.dbsession.query(models.Delegation, models.Contact).filter(
                    models.Delegation.id_delegataire == current_user_id).filter(
                models.Contact.id == models.Delegation.id_delegant).all():
                result.append(d.format(c.nom, c.prenom, Utils.get_contact_organisme(request, c.id_organisme)))

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error), exc_info=True)
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

            if 'idDelegataire' in request.params:
                idDelegataire = request.params['idDelegataire']

            # Check delegation exists
            delegation_query = request.dbsession.query(models.Delegation).filter(
                models.Delegation.id_delegataire == idDelegataire).filter(
                models.Delegation.id_delegant == current_user_id).all()

            if delegation_query and len(delegation_query) > 0:
                raise Exception(CustomError.delegation_exists_exception)

            with transaction.manager:

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

                model = models.Delegation(
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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.delegation_exists_exception if str(
            e) == CustomError.delegation_exists_exception else CustomError.general_exception}

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
                delegation_record = request.dbsession.query(models.Delegation).filter(
                    models.Delegation.id == idDelegation).first()

                if delegation_record == None:
                    raise Exception(CustomError.id_not_found_exception)

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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return {'message': 'Data successfully saved'}

