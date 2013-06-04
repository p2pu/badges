from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources

from project import processors as project_api
from project.view_helpers import fetch_resources as fetch_project_resources

from p2pu_user import models as p2pu_user_api

from .processors.search import search_results


def home(request):
    context = {}
    context['badges'] = map(fetch_badge_resources, badge_api.last_n_published_badges(5))
    context['projects'] = map(fetch_project_resources, project_api.last_n_projects(10))
    context['users'] = p2pu_user_api.last_n_users(20)
    
    return render_to_response('landing/home.html', context, context_instance=RequestContext(request))


def search(request):
    q = request.GET.get('q')

    results = search_results(q)

    return render_to_response(
        'landing/search_results.html',{
            'q': q,
            'results': results,
        },
        context_instance=RequestContext(request)
    )
