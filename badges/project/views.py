from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages

from badge import api as badge_api
from media import models as media_api
from project import api as project_api
from project.forms import ProjectForm

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
            return http.HttpResponseRedirect(reverse('project_show', args=(project['id'],)))
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
    project['image'] = media_api.get_image(project['image_uri'])
    badge = badge_api.get_badge(project['badge_uri'])
    badge['image'] = media_api.get_image(project['image_uri'])
    context = {
        'project': project,
        'badge': badge
    }
    return render_to_response(
        'project/view.html',
        context,
        context_instance=RequestContext(request)
    )


def review( request, project_id ):
    context = {
        'project': project,
        'badge': badge
    }
    return render_to_response(
        'project/review.html',
        context,
        context_instance=RequestContext(request)
    )


