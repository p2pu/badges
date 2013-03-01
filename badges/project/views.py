from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from badge import api as badge_api
from project.forms import ProjectForm

def create( request, badge_id ):
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))
    context = { 'badge': badge }

    if request.method == 'POST':
        form = ProjectForm(request.POST)
    else:
        form = ProjectForm()

    if form.is_valid():
        pass

    context['form'] = form
    return render_to_response(
        'project/create.html',
        context,
        context_instance=RequestContext(request)
    )


def view( request, project_id ):
    pass
