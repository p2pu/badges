"""
Handles Mozilla Open Badge requests.
"""

from django.http import HttpResponse
from django.http import HttpResponseGone
from django.shortcuts import get_object_or_404
import json
from badge.models import Badge
from badge.models import Award
from media.processors import get_image
from p2pu_user.models import get_user
from .responses import create_assertion_from_template
from .responses import create_badge_from_template
from .responses import create_organisation_from_template
from .helpers import reverse_url
from p2pu_user.models import get_user


def get_assertion(request, uid):
    """
    Handle badge assertion requests.
    """

    award = get_object_or_404(Award, pk=uid)

    if award.ob_state=='REVOKED':
        return HttpResponseGone('{"revoked": true}', mimetype="application/json")

    badge = award.badge
    recipient_email = get_user(award.user_uri)['email']
    image = get_image(badge.image_uri)

    assertion = create_assertion_from_template(
        uid=uid,
        recipient_email=recipient_email,
        image=image['url'],
        evidence=award.evidence_url,
        issued_on=award.date_awarded,
        badge_id=badge.pk,
    )
    json_assertion = json.dumps(assertion)

    return HttpResponse(json_assertion, mimetype="application/json")


def get_badge(request, badge_id):
    """
    Handles badge requests.
    """

    badge = get_object_or_404(Badge, pk=badge_id)
    image = get_image(badge.image_uri)
    criteria = reverse_url('badge_view', args=[badge_id])

    badge = create_badge_from_template(
        name = badge.title,
        description = badge.description,
        image = image['url'],
        criteria = criteria,
    )
    json_badge = json.dumps(badge)

    return HttpResponse(json_badge, mimetype="application/json")


def get_organisation(request):
    """
    Handle organisation requests.
    """

    organisation = create_organisation_from_template()
    json_organisation = json.dumps(organisation)

    return HttpResponse(json_organisation, mimetype="application/json")
