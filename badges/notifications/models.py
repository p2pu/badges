from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from notifications.utils import localize_for_user
from p2pu_user.models import get_user

import logging
log = logging.getLogger(__name__)


def send_notification_i18n(receiver_uri, subject_template, text_template, html_template=None, context={}, sender=None, callback=None):
    """
    Translate the notification before sending it
    """
    subject = localize_for_user(receiver_uri, subject_template, context).strip()
    text = localize_for_user(receiver_uri, text_template, context).strip()
    html = None
    if html_template:
        html = localize_for_user(receiver_uri, html_template, context).strip()

    return send_notification(receiver_uri, subject, text, html, sender, callback)


def send_notification(receiver_uri, subject, text, html=None, sender=None, callback=None):
    """
    Send a notification to a single receiver via the Django-mandrill to a user
    receiver - uri of user to send the notification to
    sender - name to use in from part of email
    """
    receiver = get_user(receiver_uri)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[receiver['email']],
    )

    if html:
        msg.attach_alternative(html, "text/html")

    try:
        msg.send()
    except:
        log.error(u'Could not send email notification to {0}'.format(receiver['email']))

