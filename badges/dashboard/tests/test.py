from django.test import LiveServerTestCase


class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for selenium, providing helper methods for generating
    clients and logging in profiles.
    """

    def open(self, url):
        self.wd.get("%s%s" % (self.live_server_url, url))