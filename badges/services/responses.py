from django.template import Context
from django.template.loader import get_template
from django.conf import settings


def create_response_from_template(**kwargs):
    """
    Creates oEmbed reponse dict
    """

    id = kwargs['id']
    title = kwargs['title']
    author_name = kwargs['author_name']
    author_url = kwargs['author_url']
    template = get_template('services/badge_oembed.html')
    context = Context({
        'badge_url': kwargs['badge_url'],
        'maxwidth': kwargs['maxwidth'],
        'maxheight': kwargs['maxheight'],
        'username': kwargs['username'],
    })

    RESPONSE_TEMPLATE = {
        'type': 'rich',
        'version': '1.0',
        'id': id,
        'title': title,
        'author_name': author_name,
        'author_url': author_url,
        'provider_name': settings.OPEN_BADGES_ORGANISATION_NAME,
        'provider_url': settings.OPEN_BADGES_ORGANISATION_URL,
        'html': template.render(context),
    }

    return RESPONSE_TEMPLATE

