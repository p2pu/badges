from datetime import datetime
from p2pu_user.models import User
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Auth(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user',
                                        image_url='http://placehold.it/40x40',
                                        email='user@test.com',
                                        date_joined=datetime.utcnow(),
                                        date_updated=datetime.utcnow(),)

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(Auth, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(Auth, cls).tearDownClass()

    def test_login(self):
        url = reverse('become', args=[self.user.username])
        self.selenium.get('%s%s' % (self.live_server_url, url))

        wait = WebDriverWait(self.selenium, 10)
        dashboard = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#user_dashboard_btn')))
        dashboard.click()

        title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.user h3')))
        self. assertEquals(title.text, self.user.username)

        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Projects that need your feedback', body.text)
        self.assertIn('Get Your Own Nifty Badge!', body.text)
        self.selenium.find_element_by_link_text('Browse')

        # Create a Badge
        badge = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Create a Badge')))
        badge.click()

        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.preview-badge-button')))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Create a Badge', body.text)

        badge_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#id_title')))
        badge_title.send_keys("Test Badge")
        badge_id = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#id_description')))
        badge_id.send_keys("Test Badge description")
        self.selenium.implicitly_wait(10)


