from django.test import TestCase
from mock import patch

from project import models as project_api


class SimpleTest(TestCase):

    project_values = {
        'badge_uri': '/uri/badge/1',
        'author_uri': '/uri/user/testuser/',
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
        project_values2['author_uri'] = '/uri/user/testuser2'
        project = project_api.create_project(**project_values2)
        project_values2['author_uri'] = '/uri/user/testuser3'
        project = project_api.create_project(**project_values2)
        project_values2['badge_uri'] = '/uri/badge/3'
        project = project_api.create_project(**project_values2)

        projects = project_api.get_projects()
        self.assertEqual(len(projects), 4)


    def test_get_projects_for_badge(self):
        project = project_api.create_project(**self.project_values)
        project_values2 = self.project_values.copy()
        project_values2['author_uri'] = '/uri/user/testuser2'
        project = project_api.create_project(**project_values2)
        project_values2['author_uri'] = '/uri/user/testuser3'
        project = project_api.create_project(**project_values2)
        project_values2['badge_uri'] = '/uri/badge/3'
        project = project_api.create_project(**project_values2)

        projects = project_api.get_projects_for_badge(self.project_values['badge_uri'])
        self.assertEqual(len(projects), 3)


    def test_search_projects(self):
        project_api.create_project('/uri/badge/1', '/uri/user/user1', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/1', '/uri/user/user2', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/1', '/uri/user/user3', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        project_api.create_project('/uri/badge/2', '/uri/user/user1', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/2', '/uri/user/user4', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/2', '/uri/user/user5', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        project_api.create_project('/uri/badge/3', '/uri/user/user1', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/3', '/uri/user/user6', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        projects = project_api.search_projects(author_uri='/uri/user/user1')
        self.assertEqual(len(projects), 3)

        projects = project_api.search_projects(badge_uri='/uri/badge/3')
        self.assertEqual(len(projects), 2)
        
        projects = project_api.search_projects(author_uri='/uri/user/user1', badge_uri='/uri/badge/2')
        self.assertEqual(len(projects), 1)
        
        projects = project_api.search_projects(author_uri='/uri/user/user2', badge_uri='/uri/badge/3')
        self.assertEqual(len(projects), 0)


    def test_get_projects_ready_for_feedback(self):
        project_api.create_project('/uri/badge/1', '/uri/user/user1', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/1', '/uri/user/user2', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/1', '/uri/user/user3', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        project_api.create_project('/uri/badge/2', '/uri/user/user1', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/2', '/uri/user/user4', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/2', '/uri/user/user5', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        project_api.create_project('/uri/badge/3', '/uri/user/user1', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])
        project_api.create_project('/uri/badge/3', '/uri/user/user6', 'Title', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        projects_ready_for_feedback = project_api.get_projects_ready_for_feedback('/uri/badge/1')
        self.assertEqual(len(projects_ready_for_feedback), 3)
