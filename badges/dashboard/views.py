from django.shortcuts import render_to_response
from django.template import RequestContext


from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources
from project import processors as project_api
from project.view_helpers import fetch_resources
from p2pu_user import models as user_api


def profile(request, username ):

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
    map(fetch_resources, context['feedback_your_projects'])
    peer_projects = []
    feedback_latest = []
    for badge in context['earned_badges']:
        feedback_latest += project_api.get_projects_ready_for_feedback(badge['uri'])
        peer_projects += project_api.search_projects(badge_uri=badge['uri'])

    filter_func = lambda project: not project['author_uri'] == user_uri
    peer_projects = filter(filter_func, peer_projects)

    badges_under_revision = []
    context['badges_under_revision'] = None
    for project in context['feedback_your_projects']:
        badge_uri = project_api.get_badge_uri_from_project_under_revision(project['uri'])
        if badge_uri:
            badge = badge_api.get_badge(badge_uri)
            fetch_badge_resources(badge)
            badges_under_revision.append(badge)

    if badges_under_revision:
        context['badges_under_revision'] = badges_under_revision

    context['feedback_peer_projects'] = map(fetch_resources, peer_projects)
    context['feedback_latest'] = map(fetch_resources, feedback_latest)
    context['user'] = user_api.get_user(user_api.username2uri(username))
    context['can_delete'] = False

    if 'user' in request.session:
        if context['user']['username'] == request.session.get('user')['username']:
            context['can_delete'] = True

    return render_to_response(
        'dashboard/dashboard.html',
        context,
        context_instance=RequestContext(request)
    )
