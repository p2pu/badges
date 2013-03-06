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


    def test_get_projects(self):
        project = project_api.create_project(**self.project_values)
        project_values2 = self.project_values.copy()
        project_values2['user_uri'] = '/uri/user/testuser2'
        project = project_api.create_project(**project_values2)
        project_values2['user_uri'] = '/uri/user/testuser3'
        project = project_api.create_project(**project_values2)
        project_values2['badge_uri'] = '/uri/badge/3'
        project = project_api.create_project(**project_values2)

        projects = project_api.get_projects()
        self.assertEqual(len(projects), 4)


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
