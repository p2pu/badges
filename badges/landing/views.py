from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources

from project import models as project_api
from project.view_helpers import fetch_resources as fetch_project_resources

from p2pu_user import models as p2pu_user_api

def home(request):
    context = {}
    context['badges'] = map(fetch_badge_resources, badge_api.get_published_badges())
    context['projects'] = map(fetch_project_resources, project_api.get_projects())
    context['users'] = p2pu_user_api.get_users()
    
    return render_to_response('landing/home.html', context, context_instance=RequestContext(request))
