from pyramid.view import view_config
from sqlalchemy import exc
from sqlalchemy import *
from .. import models
from ..scripts.wfs_query import WFSQuery
from ..scripts.ldap_query import LDAPQuery
from ..scripts.utils import Utils

from ..exceptions.custom_error import CustomError
import transaction
import json
import requests
import logging
from pyramid.httpexceptions import HTTPForbidden


log = logging.getLogger(__name__)




########################################################
# Home view
########################################################
@view_config(route_name='home', renderer='../templates/home.jinja2')
@view_config(route_name='home_slash', renderer='../templates/home.jinja2')
def home_view(request):
    return {}


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
            raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)


    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)



    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
    return query



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
            raise Exception(CustomError.id_not_found_exception)

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

        else:
            array = []
            for item in query:
              array.append(item.valeur)
            return array

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
                raise Exception(CustomError.id_not_found_exception)

    except Exception as e:
        tm.abort()
        request.dbsession.rollback()
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
            raise Exception(CustomError.id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(organisme)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
    return query


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
            raise Exception(CustomError.user_not_found_exception)

        # Check if user exists in LDAP
        else:
            entites = []
            for lce, e in request.dbsession.query(models.LienContactEntite, models.Entite).filter(models.LienContactEntite.id_contact == contact.id).filter(models.Entite.id == models.LienContactEntite.id_entite).all():
                entites.append(e.format())

            response = LDAPQuery.do_login(request, login, password, contact, entites)

    except Exception as error:
        log.error(str(error), exc_info=True)
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
        log.error(str(error), exc_info=True)
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
                raise Exception(CustomError.user_not_found_exception)

            # Entites
            entites = []
            for lce, e in request.dbsession.query(models.LienContactEntite, models.Entite).filter(
                    models.LienContactEntite.id_contact == contact.id).filter(
                    models.Entite.id == models.LienContactEntite.id_entite).all():
                entites.append(e.format())

            contact_json = contact.format()
            contact_json['entites'] = entites
        else:
            raise Exception(CustomError.user_not_found_exception)

    except HTTPForbidden as e:
        raise HTTPForbidden()

    except Exception as error:
        log.error(str(error), exc_info=True)
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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 403, 'message': str(error)}

    return entites


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
            raise Exception(CustomError.id_not_found_exception)

        with transaction.manager:
            request.dbsession.delete(delegation)
            # Commit transaction
            transaction.commit()

    except Exception as e:
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500,
                'message': CustomError.id_not_found_exception if str(e) == CustomError.id_not_found_exception else CustomError.general_exception}

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
        log.error(str(e), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}

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
        log.error(str(error), exc_info=True)
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
        log.error(str(error), exc_info=True)
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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}
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
        log.error(str(error), exc_info=True)
        return {'error': 'true', 'sitn_error': false, 'code': 500, 'message': CustomError.general_exception}
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
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 200
    return {'error': 'true', 'code': 50, 'message': CustomError.general_exception}


########################################################
# Common StatementError return message
########################################################
@view_config(context=exc.StatementError, renderer='json')
def statement_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}


########################################################
# Common ResourceClosedError return message
########################################################
@view_config(context=exc.ResourceClosedError, renderer='json')
def resource_closed_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}


########################################################
# Common InternalError return message
########################################################
@view_config(context=exc.InternalError, renderer='json')
def internal_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}


########################################################
# Common NoReferenceError return message
########################################################
@view_config(context=exc.NoReferenceError, renderer='json')
def noreference_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}



########################################################
# Common InvalidRequestError return message
########################################################
@view_config(context=exc.InvalidRequestError, renderer='json')
def invalidrequest_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}


########################################################
# Common DBAPIError return message
########################################################
@view_config(context=exc.DBAPIError, renderer='json')
def dbaapierror_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}


########################################################
# Common SQLAlchemyError return message
########################################################
@view_config(context=exc.SQLAlchemyError, renderer='json')
def sqlalchemyerror_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 500
    return {'error': 'true', 'code': 500, 'message': CustomError.general_exception}



########################################################
# Common HTTPForbidden return message
########################################################
@view_config(context=HTTPForbidden, renderer='json')
def http_forbidden_error(exc, request):
    log.error(str(exc.orig) if hasattr(exc, 'orig') else str(exc), exc_info=True)
    request.response.status = 403
    return {'error': 'true', 'code': 403, 'message': CustomError.not_authorized_exception}



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
