from django.core.serializers.json import DjangoJSONEncoder
from django import http
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import simplejson as json

from badge.forms import BadgeForm
from badge import models as badge_api
from badge.view_helpers import fetch_badge_resources
from media import processors as media_api
from project import processors as project_api
from project.view_helpers import fetch_resources
from oauthclient.decorators import require_login
from p2pu_user import models as p2pu_user_api


@require_login
def create(request):
    user_uri = request.session['user']['uri']
    user = p2pu_user_api.get_user(user_uri)
    user_partner = user['partner']

    form = BadgeForm(user_uri=user_uri)

    if request.method == 'POST':
        form = BadgeForm(request.POST, request.FILES, user_uri=user_uri)

    if form.is_valid():
        try:
            if request.FILES['image_uri'].size > (256 * 1024):
                raise media_api.UploadImageError('Image size too large.')

            image = media_api.upload_image(
                request.FILES['image_uri'],
                user_uri,
                media_root=settings.MEDIA_ROOT,
                delete_original=True)

            badge = badge_api.create_badge(
                form.cleaned_data['title'],
                image['uri'],
                form.cleaned_data['description'],
                form.cleaned_data['requirements'],
                user_uri,
                partner_name=form.cleaned_data['partner']
            )
            return http.HttpResponseRedirect(
                reverse('badge_publish', args=(badge_api.uri2id(badge['uri']),))
            )
        except badge_api.DuplicateTitleError:
            form.errors['title'] = [_('Badge title needs to be unique'), ]
        except media_api.UploadImageError:
            form.errors['title'] = [_('Badge image cannot be uploaded. Possible reasons: format not supported'
                                      '(png, jpeg, jpg, gif), file size too large (up to 256kb).'), ]

    return render_to_response(
        'badge/badge_info/create.html', {
            'form': form,
            'user_is_partner': user_partner,
        },
        context_instance=RequestContext(request))


@require_login
def preview(request, badge_id):
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))
    fetch_badge_resources(badge)
    user = request.session['user']
    user['is_author'] = _user_is_author(badge, user)

    return render_to_response(
        'badge/badge_info/preview.html', {
            'badge': badge,
            'user': user,
        },
        context_instance=RequestContext(request)
    )


@require_login
def edit(request, badge_id):
    user_uri = request.session['user']['uri']
    user = p2pu_user_api.get_user(user_uri)
    user_partner = user['partner']
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))

    if not user_uri == badge['author_uri']:
        messages.error(request, _('You cannot edit someone elses badge!'))
        return http.HttpResponseRedirect(reverse(
            'badge_preview', args=(badge_id,)
        ))

    if request.method == 'POST':
        form = BadgeForm(request.POST, request.FILES, user_uri=user_uri, editing=True, published=badge['published'])
    else:
        form = BadgeForm(badge, user_uri=user_uri, editing=True, published=badge['published'])

    if request.method == 'POST' and form.is_valid():
        try:
            updated = {}
            if 'image_uri' in request.FILES:
                image = media_api.upload_image(
                    request.FILES['image_uri'],
                    request.session['user']['uri'],
                    media_root=settings.MEDIA_ROOT,
                )
                updated['image_uri'] = image['uri']

            for attr in ['title', 'description', 'requirements']:
                if not badge[attr] == form.cleaned_data[attr]:
                    updated[attr] = form.cleaned_data[attr]

            badge = badge_api.update_badge(badge['uri'], **updated)

            if badge['published']:
                return http.HttpResponseRedirect(
                    reverse('badge_view', args=(badge_api.uri2id(badge['uri']),))
                )

            return http.HttpResponseRedirect(
                reverse('badge_preview', args=(badge_api.uri2id(badge['uri']),))
            )
        except badge_api.DuplicateTitleError:
            form.errors['title'] = [_('Badge title needs to be unique'), ]

    return render_to_response(
        'badge/badge_info/edit.html', {
            'badge': badge,
            'form': form,
            'user_is_partner': user_partner,
            'existing_img': media_api.get_image(badge['image_uri']),
        },
        context_instance=RequestContext(request))


@require_login
def publish(request, badge_id):
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


