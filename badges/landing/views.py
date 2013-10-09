from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources

from project import processors as project_api
from project.view_helpers import fetch_resources as fetch_project_resources

from p2pu_user import models as p2pu_user_api

from .processors.search import search_results


def home(request):
    featured_badges = map(fetch_badge_resources, badge_api.get_featured_badges())

    users = p2pu_user_api.get_users()
    paginator = Paginator(users, 16)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        return HttpResponse(status=404)
    if request.is_ajax():
        return render_to_response('p2pu_user/browse_users.html',
                                  {'users': users},
                                  context_instance=RequestContext(request))

    last_n_projects = project_api.last_n_projects(10)
    for project in last_n_projects:
        fetch_project_resources(project,
                                feedback_list=project_api.get_project_feedback(project['uri']))

    return render_to_response('landing/home.html', {
        'badges': featured_badges,
        'users': users,
        'projects': last_n_projects,
    }, context_instance=RequestContext(request))


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


def browse_all_badges(request):

    badges = map(fetch_badge_resources, badge_api.get_published_badges())

    paginator = Paginator(badges, 10) # Show 10 badges per page

    page = request.GET.get('page')
    try:
        badges = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        badges = paginator.page(1)
    except EmptyPage:
        return HttpResponse(status=404)

    if request.is_ajax():
        return render_to_response('landing/browse_badges.html',
                                  {'badges': badges},
                                  context_instance=RequestContext(request))

    return render_to_response(
        'landing/list_badges.html',{
            'badges': badges,
        },
        context_instance=RequestContext(request)
    )
