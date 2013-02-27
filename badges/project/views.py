from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

def create( request, badge_id ):
    context = {}
    return render_to_response(
        'project/create.html',
        context,
        context_instance=RequestContext(request)
    )




def view( request, project_id ):
    pass
