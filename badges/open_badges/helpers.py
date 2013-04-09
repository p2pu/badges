from django.conf import settings
from django.core.urlresolvers import reverse


def reverse_url(viewname, args=None):
    return settings.OPEN_BADGES_PUBLIC_URL + reverse(viewname, args=args)


def static_url(path):
    return settings.OPEN_BADGES_PUBLIC_URL + settings.MEDIA_URL + path