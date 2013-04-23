"""
Open badges context processor.
"""

from django.conf import settings


def process(request):
    return {
        'OPEN_BADGES_ISSUER_JS_URL': settings.OPEN_BADGES_ISSUER_JS_URL,
    }