from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from badge import models as badge_api

def home(request):
    context = {}
    context['badges'] = badge_api.get_published_badges()

    context['projects'] = [
        {'title': 'IPhone movie'},
        {'title': 'Robots in Love'},
        {'title': 'Perfect bow'},
        {'title': 'Homemade rocket'},
    ]
    return render_to_response('landing/home.html', context, context_instance=RequestContext(request))
