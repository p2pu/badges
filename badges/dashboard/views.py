from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources
from media import models as media_api
from project import models as project_api
from project.view_helpers import fetch_resources
from oauthclient.decorators import require_login

def profile( request, username ):

    context = {}
    user_uri = u'/uri/user/{0}'.format(username)
    context['draft_badges'] = badge_api.get_user_draft_badges(user_uri)
    map(fetch_badge_resources, context['draft_badges'])

    return render_to_response(
        'dashboard/dashboard.html',
        context,
        context_instance=RequestContext(request)
    )
