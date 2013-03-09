from django.test import TestCase
from mock import patch

from notifications import models


class SimpleTest(TestCase):

    def test_send_notification(self):
        with patch('requests.post') as requests_post:
            requests_post.return_value.status_code = 200

            ret = models.send_notification(
                '/uri/user/testuser',
                'Notification subject',
                'Notification text',
                '<html></html>',
                'The Sender',
                'http://call.me'
            )
            self.assertTrue(ret)
            self.assertTrue(requests_post.called)

    
    def test_send_notification_fail(self):
        with patch('requests.post') as requests_post:
            requests_post.return_value.status_code = 404

            ret = models.send_notification(
                '/uri/user/testuser',
                'Notification subject',
                'Notification text',
                '<html></html>',
                'The Sender',
                'http://call.me'
            )
            self.assertFalse(ret)
            self.assertTrue(requests_post.called)


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
