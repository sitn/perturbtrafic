from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated

# Authentification
from pyramid_ldap3 import (
    get_ldap_connector,
    groupfinder,
)


class RootFactory(object):
    __acl__ = [(Allow, Authenticated, 'view')]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings, root_factory=RootFactory) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('pyramid_ldap3')
        config.scan()
        config.add_subscriber(add_cors_headers_response_callback, NewRequest)

        config.set_authentication_policy(
            AuthTktAuthenticationPolicy('secret', callback=groupfinder)
        )
        config.set_authorization_policy(
            ACLAuthorizationPolicy()
        )

        config.ldap_setup(
            settings['ldap_url'],
            bind=settings['ldap_bind'],
            passwd=settings['ldap_passwd'])

        config.ldap_set_login_query(
            base_dn=settings['ldap_login_query_base_dn'],
            filter_tmpl=settings['ldap_login_query_filter_tmpl'],
            attributes=settings['ldap_login_query_attributes'].replace(' ', '').split(','),
            scope=settings['ldap_login_query_scope'])

        config.ldap_set_groups_query(
            base_dn=settings['ldap_group_query_base_dn'],
            filter_tmpl=settings['ldap_group_query_filter_tmpl'],
            attributes=settings['ldap_login_query_attributes'].replace(' ', '').split(','),
            scope=settings['ldap_group_query_scope'],
            cache_period=int(settings['ldap_group_query_cache_period']))

    return config.make_wsgi_app()


# Add CORS Header
def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:4200',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })
    event.request.add_response_callback(cors_headers)
