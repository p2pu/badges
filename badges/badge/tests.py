"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from django.test import TestCase
from badge import models as badge_api
from project import models as project_api
from mock import patch


@patch('badge.notification_helpers.fetch_badge_resources', lambda x: x)
@patch('project.notification_helpers.fetch_resources', lambda x: x)
class SimpleTest(TestCase):

    def setUp(self):
        self.badge_attrs = [
            'uri',
            'id',
            'title',
            'image_uri',
            'description',
            'requirements',
            'author_uri'
        ]

        self.badge_values = [
            'Movie Maker',
            '/uri/image/1',
            'Create a short movie',
            'Create a movie and upload it to youtube or vimeo',
            '/uri/user/badgemaker',
        ]

    def test_create_and_get_badge(self):
        """ Test that we can create a badge """
        badge = badge_api.create_badge(*self.badge_values)

        # test the presence or attributes for a badge
        for attr in self.badge_attrs:
            self.assertIn(attr, badge)

        # test attribute values
        attrs = self.badge_attrs
        del attrs[0]
        del attrs[0]
        for key, value in zip(attrs, self.badge_values):
            self.assertEquals(badge[key], value)
       
        # test make sure attributes are equal
        badge2 = badge_api.get_badge(badge['uri'])
        self.assertEqual(badge, badge2)

        # test that the badge shows up in drafts
        badges = badge_api.get_user_draft_badges(badge['author_uri'])
        self.assertEquals(len(badges), 1)
        self.assertEquals(badge2, badges[0])


    def test_badge_create_sends_notification(self):
        """ Test that we can create a badge """
        with patch('notifications.models.send_notification') as send:
            badge = badge_api.create_badge(*self.badge_values)
            self.assertTrue(send.called)


    def test_update_badge(self):
        """ Test that we can update a badge """
        badge = badge_api.create_badge(*self.badge_values)
        attrs = self.badge_attrs
        del attrs[1]
        kwargs = dict(zip(self.badge_attrs, [badge['uri']] + self.badge_values))
        del kwargs['author_uri']
        kwargs['title'] = 'A new title'
        badge_api.update_badge(**kwargs)
        badge2 = badge_api.get_badge(badge['uri'])
        self.assertNotEquals(badge, badge2)


    def test_publish_badge(self):
        badge = badge_api.create_badge(*self.badge_values)

        badges = badge_api.get_published_badges()
        self.assertTrue(len(badges) == 0)
        badges = badge_api.get_user_draft_badges(badge['author_uri'])
        self.assertTrue(len(badges) == 1)

        badge_api.publish_badge(badge['uri'])
        self.assertRaises(Exception, badge_api.update_badge, [badge['uri']], {'title':'Updated title'})
        badges = badge_api.get_published_badges()
        self.assertEqual(len(badges), 1)

        badges = badge_api.get_user_draft_badges(badge['author_uri'])
        self.assertEqual(len(badges), 0)
        badges = badge_api.get_user_created_badges(badge['author_uri'])
        self.assertEqual(len(badges), 1)


    def test_unique_title(self):
        badge = badge_api.create_badge(*self.badge_values)
        self.assertRaises(Exception, badge_api.create_badge, self.badge_values)


    def test_award_badge(self):
        badge = badge_api.create_badge(*self.badge_values)
        self.assertNotIn(badge['author_uri'], badge_api.get_badge_experts(badge['uri']))

        badge_api.publish_badge(badge['uri'])
        kwargs = {
            'badge_uri': badge['uri'],
            'user_uri': badge['author_uri'],
            'expert_uri': badge['author_uri'],
            'evidence_url': 'http://some.evi/dence'
        }
        
        # test that the author have the badge
        with self.assertRaisesRegexp(Exception, 'already awarded'):
            badge_api.award_badge(**kwargs)

        # test that non expert cannot award badge
        kwargs['user_uri'] = '/uri/user/iwantbadge'
        kwargs['expert_uri'] = '/uri/user/igivebadge'
        with self.assertRaisesRegexp(Exception, 'Cannot award'):
            badge_api.award_badge(**kwargs)

        # test that expert can award badge
        kwargs['expert_uri'] = badge['author_uri']
        badge_api.award_badge(**kwargs)
        self.assertIn(kwargs['user_uri'], badge_api.get_badge_experts(badge['uri']))
        badges = badge_api.get_user_earned_badges(kwargs['user_uri'])
        self.assertEqual(len(badges), 1)
        badges = badge_api.get_user_awarded_badges(kwargs['expert_uri'])
        self.assertEqual(len(badges), 2) # 2 because author awards it to self


        # test that badge awards triggers notifications
        kwargs['user_uri'] = '/uri/user/ialsowantbadge'
        with patch('notifications.models.send_notification') as send:
            badge_api.award_badge(**kwargs)
            self.assertTrue(send.called)

    def test_get_user_badges(self):
        badge = badge_api.create_badge(*self.badge_values)
        badge_api.publish_badge(badge['uri'])

        badge_values = self.badge_values
        badge_values[0] = 'Badge 2'
        badge = badge_api.create_badge(*badge_values)
        badge_api.publish_badge(badge['uri'])

        badge_values[0] = 'Badge 3'
        badge = badge_api.create_badge(*badge_values)
        badge_api.publish_badge(badge['uri'])

        badge_values[0] = 'Badge 4'
        badge_values[4] = '/uri/user/bob'
        badge = badge_api.create_badge(*badge_values)
        badge_api.publish_badge(badge['uri'])

        badges = badge_api.get_user_earned_badges('/uri/user/badgemaker')
        self.assertEqual(len(badges), 3)

        badges = badge_api.get_user_earned_badges('/uri/user/bob')
        self.assertEqual(len(badges), 1)

        badges = badge_api.get_user_earned_badges('/uri/user/auser')
        self.assertEqual(len(badges), 0)

    def test_badge_without_projects_was_deleted_by_owner(self):
        # setup
        badge = badge_api.create_badge(*self.badge_values)
        badge_api.publish_badge(badge['uri'])

        # test that badge 'deleted' attribute has been set to False
        deleted_badge = badge_api.delete_badge(badge['uri'], badge['author_uri'])
        self.assertTrue(deleted_badge['deleted'])

    def test_raise_error_on_badge_delete_if_not_owner(self):
        # setup
        badge = badge_api.create_badge(*self.badge_values)
        badge_api.publish_badge(badge['uri'])

        # test that method raises error when user is not author of a badge
        with self.assertRaises(badge_api.NotTheAuthorError):
            badge_api.delete_badge(badge['uri'], '/uri/user/iamnottheowner')

    def test_raise_error_on_badge_if_has_projects(self):
        # setup
        badge = badge_api.create_badge(*self.badge_values)
        badge_api.publish_badge(badge['uri'])
        project = {
            'badge_uri': badge['uri'],
            'author_uri': '/uri/user/author',
            'title': 'Test Project 1',
            'image_uri': '/uri/image/1',
            'work_url': 'http://example.com',
            'description': 'Some description',
            'reflection': 'Some other lesions learned',
            'tags': 'tags'
        }
        project_api.create_project(**project)

        # test that method raises error when badge has projects attached to it
        with self.assertRaises(badge_api.HasProjectsAttached):
            badge_api.delete_badge(badge['uri'], badge['author_uri'])




