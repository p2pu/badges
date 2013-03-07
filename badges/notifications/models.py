from django.conf import settings
from django.utils import simplejson

import logging
log = logging.getLogger(__name__)

import requests

def send_notification( receiver, subject, text, sender, callback=None):
    
    data = {
        'api-key': settings.LERNANTA_API_KEY,
        'user': receiver,
        'subject': subject,
        'text': text,
        'sender': sender,
    }
    
    if callback:
        data['callback'] = callback

    response = requests.post(settings.NOTIFICATION_URL, data=simplejson.dumps(data))

    if not response.status_code == 200:
        log.error(u'Could not send email notificatoin to {0}'.format(receiver))
        return False
    return True
