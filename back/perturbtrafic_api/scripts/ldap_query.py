from pyramid_ldap3 import (
    get_ldap_connector,
    groupfinder,
)

from pyramid.security import remember, forget
from pyramid.response import Response
import json

class LDAPQuery():

    @classmethod
    def do_login(cls, request, login, password, contact, entites):
        response = None
        try:
            headers = forget(request)

            # Check if user exists in LDAP
            connector = get_ldap_connector(request)
            data = connector.authenticate(login, password)

            if data is not None:
                dn = data[0]

                headers = remember(request, dn)


                if contact :
                    contact_json = contact.format()
                    contact_json['entites'] = entites

                contact_json = json.dumps(contact_json) if contact else ''

                response = Response(contact_json,
                                    content_type='application/json; charset=UTF-8', headers=headers)
                response.set_cookie('test', 'test1', domain='localhost')
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
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(', ', ',').replace(' , ', ',').replace(' ,', ',').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )
                result, ret = conn.get_response(ret)

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
        dn = cls.get_user_dn(request, login)
        groups = []
        try:
            connector = get_ldap_connector(request)
            result = connector.user_groups(dn)

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
            result = connector.user_groups(dn)

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
            # user = request.authenticated_userid
            connector = get_ldap_connector(request)
            result = connector.user_groups(dn)

            if result is not None:
                for r in result:
                    if r and len(r) > 1:
                        groups.append(cls.format_json_attributes(json.loads(json.dumps(dict(r[1])))))

                # Filter to groups of type entite
                cn_attribute = request.registry.settings['ldap_group_attribute_name']
                output_json = [x for x in groups if cn_attribute in x and x[cn_attribute].startswith(request.registry.settings['ldap_entite_groups_prefix'])]

        except Exception as error:
            raise error

        return output_json

    @classmethod
    def get_user_groups_entite_by_dn(cls, request, dn):
        groups = []
        output_json = []
        try:
            # user = request.authenticated_userid
            connector = get_ldap_connector(request)
            result = connector.user_groups(dn)

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
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(', ', ',').replace(
                        ' , ', ',').replace(' ,', ',').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )
                result, ret = conn.get_response(ret)


            if result is not None:
                 for r in result:
                     if 'dn' in r:
                         user_json = cls.format_json_attributes(json.loads(json.dumps(dict(r['attributes']))))
                         #user_json['dn'] = r['dn']
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
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(', ', ',').replace(' , ', ',').replace(' ,', ',').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )
                result, ret = conn.get_response(ret)

            if result is not None:
                for r in result:

                    if 'dn' in r and len(cls.get_user_groups_entite_by_dn(request, r['dn'])) > 0:
                        user_json = cls.format_json_attributes(json.loads(json.dumps(dict(r['attributes']))))
                        #user_json['dn'] = r['dn']
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
                    attributes=request.registry.settings['ldap_login_query_attributes'].replace(', ', ',').replace(
                        ' , ', ',').replace(' ,', ',').split(','),
                    search_base=request.registry.settings['ldap_login_query_base_dn'],
                    search_filter=request.registry.settings['ldap_search_user_filter']
                )
                result, ret = conn.get_response(ret)

            if result is not None:
                for r in result:
                    if 'dn' in r and len(cls.get_user_groups_by_dn(request, r['dn'])) > 0:
                        user_groups = cls.get_user_groups(request, r['dn']);
                        belongs_to_group = [x for x in user_groups if gr_name_attr in x and x[gr_name_attr] == group_name]

                        if belongs_to_group and len(belongs_to_group) > 0:
                            user_json = cls.format_json_attributes(json.loads(json.dumps(dict(r['attributes']))))
                            #user_json['dn'] = r['dn']
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

    @classmethod
    def get_user_dn(cls, request, login):
        return str(request.registry.settings['ldap_user_dn_template']).replace('{login}', login)



