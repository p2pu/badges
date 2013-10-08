from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources
from media import processors as media_api
from p2pu_user import models as p2pu_user_api
from project import processors as project_api
from project.forms import ProjectForm
from project.forms import FeedbackForm
from project.forms import RevisionForm
from project.view_helpers import fetch_resources
from oauthclient.decorators import require_login


@require_login
def create(request, badge_id):
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))
    fetch_badge_resources(badge)
    context = {'badge': badge}
    user_uri = request.session['user']['uri']

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
    else:
        form = ProjectForm()

    if form.is_valid():

        try:
            image = media_api.upload_image(
                request.FILES['image'],
                user_uri,
                media_root=settings.MEDIA_ROOT,
                delete_original=True)

            project = project_api.create_project(
                badge['uri'],
                user_uri,
                form.cleaned_data['title'],
                image['uri'],
                form.cleaned_data['work_url'],
                form.cleaned_data['description'],
                form.cleaned_data['reflection'],
                form.cleaned_data['tags']
            )
            return http.HttpResponseRedirect(reverse('project_view', args=(project['id'],)))
        except project_api.MultipleProjectError:
            messages.error(request, _('You have already submitted a project for this badge.'))
        except media_api.UploadImageError:
            messages.error(request, _('Project image cannot be uploaded. Possible reasons: format not supported'
                                      '(png, jpeg, jpg, gif), file size too large (up to 256kb).'))

    context['form'] = form
    return render_to_response(
        'project/create.html',
        context,
        context_instance=RequestContext(request)
    )


def view(request, project_id):
    project = project_api.get_project(project_api.id2uri(project_id))
    project = fetch_resources(project)
    badge = badge_api.get_badge(project['badge_uri'])
    badge = fetch_badge_resources(badge)
    feedback = project_api.get_project_feedback(project['uri'])
    for fb in feedback:
        if fb.get('expert_uri'):
            fb['expert'] = p2pu_user_api.get_user(fb['expert_uri'])
    can_revise = False
    can_give_feedback = False
    if request.session.get('user'):
        user_uri = request.session['user']['uri']
        if user_uri == project['author_uri']:
            can_revise = project_api.can_revise_project(project['uri'])
        can_give_feedback = project_api.ready_for_feedback(project['uri'])
        can_give_feedback &= user_uri in badge_api.get_badge_experts(badge['uri'])

    context = {
        'project': project,
        'badge': badge,
        'feedback': feedback,
        'can_revise': can_revise,
        'can_give_feedback': can_give_feedback
    }
    return render_to_response(
        'project/view.html',
        context,
        context_instance=RequestContext(request)
    )


@require_login
def feedback(request, project_id):
    project = project_api.get_project(project_api.id2uri(project_id))
    fetch_resources(project)
    feedback = project_api.get_project_feedback(project_api.id2uri(project_id))
    badge = badge_api.get_badge(project['badge_uri'])
    fetch_badge_resources(badge)
    user_uri = request.session['user']['uri']

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
    else:
        form = FeedbackForm()

    if form.is_valid():
        try:
            feedback = project_api.submit_feedback(
                project['uri'],
                user_uri,
                form.cleaned_data['good'],
                form.cleaned_data['bad'],
                form.cleaned_data['ugly'],
                form.cleaned_data.get('award_badge', form.cleaned_data.get('award_badge', False))
            )
            if feedback == project_api.submit_feedback_result.AWARDED:
                badge_api.award_badge(
                    badge['uri'],
                    project['author_uri'],
                    user_uri,
                    reverse('project_view', args=(project_id,)),
                )
                messages.success(request, _("Success! You've awarded the Badge to %s" % project['author']['username']))
            elif feedback == project_api.submit_feedback_result.REQUIRES_APPROVAL:
                messages.error(request, _("Badge can only be awarded by it's creator. "
                                          "We had notified them that you liked this project."))
        except Exception, e:
            messages.error(request, _(e[0]))
        return http.HttpResponseRedirect(reverse('project_view', args=(project_id,)))

    context = {
        'badge': badge,
        'project': project,
        'form': form,
        'feedback': project_api.get_project_feedback(project_api.id2uri(project_id))
    }

    return render_to_response(
        'project/feedback.html',
        context,
        context_instance=RequestContext(request)
    )


@require_login
def revise(request, project_id):
    project = project_api.get_project(project_api.id2uri(project_id))
    badge = badge_api.get_badge(project['badge_uri'])
    fetch_badge_resources(badge)

    if request.method == 'POST':
        form = RevisionForm(request.POST)
    else:
        form = RevisionForm()

    if form.is_valid():
        try:
            project_api.revise_project(
                project['uri'],
                form.cleaned_data['improvement'],
                form.cleaned_data.get('work_url', None)
            )
        except Exception as e:
            messages.error(request, _(e.args[0]))
        return http.HttpResponseRedirect(reverse('project_view', args=(project_id,)))

    context = {
        'badge': badge,
        'project': project,
        'form': form
    }
    return render_to_response(
        'project/revise.html',
        context,
        context_instance=RequestContext(request)
    )


def review(request):
    """
    This view shows a list of projects for a user that he/she can submit feedback on
    """

    user = request.session.get('user')
    projects = []

    if user:
        user_badges = badge_api.get_user_earned_badges(user['uri'])
        for badge in user_badges:
            projects += project_api.get_projects_ready_for_feedback(badge['uri'])

    badges = []
    feedback_list = []

    if len(projects) == 0:
        badges = badge_api.get_published_badges()
    else:
        for project in projects:
            feedback_list = project_api.get_project_feedback(project['uri'])
            fetch_resources(project, feedback_list)

    return render_to_response(
        'project/review.html', {
            'projects': map(fetch_resources, projects),
            'badges': map(fetch_badge_resources, badges)
        },
        context_instance=RequestContext(request)
    )
