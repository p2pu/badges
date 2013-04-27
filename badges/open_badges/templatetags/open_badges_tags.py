from django import template
from badge.models import Award
from django.core.urlresolvers import reverse
from ..helpers import reverse_url

register = template.Library()

@register.simple_tag()
def assertion_url(badge):
    """
    Retrieves award based on user badge.
    """

    if 'award_id' in badge:
        return reverse_url('ob_get_assertion', args=[badge['award_id']])
    else:
        return ''


@register.simple_tag()
def pushed_to_backpack_url(badge):
    """
    Retrieves award based on user badge.
    """

    if 'award_id' in badge:
        return reverse('badge_pushed_to_backpack', args=[badge['award_id']])
    else:
        return ''