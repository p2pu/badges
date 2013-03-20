from django.test import TestCase
from ludibrio import Stub
from ludibrio.matcher import any
from badge import models as badge_api
from project import models as project_api

class ProjectTest(TestCase):


    def test_get_badge_uri_from_project_under_revision(self):

        # setup
        with Stub() as send_badge_creation_notification:
            from badge.notification_helpers import send_badge_creation_notification
            send_badge_creation_notification(any())

        badge = badge_api.create_badge('Title badge 1', '/media/img/1.png', 'desc', 'reqs', '/uri/user/2' )

        with Stub() as send_project_creation_notification:
            from project.notification_helpers import send_project_creation_notification
            send_project_creation_notification(any())

        with Stub() as send_project_creation_expert_notification:
            from project.notification_helpers import send_project_creation_expert_notification
            send_project_creation_expert_notification(any(), any(), any())

        project = project_api.create_project('/uri/badge/1', '/uri/user/user1', 'Title project 1', '/uri/image/1', 'https://url.com', 'Description', 'Reflection', ['tag1', 'tag2'])

        # run
        badge_uri = project_api.get_badge_uri_from_project_under_revision(project['uri'])

        # assert
        self.assertEquals('/uri/badge/1', badge_uri)

        # setup
        with Stub() as send_feedback_notification:
            from project.notification_helpers import send_feedback_notification
            send_feedback_notification(any())

        project_api.submit_feedback(project['uri'], '/uri/user/2' ,'good', 'bad', 'ugly', badge_awarded=True)

        # run
        badge_uri = project_api.get_badge_uri_from_project_under_revision(project['uri'])

        # assert
        self.assertEquals(None, badge_uri)

