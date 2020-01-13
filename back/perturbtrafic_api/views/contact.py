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
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
                contact_record.login = login
                contact_record.nom = nom
                contact_record.prenom = prenom
                contact_record.telephone = telephone
                contact_record.courriel = courriel

                transaction.commit()
            else:
                raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        transaction.abort()
        request.dbsession.rollback()
        log.error(str(e))
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
        log.error(str(e))
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
            contact_json = contact.format()


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

        for cp, c, o in request.dbsession.query(models.ContactPotentielAvisPerturbation, models.Contact).filter(models.Contact.courriel.isnot(None)).filter(
                models.ContactPotentielAvisPerturbation.id_contact == models.Contact.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e))
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
        log.error(str(e))
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
        log.error(str(e))
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
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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

        for cp, c, o in request.dbsession.query(models.ContactAvisFermetureUrgence, models.Contact).filter(models.Contact.courriel.isnot(None)).filter(
                models.ContactAvisFermetureUrgence.id_contact == models.Contact.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e))
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
        log.error(str(e))
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
        log.error(str(e))
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
        log.error(str(e))
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

        for cp, c, o in request.dbsession.query(models.ContactAvisPrTouche, models.Contact).filter(models.Contact.courriel.isnot(None)).filter(
                models.ContactAvisPrTouche.id_contact == models.Contact.id).all():
            result.append(cp.format(c.nom, c.prenom, o.nom))

    except Exception as e:
        log.error(str(e))
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
        log.error(str(e))
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
        log.error(str(e))
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
        log.error(str(e))
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

    return {'message': 'Data successfully saved'}

