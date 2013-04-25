"""
Mozilla Open Badges response templates.
"""

from django.conf import settings
from .helpers import reverse_url
from .helpers import static_url
from .helpers import hash_email


def create_assertion_from_template(**kwargs):
    """
    Creates assertion dict based on provided arguments.
    """

    uid = kwargs['uid']
    recipient_email = kwargs['recipient_email']
    image = kwargs.get('image')
    evidence = kwargs.get('evidence')
    issued_on = kwargs['issued_on'].isoformat()
    badge_id = kwargs['badge_id']
    salt = settings.OPEN_BADGES_HASH_EMAIL_SALT
    identity = hash_email(recipient_email, salt)

    ASSERTION_TEMPLATE = {
        'uid': uid,
        'recipient': {
            'type': 'email',
            'hashed': True,
            'salt': salt,
            'identity': identity,
        },
        'image': static_url(image),
        'evidence': static_url(evidence),
        'issuedOn': issued_on,
        'badge': reverse_url('ob_get_badge', args=[badge_id]),
        'verify': {
            'type': 'hosted',
            'url': reverse_url('ob_get_assertion', args=[uid]),
        }
    }

    return ASSERTION_TEMPLATE


def create_badge_from_template(**kwargs):
    """
    Creates badge dict based on provided arguments.
    """

    name = kwargs['name']
    description = kwargs['description']
    image = kwargs['image']
    criteria = kwargs.get('criteria')
    tags = kwargs.get('tags')

    BADGE_TEMPLATE = {
        'name': name,
        'description': description,
        'image': static_url(image),
        'criteria': criteria,
        'tags': tags,
        'issuer': reverse_url('ob_get_organisation'),
    }

    if not criteria:
        del BADGE_TEMPLATE['criteria']
    if not tags:
        del BADGE_TEMPLATE['tags']

    return BADGE_TEMPLATE


def create_organisation_from_template():
    """
    Creates badge dict from settings.
    """

    ORGANISATION_TEMPLATE = {
        'name': settings.OPEN_BADGES_ORGANISATION_NAME,
        'url': settings.OPEN_BADGES_ORGANISATION_URL,
    }

    return ORGANISATION_TEMPLATE