from django.test import TestCase
from mock import patch

from notifications import models
from p2pu_user.models import save_user


class SimpleTest(TestCase):

	def setUp(self):
		self.user = save_user('testuser', 'http://placehold.it', 'erika@p2pu.org')

	def test_send_notification(self):

		ret = models.send_notification(
			self.user['uri'],
			'Notification subject',
			'Notification text',
			'<html>Some HTML</html>',
			'The Badge Sender'
		)
		self.assertTrue(ret)


	def test_send_notification_fail(self):
		ret = models.send_notification(
			self.user['uri'],
			'Notification subject',
			'Notification text',
			'<html>Some HTML</html>',
			'The Badge Sender'
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
