from django.http import Http404
from mock import patch
from django.test import TestCase
from django.core import mail

from notifications import models as notification
from p2pu_user.models import save_user


class SimpleTest(TestCase):

    def setUp(self):
        self.user = save_user('testuser', 'http://placehold.it', 'erika@p2pu.org')

    def test_send_notification(self):

        notification.send_notification(
            self.user['uri'],
            'Notification subject',
            'Notification text',
            '<html>Some HTML</html>',
            'The Badge Sender'
        )
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Notification subject')

    def test_send_notification_fail(self):

        self.assertRaises(Http404, notification.send_notification,
                          'non/existent/user/',
                          'Notification subject',
                          'Notification text',
                          '<html>Some HTML</html>',
                          'The Badge Sender')

        self.assertEquals(len(mail.outbox), 0)

    def test_send_notification_i18n(self):
        with patch('notifications.models.send_notification') as send_notification:
            notification.send_notification_i18n(
                '/uri/user/testuser',
                'emails/project_submitted_subject.txt',
                'emails/project_submitted.txt',
                context={'test1': 'test123'},
                callback='http://call.me'
            )
            self.assertTrue(send_notification.called)
