from django import http
from django.core.urlresolvers import reverse

def require_login( method ):
    def call_method( *args, **kwargs):
        if not args[0].session.get('username'):
            return http.HttpResponseRedirect(reverse('oauth_login'))
        return method(*args, **kwargs)

    return call_method
