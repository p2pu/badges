from django.conf import settings
from django.utils import simplejson

from notifications.utils import localize_for_user

import requests

import logging
log = logging.getLogger(__name__)


def send_notification_i18n( receiver_uri, subject_template, text_template, html_template=None, context={}, sender=None, callback=None):
    """ translate the notification before sending it """
    
    subject = localize_for_user(receiver_uri, subject_template, context)
    text = localize_for_user(receiver_uri, text_template, context)
    html = None
    if html_template:
        html = localize_for_user(receiver_uri, html_template, context)

    return send_notification(receiver_uri, subject, text, html, sender, callback)


def send_notification( receiver_uri, subject, text, html=None, sender=None, callback=None):
    """ Send a notification to a single receiver via the P2PU API to a user
        receiver - uri of user to send the notification to
        sender - name to use in from part of email
    """
    receiver_username = receiver_uri.strip('/').split('/')[-1]

    if not sender:
        sender = settings.DEFAULT_FROM_ADDRESS

    data = {
        'api-key': settings.LERNANTA_API_KEY,
        'user': receiver_username,
        'subject': subject,
        'text': text,
    }

    if html:
        data['html'] = html
    
    if sender:
        data['sender'] = sender

    if callback:
        data['callback'] = callback

    response = None
    try:
        response = requests.post(settings.NOTIFICATION_URL, data=simplejson.dumps(data))
    except requests.ConnectionError:
        log.error('Could not connect to notification URL')
        return False

    if not response or not response.status_code == 200:
        log.error(u'Could not send email notification to {0}'.format(receiver_uri))
        return False
    return True
