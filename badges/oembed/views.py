"""
Handles oEmbed requests.
"""
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from badge.models import get_badge_id_from_parameter_url
from badge.models import get_badge_by_id
from media.processors import get_image
from p2pu_user.models import uri2username
from .responses import create_response_from_template
from .procesors import check_if_url_is_valid


def oembed(request):

    # Extract GET parameters
    url = request.GET.get('url', None)

    if url and url.startswith('http://'):
        url = url[5:]

    #if not settings.DEBUG:
    #    valid_url = check_if_url_is_valid(url)
    #    if not valid_url:
    #        return HttpResponseNotFound(status=404)

    maxwidth = request.GET.get('maxwidth', '100%')
    maxheight = request.GET.get('maxheight', 180)
    username = request.GET.get('username', None)

    badge_id = get_badge_id_from_parameter_url(url)
    badge = get_badge_by_id(badge_id)
    author_url = badge['author_uri']
    author_name = uri2username(badge['author_uri'])
    image_url = get_image(badge['image_uri'])['url'].split('/')[-1]

    response_badge = create_response_from_template(
        id=badge['id'],
        title=badge['title'],
        badge_url=url,
        badge_image=image_url,
        badge_description=badge['description'],
        badge_requirements=badge['requirements'],
        author_url=author_url,
        author_name=author_name,
        maxwidth=maxwidth,
        maxheight=maxheight,
        username=username,
    )
    json_badge = json.dumps(response_badge)
    return HttpResponse(json_badge, mimetype="application/json")
