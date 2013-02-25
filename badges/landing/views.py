from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    context = {}
    context['badges'] = [
        {'title': 'Content Marketing'},
        {'title': 'Movie Maker'},
        {'title': 'Science Field Trip'},
        {'title': 'Open Licensee'},
    ]
    context['projects']: [
        {'title': 'IPhone movie'},
        {'title': 'Robots in Love'},
        {'title': 'Perfect bow'},
        {'title': 'Homemade rocket'},
    ]
    return render_to_response('landing/home.html', context, context_instance=RequestContext(request))
