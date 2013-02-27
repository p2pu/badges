from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext


def create( request ):
    context = {}
    return render_to_response(
        'badge/create.html',
        context,
        context_instance=RequestContext(request)
    )


def preview( request, badge_id ):
    context = {}
    return render_to_response(
        'badge/preview.html',
        context,
        context_instance=RequestContext(request)
    )


def publish( request, badge_id ):
    context = {}
    return render_to_response(
        'badge/publish.html',
        context,
        context_instance=RequestContext(request)
    )



def view( request, badge_id ):
    context = {}
    return render_to_response(
        'badge/view.html',
        context,
        context_instance=RequestContext(request)
    )

