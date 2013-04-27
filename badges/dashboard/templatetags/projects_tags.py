from django import template
from django.template.defaultfilters import mark_safe

register = template.Library()


@register.filter
def purge_content(value):
    return mark_safe(value.replace('<p>&nbsp;</p>', ''))