def view(request, badge_id):
    badge = badge_api.get_badge(badge_api.id2uri(badge_id))
    fetch_badge_resources(badge)

    projects = project_api.search_projects_awarded_badges(badge_uri=badge['uri'])
    for project in projects:
        fetch_resources(project, feedback_list=project_api.get_project_feedback(project['uri']))

    expert_uris = badge_api.get_badge_experts(badge['uri'])
    user = request.session.get('user')

    if user:
        user['is_expert'] = user['uri'] in expert_uris
        user['is_author'] = _user_is_author(badge, user)
        if user['is_author']:
            user['can_delete_badge'] = badge_api.is_allowed_to_remove(badge['uri'])
        if user['is_expert']:
            user['added_to_backpack'] = badge_api.pushed_to_backpack(badge, user['uri'])

    projects_ready_for_feedback = project_api.get_projects_ready_for_feedback(badge['uri'])
    for project in projects_ready_for_feedback:
        feedback_list = project_api.get_project_feedback(project['uri'])
        fetch_resources(project, feedback_list=feedback_list)

    experts = map(p2pu_user_api.get_user, expert_uris)

    iframe = '//%s%s?rendering=normal' % (settings.ORGANISATION_URL,
                                               reverse('badge_view_embedded', args=[badge_id]))

    return render_to_response(
        'badge/badge_info/view.html', {
            'user': user,
            'badge': badge,
            'projects': projects,
            'projects_ready_for_feedback': projects_ready_for_feedback,
            'experts': experts,
            'iframe': iframe,
            'organisation_url': settings.ORGANISATION_URL,
        },
        context_instance=RequestContext(request)
    )


@require_login
def delete(request, badge_id):
    """
    Setting badge attribute 'deleted' to True
    """
    user_uri = request.session['user']['uri']

    try:
        badge_api.delete_badge(badge_api.id2uri(badge_id), user_uri)
        messages.success(request, _('Success! You have deleted your badge'))
    except badge_api.NotTheAuthorError:
        messages.error(request, _('Error! You are not the author of the badge!'))
    except badge_api.HasProjectsAttachedError:
        messages.error(request, _('Error! Badge has projects attached!'))

    return http.HttpResponseRedirect(
        reverse('dashboard', args=(p2pu_user_api.uri2username(user_uri),))
    )


@require_login
def pushed_to_backpack(request, award_id):
    # TODO: needs further love
    badge_api.award_was_pushed_to_backpack(award_id)
    return HttpResponse('OK')


def view_embedded(request, badge_id):
    # Get username from parameters or None
    username = request.GET.get('username', None)
    # Check if user is logged in
    if 'user' in request.session:
        username = request.session['user']['username']

    badge_uri = badge_api.id2uri(badge_id)
    badge = badge_api.get_badge(badge_uri)
    fetch_badge_resources(badge)
    projects = None
    user_has_badge = False
    template = 'badge/embed/embedded_large.html'

    if username:
        user_has_badge = badge_api.check_if_user_has_badge(badge['uri'],
                                                           p2pu_user_api.username2uri(username))
    if user_has_badge:
        projects = project_api.get_projects_ready_for_feedback(badge_uri)

    if projects:
        map(fetch_resources, projects)

    # Extract rendering preference -> default large
    rendering = request.GET.get('rendering', 'large')

    if rendering == 'normal':
        template = 'badge/embed/embedded_normal.html'

    return render_to_response(
        template,
        {
            'badge': badge,
            'projects': projects,
            'user_has_badge': user_has_badge,
            'rendering': rendering,
        },
        context_instance=RequestContext(request)
    )


def featured_feed(request):
    featured = map(fetch_badge_resources, badge_api.get_featured_badges())

    def add_url(badge):
        badge['image_url'] = ''.join([
            'http://',
            Site.objects.get_current().domain, badge['image']['url']])
        badge['url'] = ''.join(['http://', badge['url']])
        return badge
    featured = map(add_url, featured)
    return http.HttpResponse(json.dumps(featured, cls=DjangoJSONEncoder), content_type='application/json')


def name_search(request):
    user = request.session['user']
    search_q = request.GET.get('title', '')
    title_exists = {'success': ''}

    if request.is_ajax():
        if badge_api.if_title_exists(search_q.strip(), user['uri']):
            title_exists = {'error': _('Sorry, Badge with this name already exists')}

    return HttpResponse(json.dumps(title_exists), content_type="application/json", status=200)


def _user_is_author(badge, user):
    return user['uri'] == badge['author_uri']

