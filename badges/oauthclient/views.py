from django import http
from django.conf import settings
from django.core.urlresolvers import reverse

import urllib
import requests

def login( request ):

    referer = request.META.get('HTTP_REFERER')
    if referer:
        request.session['next_url'] = referer

    params = {
        'redirect_uri': "http://localhost:8000{0}".format(reverse('oauth_redirect')),
        'client_id': settings.OAUTH_CLIENT_KEY,
        'response_type': 'code',
    }
    login_url = '{0}?{1}'.format(settings.OAUTH_GRANT_URL, urllib.urlencode(params))
    return http.HttpResponseRedirect(login_url)


def logout( request ):
    del request.session['username']
    return http.HttpResponseRedirect(reverse('landing'))


def redirect( request ):
    # get token
    # get username
    # redirect to final destination

    params = {
        'code': request.GET['code'],
        'grant_type': 'authorization_code',
        'client_id': settings.OAUTH_CLIENT_KEY,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
        'redirect_uri': "http://localhost:8000{0}".format(reverse('oauth_redirect')),
    }

    response = requests.post(settings.OAUTH_TOKEN_URL, data=params)
    if response.status_code != 200:
        raise Exception('Could not authenticate with oauth provider')
    data = response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']

    params = {
        'bearer_token': access_token,
    }

    response = requests.get(settings.OAUTH_ID_URL, params=params)
    if response.status_code != 200:
        raise Exception('Could not get identity for oauth provider')

    request.session['username'] = response.json()['user']

    if request.session.get('next_url'):
        next_url = request.session.get('next_url')
        del request.session['next_url']
        return http.HttpResponseRedirect(next_url)

    return http.HttpResponseRedirect(reverse('landing'))


def become( request, username ):
    if settings.DEBUG:
        request.session['username'] = username
    return http.HttpResponseRedirect(reverse('landing'))

