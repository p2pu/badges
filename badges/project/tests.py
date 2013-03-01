from django.test import TestCase

from project import api as project_api


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


    def test_submit_feedback(self):
        project = project_api.create_project(**self.project_values)
        project_api.submit_feedback(project['uri'], '/uri/user/expert/', 'Ugly', 'Bad', 'Good')
        self.assertTrue(False)


    def test_revise_project(self):
        self.assertTrue(False)
