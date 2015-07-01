from datetime import datetime
from dashboard.tests.ck_editor_object import Ckeditor
from p2pu_user.models import User
from django.core.urlresolvers import reverse

from test import SeleniumTestCase
from webdriver import CustomWebDriver


class Auth(SeleniumTestCase):
    def setUp(self):
        # setUp is where setup call fixture creation scripts
        # and instantiate the WebDriver, which in turns loads up the browser.
        self.user = User.objects.create(username='test_user',
                                        image_url='http://placehold.it/40x40',
                                        email='user@test.com',
                                        date_joined=datetime.utcnow(),
                                        date_updated=datetime.utcnow(),
                                        )

        # Instantiating the WebDriver will load your browser
        self.wd = CustomWebDriver()

    def tearDown(self):
        # Don't forget to call quit on your webdriver, so that
        # the browser is closed after the tests are ran
        self.wd.quit()

    """
    def test_open(self):
        #Django Admin login test


        # Login
        #url = reverse('dashboard', args=[self.user.username])
        #self.open(url)
        url = reverse('become', args=[self.user.username])
        self.open(url=url)
        self.wd.wait_for_css('[title="%s\'s Dashboard"]' % self.user.username)

        # Open the dashboard page
        self.wd.find_css('#user_dashboard_btn').click()
        self.wd.wait_for_css('.user-img')

        body = self.wd.find_element_by_tag_name('body')
        self.assertIn('Projects that need your feedback', body.text)
        self.assertIn('Get Your Own Nifty Badge!', body.text)
        self.wd.find_element_by_link_text('Browse')

        # Create a Badge
        self.wd.find_element_by_link_text('Create a Badge').click()
        self.wd.wait_for_css('.preview-badge-button')
        body = self.wd.find_element_by_tag_name('body')
        self.assertIn('Create a Badge', body.text)

        self.wd.find_css('#id_title').send_keys("Test Badge")
        self.wd.find_css('#id_description').send_keys("Test Badge description")
        self.pause(5)

        #cke_element = Ckeditor(self.wd.find_element_by_id('cke_id_requirements'))
        #cke_element.clear()
        #cke_element.send_keys('Hello World!')
        #print cke_element.text
    """

