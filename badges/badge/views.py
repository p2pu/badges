from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse

from badge.forms import BadgeForm
from badge import api as badge_api

class BadgeCreateView(FormView):
    template_name = 'badge/create.html'
    form_class = BadgeForm
    success_url = '/badges/'

    def form_valid(self, form):
        #TODO upload image
        badge = badge_api.create_badge(
            form.cleaned_data['title'],
            '/uri/image/1',
            form.cleaned_data['description'],
            form.cleaned_data['requirements'],
            '/uri/author/1'
        )
        #TODO handle possible error from model
        return http.HttpResponseRedirect(
            reverse('badge_preview', args=(badge_api.uri2id(badge['uri']),))
        )


def create( request ):
    context = {}
    return render_to_response(
        'badge/create.html',
        context,
        context_instance=RequestContext(request)
    )


def preview( request, badge_id ):

    context = {
        'badge': badge_api.get_badge(badge_api.id2uri(badge_id))
    }

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

