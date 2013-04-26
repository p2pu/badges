from django import http
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings

from badge.forms import BadgeForm
from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources
from media import models as media_api
from project import models as project_api
from project.view_helpers import fetch_resources
from oauthclient.decorators import require_login
from p2pu_user import models as p2pu_user_api

@require_login
def create( request ):
    template_name = 'badge/create.html'

    if request.method == 'POST':
        form = BadgeForm(request.POST, request.FILES)
    else:
        form = BadgeForm()

    user_uri = request.session['user']['uri']

    if form.is_valid():
        try:
            if request.FILES['image'].size > (256 * 1024):
                raise media_api.UploadImageError('Image size too large.')

            image = media_api.upload_image(
                request.FILES['image'],
                user_uri,
                media_root=settings.MEDIA_ROOT,
                delete_original=True)

            badge = badge_api.create_badge(
                form.cleaned_data['title'],
                image['uri'],
                form.cleaned_data['description'],
                form.cleaned_data['requirements'],
                user_uri
            )
            return http.HttpResponseRedirect(
                reverse('badge_publish', args=(badge_api.uri2id(badge['uri']),))
            )
        except badge_api.DuplicateTitleError:
            form.errors['title'] = [_('Badge title needs to be unique'),]
        except media_api.UploadImageError:
            form.errors['title'] = [_('Badge image cannot be uploaded. Possible reasons: format not supported'
                                      '(png, jpeg, jpg, gif), file size too large (up to 256kb).'),]

    return render_to_response(
        template_name, {'form': form},
        context_instance=RequestContext(request))


@require_login
def preview( request, badge_id ):
    context = {
        'badge': badge_api.get_badge(badge_api.id2uri(badge_id))
    }
    fetch_badge_resources(context['badge'])
    return render_to_response(
        'badge/preview.html',
        context,
        context_instance=RequestContext(request)
    )


@require_login
def edit( request, badge_id ):
    template_name = 'badge/edit.html'
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))

    if not request.session['user']['uri'] == badge['author_uri']:
        messages.error(request, _('You cannot edit someone elses badge!'))
        return http.HttpResponseRedirect(reverse(
            'badge_preview', args=(badge_id,)
        ))

    if badge['publised']:
        messages.error(request, _('Badge already publised, create a new badge instead'))
        return http.HttpResponseRedirect(reverse(
            'badge_view', args=(badge_id,)
        ))

    if request.method == 'POST':
        form = BadgeForm(request.POST, request.FILES)
    else:
        form = BadgeForm(badge)

    if request.method == 'POST' and form.is_valid():
        #TODO update image
        #image = media_api.upload_image(request.FILES['image'], '/uri/user/1')
        try:
            updated = {}
            for attr in ['title', 'description', 'requirements']:
                if not badge[attr] == form.cleaned_data[attr]:
                    updated[attr] = form.cleaned_data[attr]

            badge = badge_api.update_badge(badge['uri'], **updated)
            return http.HttpResponseRedirect(
                reverse('badge_preview', args=(badge_api.uri2id(badge['uri']),))
            )
        except badge_api.DuplicateTitleError:
            form.errors['title'] = [_('Badge title needs to be unique'),]

    return render_to_response(
        template_name, {'form': form},
        context_instance=RequestContext(request))


@require_login
def publish( request, badge_id ):
    user = request.session['user']
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))

    if not user['uri'] == badge['author_uri']:
        messages.error(request, _('You cannot publish someone elses badge!'))
        return http.HttpResponseRedirect(reverse(
            'badge_preview', args=(badge_id,)
        ))

    if request.method == 'POST':
        badge_api.publish_badge(badge['uri'])
        return http.HttpResponseRedirect(reverse(
            'badge_view', args=(badge_id,)
        ))

    return http.HttpResponseRedirect(reverse(
        'badge_preview', args=(badge_id,)
    ))
    

def view( request, badge_id ):
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))
    fetch_badge_resources(badge)
    context = {
        'badge': badge
    }
    context['projects'] = map(fetch_resources, project_api.search_projects(badge_uri=badge['uri']))

    expert_uris = badge_api.get_badge_experts(badge['uri'])

    if request.session.get('user'):
        context['user_is_expert'] = request.session['user']['uri'] in expert_uris

    context['experts'] = map(p2pu_user_api.get_user, expert_uris)

    return render_to_response(
        'badge/view.html',
        context,
        context_instance=RequestContext(request)
    )


@require_login
def pushed_to_backpack( request, award_id ):
    # TODO: needs further love
    badge_api.award_was_pushed_to_backpack(award_id)
    return HttpResponse('OK')
