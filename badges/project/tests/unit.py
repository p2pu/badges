from django.test import TestCase

from project import models as project_api


class SimpleTest(TestCase):

    project_values = {
        'badge_uri': '/uri/badge/1',
        'user_uri': '/uri/user/testuser/',
        'title': 'Test Title',
        'image_uri': '/uri/image/1',
        'work_url': 'http://project.org/url',
        'steps': 'Did the test',
        'reflection': 'Will do it earlier and more next time',
        'tags': ['test', 'tdd'],
    }


    def test_create_project(self):
        project = project_api.create_project(**self.project_values)
        attrs = self.project_values.keys()
        attrs += ['id', 'uri']

        for attr in attrs:
            self.assertIn(attr, project)

        for attr, value in self.project_values.items():
            self.assertEqual(project[attr], value)

        project2 = project_api.get_project(project['uri'])
        self.assertEqual(project, project2)


    def test_one_project_per_badge(self):
        project = project_api.create_project(**self.project_values)
        with self.assertRaises(project_api.MultipleProjectError):
            project_api.create_project(**self.project_values)


    def test_get_projects_for_badge(self):
        project = project_api.create_project(**self.project_values)
        project_values2 = self.project_values.copy()
        project_values2['user_uri'] = '/uri/user/testuser2'
        project = project_api.create_project(**project_values2)
        project_values2['user_uri'] = '/uri/user/testuser3'
        project = project_api.create_project(**project_values2)
        project_values2['badge_uri'] = '/uri/badge/3'
        project = project_api.create_project(**project_values2)

        projects = project_api.get_projects_for_badge(self.project_values['badge_uri'])
        self.assertEqual(len(projects), 3)


    def test_project_feedback_cycle(self):
        project = project_api.create_project(**self.project_values)

        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 0)

        with self.assertRaises(Exception):
            project_api.revise_project(project['uri'], 'All better')

        project_api.submit_feedback(project['uri'], '/uri/user/expert/', 'Ugly', 'Bad', 'Good')
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 1)
        self.assertIn('good', project_feedback[0])
        self.assertIn('bad', project_feedback[0])
        self.assertIn('ugly', project_feedback[0])
        self.assertIn('expert_uri', project_feedback[0])

        # test that multiple feedback cannont be submitted without a revision
        with self.assertRaises(Exception):
            project_api.submit_feedback(project['uri'], '/uri/user/expert/', 'Ugly', 'Bad', 'Good')

        project_api.revise_project(project['uri'], 'everything is better now!!')
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 2)

        project_api.submit_feedback(project['uri'], '/uri/user/expert/', 'Ugly', 'Bad', 'Good')

        project_api.revise_project(project['uri'], 'everything is better now, promise!!', work_url='http://mywork.com/new-and-improved')
        project_feedback = project_api.get_project_feedback(project['uri'])
        self.assertEqual(len(project_feedback), 4)
 
        self.assertIn('improvement', project_feedback[1]) 
        self.assertIn('date_created', project_feedback[1]) 
        self.assertNotIn('work_url', project_feedback[1])

        self.assertIn('improvement', project_feedback[3]) 
        self.assertIn('work_url', project_feedback[3])


