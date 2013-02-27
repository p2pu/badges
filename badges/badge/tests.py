"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from badges import api as badge_api


class SimpleTest(TestCase):

    def test_create_and_get_badge(self):
        """ Test that we can create a badge """
        title = "Movie Maker"
        image_uri = ""
        description = "Create a short movie"
        requirements = ""
        badge = badge_api.create_badge(title, image_uri, description, requirements)

        badge_attr = ['uri', 'image_uri', 'title', 'description', 'requirements', 'author_uri']

        # test the presence or attributes for a badge
        for attr in badge_attr:
            self.assertIn(attr, badge)
       
        badge2 = badge_api.get_badge(badge['uri'])

        # make sure attributes are equal
        for attr in badge_attr:
            self.assertEqual(badge[attr], badge2[attr])


    def get_badges(self):
        """ Test that we can create and retrieve multiple badges """

        badges = badge_api.get_badges()
        self.assertTrue(len(badges) == 0)


    def test_update_badge(self):
        """ Test that we can update a badge """
        pass


    def test_publish_badge(self):

        badge = badge_api.create_badge()
        badge = badge_api.publish_badge(badge['uri'])
        with self.assertRaises(Exception):
            badge_api.update_badge(badge['uri'], title="Updated title")
