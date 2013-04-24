from django import http
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.contrib import messages

import urllib
import requests

import logging
log = logging.getLogger(__name__)

from p2pu_user import models as p2pu_user_api

def login( request ):

    current_site = Site.objects.get_current()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        request.session['next_url'] = referer

    params = {
        'redirect_uri': "http://{0}{1}".format(current_site.domain, reverse('oauth_redirect')),
        'client_id': settings.OAUTH_CLIENT_KEY,
        'response_type': 'code',
    }
    login_url = '{0}?{1}'.format(settings.OAUTH_GRANT_URL, urllib.urlencode(params))
    return http.HttpResponseRedirect(login_url)


def logout( request ):
    del request.session['user']
    return http.HttpResponseRedirect(reverse('landing'))


def redirect( request ):
    # get token
    # get username
    # redirect to final destination

    current_site = Site.objects.get_current()
    params = {
        'code': request.GET['code'],
        'grant_type': 'authorization_code',
        'client_id': settings.OAUTH_CLIENT_KEY,
        'client_secret': settings.OAUTH_CLIENT_SECRET,
        'redirect_uri': "http://{0}{1}".format(current_site.domain, reverse('oauth_redirect')),
    }

    response = requests.post(settings.OAUTH_TOKEN_URL, data=params)
    if response.status_code != 200:
        messages.error(request, _('There was a problem while trying to log in! Please try again.'))
        log.error(u'Could not authenticate with oauth provider: {0}.'.format(response.text))
        return http.HttpResponseRedirect(reverse('landing'))
    data = response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']

    params = {
        'bearer_token': access_token,
    }

    response = requests.get(settings.OAUTH_ID_URL, params=params)
    if response.status_code != 200:
        messages.error(request, _('There was a problem while trying to log in! Please try again.'))
        log.error(u'Could not get identity from oauth provider: {0}'.format(response.text))
        return http.HttpResponseRedirect(reverse('landing'))

    username = response.json()['user']
    #TODO user_url = response.json()['url']
    image_url = response.json()['image_url']

    #TODO get email adress from lernanta and save it
    request.session['user'] = p2pu_user_api.save_user(username, image_url)

    if request.session.get('next_url'):
        next_url = request.session.get('next_url')
        del request.session['next_url']
        return http.HttpResponseRedirect(next_url)

    return http.HttpResponseRedirect(reverse('landing'))


def become( request, username ):
    if settings.DEBUG:
        request.session['user'] = p2pu_user_api.save_user(
            username, 'http://placehold.it/40x40'
        )
    return http.HttpResponseRedirect(reverse('landing'))

