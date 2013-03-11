from django.test import TestCase
from mock import patch

from project import models as project_api
from badge import models as badge_api


class ProjectIntegrationTests(TestCase):

    badge_values = {
        'title': 'Movie Maker',
        'image_uri': '/uri/image/1',
        'description': 'Create a short movie',
        'requirements': 'Create a movie and upload it to youtube or vimeo',
        'author_uri': '/uri/user/badgemaker'
    }

    project_values = {
        'badge_uri': '/uri/badge/1',
        'author_uri': '/uri/user/testuser',
        'title': 'Test Title',
        'image_uri': '/uri/image/1',
        'work_url': 'http://project.org/url',
        'description': 'Did the test',
        'reflection': 'Will do it earlier and more next time',
        'tags': ['test', 'tdd'],
    }


    def setUp(self):
        self.notification_patcher = patch('notifications.models.send_notification')
        self.notification_patcher.start()


    def tearDown(self):
        self.notification_patcher.stop()


    def test_project_feedback_cycle(self):
        badge = badge_api.create_badge(**self.badge_values)
        badge_api.publish_badge(badge['uri'])

        project_values = self.project_values.copy()
        project_values['badge_uri'] = badge['uri']
        project = project_api.create_project(**project_values)

        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 0)

        self.assertFalse(project_api.can_revise_project(project['uri']))
        with self.assertRaises(Exception):
            project_api.revise_project(project['uri'], 'All better')

        self.assertTrue(project_api.ready_for_feedback(project['uri']))

        project_api.submit_feedback(project['uri'], '/uri/user/badgemaker', 'Ugly', 'Bad', 'Good')
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 1)
        self.assertIn('good', project_feedback[0])
        self.assertIn('bad', project_feedback[0])
        self.assertIn('ugly', project_feedback[0])
        self.assertIn('expert_uri', project_feedback[0])

        # test that multiple feedback cannont be submitted without a revision
        self.assertFalse(project_api.ready_for_feedback(project['uri']))
        with self.assertRaises(Exception):
            project_api.submit_feedback(project['uri'], '/uri/user/badgemaker', 'Ugly', 'Bad', 'Good')

        project_api.revise_project(project['uri'], 'everything is better now!!')
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 2)

        project_api.submit_feedback(project['uri'], '/uri/user/badgemaker', 'Ugly', 'Bad', 'Good')

        project_api.revise_project(project['uri'], 'everything is better now, promise!!', work_url='http://mywork.com/new-and-improved')
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 4)
 
        self.assertIn('improvement', project_feedback[1]) 
        self.assertIn('date_created', project_feedback[1]) 
        self.assertNotIn('work_url', project_feedback[1])

        self.assertIn('improvement', project_feedback[3]) 
        self.assertIn('work_url', project_feedback[3])


    def test_expert_feedback_and_creator_revision(self):
        badge = badge_api.create_badge(**self.badge_values)
        badge_api.publish_badge(badge['uri'])

        project_values = self.project_values.copy()
        project_values['badge_uri'] = badge['uri']
        project = project_api.create_project(**project_values)

        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 0)
        
        with self.assertRaises(Exception):
            project_api.submit_feedback(project['uri'], '/uri/user/not_an_expert', 'Ugly', 'Bad', 'Good')

        project_api.submit_feedback(project['uri'], badge['author_uri'], 'Ugly', 'Bad', 'Good')
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 1)


    def test_final_feedback(self):
        badge = badge_api.create_badge(**self.badge_values)
        badge_api.publish_badge(badge['uri'])

        project_values = self.project_values.copy()
        project_values['badge_uri'] = badge['uri']
        project = project_api.create_project(**project_values)

        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 0)
        
        self.assertTrue(project_api.ready_for_feedback(project['uri']))
        project_api.submit_feedback(project['uri'], badge['author_uri'], 'Ugly', 'Bad', 'Good', True)
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 1)

        self.assertFalse(project_api.ready_for_feedback(project['uri']))
        self.assertFalse(project_api.can_revise_project(project['uri']))

