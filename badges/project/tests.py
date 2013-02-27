"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from project import api as project_api


class SimpleTest(TestCase):

    def test_create_project(self):
        project = project_api.create_project(
            "Title",
            "http://project.org/url",
            "/uri/image/1"
        )

        self.assertTrue("uri" in project)
        self.assertTrue("title" in project)
        self.assertTrue("user_uri" in project)
        self.assertTrue("work_url" in project)

