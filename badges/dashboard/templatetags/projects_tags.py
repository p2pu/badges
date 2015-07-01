from django import template
from django.template.defaultfilters import mark_safe
from subprocess import Popen, PIPE

register = template.Library()


@register.filter
def purge_content(value):
    return mark_safe(value.replace('<p>&nbsp;</p>', ''))

@register.filter
def html2text(value):
    """
    Pipes given HTML string into the text browser W3M, which renders it.
    Rendered text is grabbed from STDOUT and returned.
    """
    try:
        cmd = "w3m -dump -T text/html -O ascii"
        proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
        return proc.communicate(str(value))[0]
    except OSError:
        # something bad happened, so just return the input
        return value