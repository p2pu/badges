from datetime import datetime
from p2pu_user.models import User
from django.core.urlresolvers import reverse

from test import SeleniumTestCase
from webdriver import CustomWebDriver


class Auth(SeleniumTestCase):
    def setUp(self):
        # setUp is where setup call fixture creation scripts
        # and instantiate the WebDriver, which in turns loads up the browser.
        self.user = User.objects.create(username='erika',
                                        image_url='http://placehold.it/40x40',
                                        email='erika@p2pu.com',
                                        date_joined=datetime.utcnow(),
                                        date_updated=datetime.utcnow(),
                                        )

        # Instantiating the WebDriver will load your browser
        self.wd = CustomWebDriver()

    def tearDown(self):
        # Don't forget to call quit on your webdriver, so that
        # the browser is closed after the tests are ran
        self.wd.quit()

    def test_open(self):
        """
        Django Admin login test
        """

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

        iframe = self.wd.find_elements_by_tag_name("iframe")
        """
        self.wd.switch_to_window(iframe)

        tinymce = self.wd.find_elements_by_tag_name("body")
        tinymce.clear()
        tinymce.send_keys("Test Badge requirements")

        self.wd.find_css('.preview-badge-button').click()
        self.wd.wait_for_css('#div_id_image_uri .required')
        self.pause(5000)
        """
        # Selenium knows it has to wait for page loads (except for AJAX requests)
        # so we don't need to do anything about that, and can just
        # call find_css. Since we can chain methods, we can
        # call the built-in send_keys method right away to change the
        # value of the field
        #self.wd.find_css('#id_username').send_keys("admin")
        # for the password, we can now just call find_css since we know the page
        # has been rendered
        #self.wd.find_css("#id_password").send_keys('pw')
        # You're not limited to CSS selectors only, check
        # http://seleniumhq.org/docs/03_webdriver.html for
        # a more compreehensive documentation.
        #self.wd.find_element_by_xpath('//input[@value="Log in"]').click()
        # Again, after submiting the form, we'll use the find_css helper
        # method and pass as a CSS selector, an id that will only exist
        # on the index page and not the login page
        #self.wd.find_css("#content-main")

