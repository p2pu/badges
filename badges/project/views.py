from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages

from badge import models as badge_api
from media import models as media_api
from project import models as project_api
from project.forms import ProjectForm
from project.forms import FeedbackForm
from project.forms import RevisionForm
from project.view_helpers import fetch_resources
from oauthclient.decorators import require_login

@require_login
def create( request, badge_id ):
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))
    context = { 'badge': badge }
    user_uri = '/uri/user/{0}'.format(request.session['username'])

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
    else:
        form = ProjectForm()

    if form.is_valid():
        image = media_api.upload_image(request.FILES['image'], user_uri)
        try:
            project = project_api.create_project(
                badge['uri'],
                user_uri,
                form.cleaned_data['title'],
                image['uri'],
                form.cleaned_data['work_url'],
                form.cleaned_data['steps'],
                form.cleaned_data['reflection'],
                form.cleaned_data['tags']
            )
            return http.HttpResponseRedirect(reverse('project_view', args=(project['id'],)))
        except project_api.MultipleProjectError:
            messages.error(request, _('You have already submitted a project for this badge.'))

    context['form'] = form
    return render_to_response(
        'project/create.html',
        context,
        context_instance=RequestContext(request)
    )


def view( request, project_id ):

    project = project_api.get_project(project_api.id2uri(project_id))
    project = fetch_resources(project)
    badge = badge_api.get_badge(project['badge_uri'])
    badge['image'] = media_api.get_image(project['image_uri'])
    feedback = project_api.get_project_feedback(project['uri'])
    context = {
        'project': project,
        'badge': badge,
        'feedback': feedback
    }
    return render_to_response(
        'project/view.html',
        context,
        context_instance=RequestContext(request)
    )


def feedback( request, project_id ):
    project = project_api.get_project(project_api.id2uri(project_id))
    user_uri = '/uri/user/{0}'.format(request.session['username'])

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
    else:
        form = FeedbackForm()

    if form.is_valid():
        project_api.submit_feedback(
            project['uri'],
            user_uri,
            form.cleaned_data['good'],
            form.cleaned_data['bad'],
            form.cleaned_data['ugly']
        )
        return http.HttpResponseRedirect(reverse('project_view', args=(project_id,)))

    context = {
        'project': project,
        'form': form
    }

    return render_to_response(
        'project/feedback.html',
        context,
        context_instance=RequestContext(request)
    )


def revise( request, project_id ):
    project = project_api.get_project(project_api.id2uri(project_id))

    if request.method == 'POST':
        form = RevisionForm(request.POST)
    else:
        form = RevisionForm()

    if form.is_valid():
        project_api.revise_project(
            project['uri'],
            form.cleaned_data['improvement'],
            form.cleaned_data.get('work_url', None)
        )
        return http.HttpResponseRedirect(reverse('project_view', args=(project_id,)))

    context = {
        'project': project,
        'form': form
    }

    context = {
        'project': project,
    }
    return render_to_response(
        'project/revise.html',
        context,
        context_instance=RequestContext(request)
    )


