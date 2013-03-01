from django.conf import settings
from django.core.urlresolvers import reverse
import urllib

def login_url( request ):
    login_url = settings.OAUTH_GRANT_URL
    params = {
        'redirect_uri': "http://localhost:8000{0}".format(reverse('oauth_redirect')),
        'client_id': settings.OAUTH_CLIENT_KEY,
        'response_type': 'code',
        'next': request.path
    }

    return {'OAUTH_LOGIN_URL': '{0}?{1}'.format(login_url,urllib.urlencode(params))}
