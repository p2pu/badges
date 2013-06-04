from django.test import TestCase
from mock import patch, Mock

from project import processors as project_api
from badge import models as badge_api
from p2pu_user import models as p2pu_user_api


@patch('project.notification_helpers.fetch_resources', lambda x: x)
@patch('badge.notification_helpers.fetch_badge_resources', lambda x: x)
class ProjectIntegrationTests(TestCase):

    badge_values = {
        'title': 'Movie Maker',
        'image_uri': '/uri/image/1',
        'description': 'Create a short movie',
        'requirements': 'Create a movie and upload it to youtube or vimeo',
        'author_uri': '/uri/user/badgemaker',
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
        # create badge
        badge = badge_api.create_badge(**self.badge_values)
        badge_api.publish_badge(badge['uri'])
        user = p2pu_user_api.save_user('badgemaker', 'http://placeholdit.com/40x40', 'some@email.com')

        # create project
        project_values = self.project_values.copy()
        project_values['badge_uri'] = badge['uri']
        project = project_api.create_project(**project_values)

        # get feedback - has to be zero, there was not any feedback submitted yet
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 0)

        # test that project can be revised - it can not, there has not been feedback given yet
        self.assertFalse(project_api.can_revise_project(project['uri']))

        # test that error is raised when revision is given - it has to be, there was no feedback given yet
        with self.assertRaises(Exception):
            project_api.revise_project(project['uri'], 'All better')

        # test that project is ready for feedback
        self.assertTrue(project_api.ready_for_feedback(project['uri']))

        # submit feedback
        project_api.submit_feedback(project['uri'], '/uri/user/badgemaker', 'Ugly', 'Bad', 'Good')
        project_feedback = project_api.get_project_feedback(project['uri'])

        self.assertEqual(len(project_feedback), 1)
        self.assertIn('good', project_feedback[0])
        self.assertIn('bad', project_feedback[0])
        self.assertIn('ugly', project_feedback[0])
        self.assertIn('expert_uri', project_feedback[0])

        # test that multiple feedback cannont be submitted without a revision
        #self.assertFalse(project_api.ready_for_feedback(project['uri']))
        #with self.assertRaises(Exception):
        #    project_api.submit_feedback(project['uri'], '/uri/user/badgemaker', 'Ugly', 'Bad', 'Good')

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
        user = p2pu_user_api.save_user('badgemaker', 'http://placeholdit.com/40x40', 'some@email.com')

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
        user = p2pu_user_api.save_user('badgemaker', 'http://placeholdit.com/40x40', 'some@email.com')

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

    @patch('project.processors.get_badge_experts', lambda uri:['/uri/user/2'])
    def test_get_badge_uri_from_project_under_revision(self):
        # create badge
        badge = badge_api.create_badge('Title badge 1', '/media/img/1.png', 'desc', 'reqs', '/uri/user/2' )
        project = project_api.create_project('/uri/badge/1', '/uri/user/user1', 'Title project 1', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        # get badge uri from a project which is unde revision
        badge_uri = project_api.get_badge_uri_from_project_under_revision(project['uri'])

        # check badge uri
        self.assertEquals('/uri/badge/1', badge_uri)

        # submit feedback award badge
        project_api.submit_feedback(project['uri'], '/uri/user/2', 'good', 'bad', 'ugly', award_badge=True)

        # check badge uri
        badge_uri = project_api.get_badge_uri_from_project_under_revision(project['uri'])

        # check there is no more project after badge was awarded
        self.assertEquals(None, badge_uri)

    def test_award_partner_badge_as_partne(self):

        #create a partner
        partner = p2pu_user_api.create_partner('test partner')

        # create a parnter badge
        badge_values = self.badge_values.copy()
        badge_values['partner_name'] = partner['name']
        badge =badge_api.create_badge(**badge_values)
        badge_api.publish_badge(badge['uri'])

        # submit a project for a badge
        project_values = self.project_values.copy()
        project_values['badge_uri'] = badge['uri']
        project = project_api.create_project(**project_values)

        # give feedback as a partner
        feedback = project_api.submit_feedback(
            project['uri'],
            self.badge_values['author_uri'],
            'Good',
            'Bad',
            'Ugly',
            )
        self.assertEquals(feedback, project_api.submit_feedback_result.NOT_AWARDED)

        # revise feedback
        revision = project_api.revise_project(project['uri'], 'Some improvement')
        self.assertEquals('Some improvement', revision['improvement'])

        # give feedback and award a badge
        feedback = project_api.submit_feedback(
            project['uri'],
            self.badge_values['author_uri'],
            'SecondGood',
            'SecondBad',
            'SecondUgly',
            award_badge=True
        )
        self.assertEquals(feedback, project_api.submit_feedback_result.AWARDED)


    def test_badge_awarded_from_nonpartner_expert(self):
        #create a partner
        partner = p2pu_user_api.create_partner('Test parnter')

        # create partner badge
        new_badge_values = self.badge_values.copy()
        new_badge_values['partner_name'] = partner['name']

        # create a parnter badge
        badge = badge_api.create_badge(**new_badge_values)
        badge_api.publish_badge(badge['uri'])

        # submit a project for a badge
        project_values = self.project_values.copy()
        project_values['badge_uri'] = badge['uri']
        project = project_api.create_project(**project_values)

        # award badge as a partner
        feedback = project_api.submit_feedback(
            project['uri'],
            badge['author_uri'],
            'Good',
            'Bad',
            'Ugly',
            award_badge=True
            )
        self.assertEquals(feedback, project_api.submit_feedback_result.AWARDED)
        # award badge
        # HACK - needs well revision on how to refactor in order to test cycle properly
        if project_api.submit_feedback_result.AWARDED:
            with patch('badge.models.send_badge_awarded_notification') as mock_notification:
                badge_api.award_badge(badge['uri'], project_values['author_uri'], badge['author_uri'], 'http://project.org/url')

        self.assertIn(project_values['author_uri'], badge_api.get_badge_experts(badge['uri']))
        # submit another project for a badge
        another_project_values = {
            'badge_uri': badge['uri'],
            'author_uri': '/uri/user/anotheruser',
            'title': 'Test Second Title',
            'image_uri': '/uri/image/2',
            'work_url': 'http://project.org/url',
            'description': 'Did the test second time',
            'reflection': 'Will not do it earlier and more next time',
            'tags': ['test', 'tdd', 'bdd'],
        }
        project = project_api.create_project(**another_project_values)

        # award badge as a non partner
        feedback = project_api.submit_feedback(
            project['uri'],
            '/uri/user/testuser',
            'Good',
            'Bad',
            'Ugly',
            award_badge=True
            )
        self.assertEquals(feedback, project_api.submit_feedback_result.REQUIRES_APPROVAL)

        # award badge as partner
        feedback = project_api.submit_feedback(
            project['uri'],
            badge['author_uri'],
            'Good',
            'Bad',
            'Ugly',
            award_badge=True
        )
        self.assertEquals(feedback, project_api.submit_feedback_result.AWARDED)

        # test that feedback can not be given anymore
        with self.assertRaises(Exception):
            project_api.submit_feedback(
                project['uri'],
                badge['author_uri'],
                'Good',
                'Bad',
                'Ugly',
                award_badge=True
            )

        # test that revision can not be given any longer either
        with self.assertRaises(Exception):
            project_api.revise_project(project['uri'], 'Some improvement')