from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources
from project import processors as project_api
from dashboard.processors import list_projects_ready_for_feedback, list_projects_by_user, list_projects_that_user_gave_feedback, check_if_owner
from project.view_helpers import fetch_resources
from p2pu_user import models as user_api


def profile_dashboard(request, username):
    user = user_api.get_user(user_api.username2uri(username))
    user = check_if_owner(request.session.get('user', default=None), username, user)

    if not user.get('is_owner'):
        return redirect(to=reverse('profile_badges', args=[username]))

    badges = map(fetch_badge_resources, badge_api.get_user_earned_badges(user['uri']))

    projects = list_projects_ready_for_feedback(badges)

    return render_to_response(
        'dashboard/dashboard.html', {
            'user': user,
            'projects': projects,
            'badges': badges,
        },
        context_instance=RequestContext(request)
    )


def profile_badges(request, username):
    user = user_api.get_user(user_api.username2uri(username))
    user = check_if_owner(request.session.get('user', default=None), username, user)
    badges = map(fetch_badge_resources, badge_api.get_user_earned_badges(user['uri']))
    draft_badges = map(fetch_badge_resources, badge_api.get_user_draft_badges(user['uri']))

    projects = list_projects_by_user(user['uri'])

    return render_to_response(
        'dashboard/dashboard_badges.html', {
            'user': user,
            'projects': projects,
            'badges': badges,
            'draft_badges': draft_badges,
        },
        context_instance=RequestContext(request)
    )


def profile_feedback(request, username):
    user = user_api.get_user(user_api.username2uri(username))
    user = check_if_owner(request.session.get('user', default=None), username, user)

    projects = list_projects_that_user_gave_feedback(user['uri'])

    return render_to_response(
        'dashboard/dashboard_feedback.html', {
            'user': user,
            'projects': projects,
        },
        context_instance=RequestContext(request)
    )