# -*- coding: utf-8 -*-
from datetime import datetime
from django.test import TestCase
from mock import patch, Mock

from badge.models import Badge
from badge.models import award_badge
from badge.models import get_badges_by_user
from badge.models import _badge2dict

from project.models import Project

from p2pu_user.models import save_user
from p2pu_user.models import username2uri

from dashboard.processors import list_projects_ready_for_feedback
from project.processors import submit_feedback


class TestDashboard(TestCase):
    def _get_image(self):
        return 'http://placehold.it/40x40'

    def _create_user(self, username):
        user = save_user(username=username, image_url=self._get_image(),
                         email='testing@email.com')
        return user

    def _create_badge(self, username, title):
        """
        :param username:
        :param title:
        :rtype : dict
        """
        badge = Badge.objects.create(title=title,
                                     image_uri=self._get_image(),
                                     description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
                                     requirements='Ed sagittis aliquam tellus nec bibendum. ',
                                     author_uri=username2uri(username),
                                     date_created=datetime.utcnow(),
                                     date_updated=datetime.utcnow(),
                                     date_published=datetime.utcnow(), )
        return _badge2dict(badge)

    def _create_project(self, badge_uri, username):
        project = Project.objects.create(badge_uri=badge_uri,
                                         author_uri=username2uri(username),
                                         title='Test Projects',
                                         image_uri=self._get_image,
                                         work_url='http://testing.url',
                                         description='Vestibulum id pellentesque tortor, at rhoncus nisi',
                                         reflection='Vestibulum eleifend, dui nec congue elementum, diam purus sempe',
                                         date_created=datetime.utcnow(),
                                         date_updated=datetime.utcnow(), )
        return project

    def test_user_has_no_badges(self):
        """
        Testing when user has no Badges
        """

        #setup
        user_one = self._create_user('username_one')
        badges = get_badges_by_user(username2uri(user_one['username']))

        #run
        projects = list_projects_ready_for_feedback(badges)

        #verify
        self.assertEquals(projects, [])
        self.assertEquals(len(badges), 0)

    def test_user_has_badges_but_no_projects_that_need_feedback(self):
        """
        Testing when user has Badges, but has not had Project submitted for their Badge
        """

        #setup
        user_one = self._create_user('username_one')
        badge = self._create_badge(user_one['username'], 'Test badge')
        badges = get_badges_by_user(username2uri(user_one['username']))

        #run
        projects = list_projects_ready_for_feedback(badges)

        #verify
        self.assertEquals(len(badges), 1)
        self.assertEquals(badges[0]['title'], badge['title'])
        self.assertEquals(projects, [])

    @patch('dashboard.processors.fetch_resources', lambda x, feedback_list=None: x)
    def test_get_products_that_need_feedback_from_user(self):
        """
        Testing when user gets submitted Project for their Badge
        """

        #setup
        user_one = self._create_user('username_one')
        badge = self._create_badge(user_one['username'], 'Test Badge')
        badges = get_badges_by_user(username2uri(user_one['username']))

        user_two = self._create_user('username_two')
        submitted_project = self._create_project(badge['uri'], user_two['username'])

        #run
        #with patch('media.processors.get_image', new=lambda x: {}):
        projects = list_projects_ready_for_feedback(badges)

        #verify
        self.assertEquals(len(projects), 1)
        #self.assertEquals(projects[0]['badge']['title'], badge['title'])
        self.assertEquals(projects[0]['title'], submitted_project.title)

    def test_user_has_multiple_badges_none_project(self):
        """
        Testing when user gets submitted Project for their Badge
        """

        #setup
        user_one = self._create_user('username_one')
        self._create_badge(user_one['username'], 'Test Badge 1')
        self._create_badge(user_one['username'], 'Test Badge 2')
        badges = get_badges_by_user(username2uri(user_one['username']))

        #run
        projects = list_projects_ready_for_feedback(badges)

        #verify
        self.assertEquals(len(projects), 0)
        self.assertEquals(len(badges), 2)

    @patch('dashboard.processors.fetch_resources', lambda x, feedback_list=None: x)
    def test_user_has_multiple_badges_one_project(self):
        """
        Testing when user gets submitted Project for their Badge
        """

        #setup
        user_one = self._create_user('username_one')
        badge_1 = self._create_badge(user_one['username'], 'Test Badge 1')
        self._create_badge(user_one['username'], 'Test Badge 2')
        badges = get_badges_by_user(username2uri(user_one['username']))

        user_two = self._create_user('username_two')
        submitted_project = self._create_project(badge_1['uri'], user_two['username'])

        #run
        projects = list_projects_ready_for_feedback(badges)

        #verify
        self.assertEquals(len(projects), 1)
        self.assertEquals(len(badges), 2)

    @patch('project.processors.send_feedback_notification', lambda x: x)
    @patch('dashboard.processors.fetch_resources', lambda x, feedback_list=None: x)
    def test_get_products_after_badge_was_already_awarded(self):
        """
        Testing dashboard after badge has been awarded
        """
        #setup
        user_one = self._create_user('username_one')
        badge = self._create_badge(user_one['username'], 'Test Badge')
        badges = get_badges_by_user(username2uri(user_one['username']))

        user_two = self._create_user('username_two')
        submitted_project = self._create_project(badge['uri'], user_two['username'])

        award_badge(badge_uri=badge['uri'],
                    user_uri=username2uri(user_one['username']),
                    expert_uri=username2uri(user_one['username']),
                    evidence_url='http://evidence.test')

        submit_feedback(
            '/uri/project/%s' % submitted_project.id,
            user_one['uri'],
            'Good',
            'Bad',
            'Ugly',
            award_badge=True,
        )
        #run
        projects = list_projects_ready_for_feedback(badges)

        #verify
        self.assertEquals(len(projects), 0)

