from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources

def home(request):
    context = {}
    context['badges'] = badge_api.get_published_badges()
    for badge in context['badges']:
        fetch_badge_resources(badge)

    context['projects'] = [
        {'title': 'IPhone movie'},
        {'title': 'Robots in Love'},
        {'title': 'Perfect bow'},
        {'title': 'Homemade rocket'},
    ]
    return render_to_response('landing/home.html', context, context_instance=RequestContext(request))
