"""
Badge helpers
"""

from django.core.urlresolvers import reverse

from django.conf import settings

from media.processors import get_image
from p2pu_user.models import get_user


def fetch_badge_resources(badge):
    badge['image'] = get_image(badge['image_uri'])
    badge['author'] = get_user(badge['author_uri'])
    badge['url'] = settings.ORGANISATION_URL + reverse('badge_view', args=(badge['id'],))
    return badge
