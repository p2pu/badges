"""
Tests for oEmbed service of Badges
"""
from unittest import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from mock import patch


@patch('badge.models.get_badge_by_id', lambda x: {'author_uri': '/uri/autor/badgemaker', 'image_uri': '/uri/image/1', 'id': 1, 'title': 'Test Badge', 'description': 'Short description', 'requirements': 'Requirements are getting listed here', })
@patch('media.processors.get_image', lambda x: {'url': 'image/url'})
class OembedBadgesTests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_response_from_http_urls_in_oembed_view(self):
		response = self.client.get(reverse('oembed'), {'url': 'https://badges.p2pu.org/en/badge/view/1/'})

		self.assertEquals(response.status_code, 200)

	def test_response_from_https_urls_in_oembed_view(self):
		response = self.client.get(reverse('oembed'), {'url': 'http://badges.p2pu.org/en/badge/view/1/'})

		self.assertEquals(response.status_code, 200)

