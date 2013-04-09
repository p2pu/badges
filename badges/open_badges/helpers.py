from django.conf import settings
from django.core.urlresolvers import reverse
import hashlib


def reverse_url(viewname, args=None):
    return settings.OPEN_BADGES_PUBLIC_URL + reverse(viewname, args=args)


def static_url(path):
    return settings.OPEN_BADGES_PUBLIC_URL + path


def hash_email(email, salt):
    return 'sha256$' + hashlib.sha256(email + salt).hexdigest()