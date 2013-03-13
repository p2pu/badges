from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources
from project import models as project_api
from project.view_helpers import fetch_resources
from oauthclient.decorators import require_login

def profile( request, username ):

    context = {}
    user_uri = u'/uri/user/{0}'.format(username)
    context['draft_badges'] = badge_api.get_user_draft_badges(user_uri)
    context['earned_badges'] = badge_api.get_user_earned_badges(user_uri)
    context['created_badges'] = badge_api.get_user_created_badges(user_uri)
    context['awarded_badges'] = badge_api.get_user_awarded_badges(user_uri)
    map(fetch_badge_resources, context['draft_badges'])
    map(fetch_badge_resources, context['earned_badges'])
    map(fetch_badge_resources, context['created_badges'])
    map(fetch_badge_resources, context['awarded_badges'])

    context['feedback_your_projects'] = project_api.search_projects(author_uri=user_uri)
    peer_projects = []
    feedback_latest = []
    for badge in context['earned_badges']:
        feedback_latest += project_api.get_projects_ready_for_feedback(badge['uri'])
        peer_projects += project_api.search_projects(badge_uri=badge['uri'])

    filter_func = lambda project: not project['author_uri'] == user_uri
    feedback_peer_projects = filter(filter_func, peer_projects)
    context['feedback_peer_projects'] = peer_projects
    context['feedback_latest'] = feedback_latest
    return render_to_response(
        'dashboard/dashboard.html',
        context,
        context_instance=RequestContext(request)
    )
