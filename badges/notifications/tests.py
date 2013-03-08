from django.test import TestCase
from mock import patch

from notifications import models

def postMock(*args, **kwargs):
    class Response(object):
        def __init__(self):
            self.status_code = 200
    return Response()


class SimpleTest(TestCase):

    def test_send_notification(self):
        with patch('requests.post', postMock) as requests_post:
            ret = models.send_notification(
                '/uri/user/testuser',
                'Notification subject',
                'Notification text',
                '<html></html>',
                'The Sender',
                'http://call.me'
            )
            self.assertTrue(ret)

    def test_send_notification_i18n(self):
        with patch('notifications.models.send_notification') as send_notification:
            models.send_notification_i18n(
                '/uri/user/testuser',
                'emails/project_submitted_subject.txt',
                'emails/project_submitted.txt',
                context={'test1': 'test123'},
                callback='http://call.me'
            )
            self.assertTrue(send_notification.called)
