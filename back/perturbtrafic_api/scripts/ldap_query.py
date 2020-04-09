from pyramid_ldap3 import (
    get_ldap_connector,
    groupfinder,
)

from pyramid.security import remember, forget
from pyramid.response import Response
import json

import logging  # log .info('Debug_GL: ')
log = logging.getLogger(__name__)  # log .info('Debug_GL: ')

class LDAPQuery():

    @classmethod
    def do_login(cls, request, login, password, contact, entites):
        response = None
        try:
            headers = forget(request)

            # Check if user exists in LDAP
            connector = get_ldap_connector(request)

            log.debug('Debug_GL: méthode do_login, juste avant la requête LDAP: authenticate(login, password), param login:{}'.format(login))

            result = connector.authenticate(login, password)

            log.debug('Debug_GL: méthode do_login, juste après la requête LDAP: authenticate(login, password), variable result:{}'.format(result))

            if result is not None:
                dn = result[0]

                headers = remember(request, dn)

                if contact :
                    contact_json = contact.format()
                    contact_json['entites'] = entites

                contact_json = json.dumps(contact_json) if contact else ''

                response = Response(contact_json, content_type='application/json; charset=UTF-8', headers=headers)

            else:
                raise Exception('Invalid credentials')

        except Exception as error:
            raise error

        return response

    @classmethod
    def do_logout(cls, request):
        response = None
        try:
            headers = forget(request)
            response = Response('{"error": "false", "code": 200, "message": "User logged out"}', headers=headers)
            response.headerlist.extend(headers)

        except Exception as error:
            raise error

        return response

    @classmethod
    def get_connected_user(cls, request):

        try:
            user_id = request.authenticated_userid

            connector = get_ldap_connector(request)

            with connector.manager.connection() as conn:
                ret = conn.search(
                    search_scope=request.registry.settings['ldap_login_query_scope'],
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(' ', '').split(','),
                    search_base=user_id,
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )

                log.debug('Debug_GL: méthode get_connected_user, juste avant la requête LDAP: get_response(ret), param ret:{}'.format(ret))

                result, ret = conn.get_response(ret)

                log.debug('Debug_GL: méthode get_connected_user, juste après la requête LDAP: get_response(ret), variable result:{}'.format(result))

            if result is None:
                result = []
            else:
                result = [r['attributes'] for r in result
                          if 'dn' in r and r['dn'] == user_id]
                result = result[0] if result and len(result) > 0 else None

                if result is not None:
                    result = json.loads(json.dumps(dict(result)))

        except Exception as error:
            raise error

        return cls.format_json_attributes(result) if result else {}

    @classmethod
    def get_user_groups(cls, request, login):
        dn = request.authenticated_userid
        groups = []
        try:
            connector = get_ldap_connector(request)

            log.debug('Debug_GL: méthode get_user_groups, juste avant la requête LDAP: user_groups(dn), param dn={}'.format(dn))

            result = connector.user_groups(dn)

            log.debug('Debug_GL: méthode get_user_groups, juste après la requête LDAP: user_groups(dn), variable result:{}'.format(result))

            if result is not None:
                for r in result:
                    if r and len(r) > 1:
                        groups.append(cls.format_json_attributes(json.loads(json.dumps(dict(r[1])))))

        except Exception as error:
            raise error

        return groups

    @classmethod
    def get_user_groups_by_dn(cls, request, dn):
        groups = []
        try:
            connector = get_ldap_connector(request)

            log.debug('Debug_GL: méthode get_user_groups_by_dn, juste avant la requête LDAP: user_groups(dn), param dn={}'.format(dn))

            result = connector.user_groups(dn)

            log.debug('Debug_GL: méthode get_user_groups_by_dn, juste après la requête LDAP: user_groups(dn), variable result:{}'.format(result))

            if result is not None:
                for r in result:
                    if r and len(r) > 1:
                        groups.append(cls.format_json_attributes(json.loads(json.dumps(dict(r[1])))))

        except Exception as error:
            raise error

        return groups

    @classmethod
    def get_user_groups_entite(cls, request, login):
        dn = cls.get_user_dn(request, login)
        groups = []
        output_json = []
        try:
            connector = get_ldap_connector(request)

            log.debug('Debug_GL: méthode get_user_groups_entite, juste avant la requête LDAP: user_groups(dn), param dn={}'.format(dn))

            result = connector.user_groups(dn)

            log.debug('Debug_GL: méthode get_user_groups_entite, juste après la requête LDAP: user_groups(dn), variable result:{}'.format(result))

            if result is not None:
                for r in result:
                    if r and len(r) > 1:
                        groups.append(cls.format_json_attributes(json.loads(json.dumps(dict(r[1])))))

                # Filter to groups of type entite
                cn_attribute = request.registry.settings['ldap_group_attribute_name']
                output_json = [x for x in groups if cn_attribute in x and x[cn_attribute].startswith(
                    request.registry.settings['ldap_entite_groups_prefix'])]

        except Exception as error:
            raise error

        return output_json

    @classmethod
    def get_user_groups_entite_by_dn(cls, request, dn):
        groups = []
        output_json = []
        try:
            connector = get_ldap_connector(request)

            log.debug('Debug_GL: méthode get_user_groups_entite_by_dn, juste avant la requête LDAP: user_groups(dn), param dn={}'.format(dn))

            result = connector.user_groups(dn)

            log.debug('Debug_GL: méthode get_user_groups_entite_by_dn, juste après la requête LDAP: user_groups(dn), variable result:{}'.format(result))

            if result is not None:
                for r in result:
                    if r and len(r) > 1:
                        groups.append(cls.format_json_attributes(json.loads(json.dumps(dict(r[1])))))

                # Filter to groups of type entite
                cn_attribute = request.registry.settings['ldap_group_attribute_name']
                output_json = [x for x in groups if cn_attribute in x and x[cn_attribute].startswith(
                    request.registry.settings['ldap_entite_groups_prefix'])]

        except Exception as error:
            raise error

        return output_json

    @classmethod
    def get_users(cls, request):
        users = []

        try:
            connector = get_ldap_connector(request)

            with connector.manager.connection() as conn:
                ret = conn.search(
                    search_scope=request.registry.settings['ldap_login_query_scope'],
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(' ', '').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )

                log.debug('Debug_GL: méthode get_users, juste avant la requête LDAP: get_response(ret), param ret:{}'.format(ret))

                result, ret = conn.get_response(ret)

                log.debug('Debug_GL: méthode get_users, juste après la requête LDAP: get_response(ret), variable result:{}'.format(result))

            if result is not None:
                 for r in result:
                     if 'dn' in r:
                         user_json = cls.format_json_attributes(json.loads(json.dumps(dict(r['attributes']))))
                         users.append(user_json)

        except Exception as error:
            raise error

        return users if users else {}

    @classmethod
    def get_users_belonging_to_group_entites(cls, request):
        users = []

        try:
            connector = get_ldap_connector(request)

            with connector.manager.connection() as conn:
                ret = conn.search(
                    search_scope=request.registry.settings['ldap_login_query_scope'],
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(' ', '').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )

                log.debug('Debug_GL: méthode get_users_belonging_to_group_entites, juste avant la requête LDAP: get_response(ret), param ret:{}'.format(ret))

                result, ret = conn.get_response(ret)

                log.debug('Debug_GL: méthode get_users_belonging_to_group_entites, juste après la requête LDAP: get_response(ret), variable result:{}'.format(result))

            if result is not None:
                for r in result:

                     if 'dn' in r and len(cls.get_user_groups_entite_by_dn(request, r['dn'])) > 0:
                        user_json = cls.format_json_attributes(json.loads(json.dumps(dict(r['attributes']))))
                        user_json['dn'] = r['dn']
                        users.append(user_json)

        except Exception as error:
            raise error

        return users if users else {}

    @classmethod
    def get_users_belonging_to_a_group(cls, request, group_name):
        users = []

        try:
            connector = get_ldap_connector(request)
            gr_name_attr = request.registry.settings['ldap_group_attribute_name']

            with connector.manager.connection() as conn:
                ret = conn.search(
                    search_scope=request.registry.settings['ldap_login_query_scope'],
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(' ', '').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )

                log.debug('Debug_GL: méthode get_users_belonging_to_a_group, juste avant la requête LDAP: get_response(ret), param ret:{}'.format(ret))

                result, ret = conn.get_response(ret)

                log.debug('Debug_GL: méthode get_users_belonging_to_a_group, juste après la requête LDAP: get_response(ret), variable result:{}'.format(result))

            if result is not None:
                for r in result:
                    if 'dn' in r:
                        user_groups = cls.get_user_groups_by_dn(request, r['dn'])

                        if len(user_groups) > 0:
                            belongs_to_group = [x for x in user_groups if gr_name_attr in x and x[gr_name_attr] == group_name]

                            if belongs_to_group and len(belongs_to_group) > 0:
                                user_json = cls.format_json_attributes(json.loads(json.dumps(dict(r['attributes']))))
                                user_json['dn'] = r['dn']
                                users.append(user_json)

        except Exception as error:
            raise error

        return users if users else {}

    @classmethod
    def get_users_belonging_to_two_groups(cls, request, group_name1, group_name2):
        users = []

        try:
            connector = get_ldap_connector(request)
            gr_name_attr = request.registry.settings['ldap_group_attribute_name']

            with connector.manager.connection() as conn:
                ret = conn.search(
                    search_scope=request.registry.settings['ldap_login_query_scope'],
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(' ', '').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )

                log.debug('Debug_GL: méthode get_users_belonging_to_two_groups, juste avant la requête LDAP: get_response(ret), param ret:{}'.format(ret))

                result, ret = conn.get_response(ret)

                log.debug('Debug_GL: méthode get_users_belonging_to_two_groups, juste après la requête LDAP: get_response(ret), variable result:{}'.format(result))

            if result is not None:
                for r in result:
                    if 'dn' in r:
                        user_groups = cls.get_user_groups_by_dn(request, r['dn'])

                        if len(user_groups) > 0:
                            belongs_to_group1 = [x for x in user_groups if gr_name_attr in x and x[gr_name_attr] == group_name1]

                            belongs_to_group2 = [x for x in user_groups if gr_name_attr in x and x[gr_name_attr] == group_name2]

                            if belongs_to_group1 and len(belongs_to_group1) > 0 and belongs_to_group2 and len(belongs_to_group2) > 0:
                                user_json = cls.format_json_attributes(json.loads(json.dumps(dict(r['attributes']))))
                                user_json['dn'] = r['dn']
                                user_json['group'] = user_groups
                                users.append(user_json)

        except Exception as error:
            raise error

        return users if users else {}

    @classmethod
    def format_json_attributes(cls, json_obj):
        for key in json_obj:
            if isinstance(json_obj[key], list) and len(json_obj[key]) > 0:
                json_obj[key] = json_obj[key][0]

        return json_obj
