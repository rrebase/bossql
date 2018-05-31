from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class AccountsSeleniumTests(StaticLiveServerTestCase):
    selenium = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.register('test1', 'test1@gmail.com', 'testparool1')

    def register(self, user, mail, password):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/register'))

        username = self.selenium.find_element_by_id('id_username')
        username.send_keys(user)

        email = self.selenium.find_element_by_id('id_email')
        email.send_keys(mail)

        password1 = self.selenium.find_element_by_id('id_password1')
        password1.send_keys(password)

        password2 = self.selenium.find_element_by_id('id_password2')
        password2.send_keys(password)

        button = self.selenium.find_element_by_id('sign_up')
        button.submit()

    def log_in(self, user, pwd):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login'))
        username = self.selenium.find_element_by_id('id_username')
        username.send_keys(user)

        password = self.selenium.find_element_by_id('id_password')
        password.send_keys(pwd)

        form = self.selenium.find_element_by_id('log_in')
        form.submit()

    def reset_visible(self):
        self.log_in('test1', 'testparool1')
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/test1'))
        btn = self.selenium.find_element_by_id('change_settings')
        btn.click()
        check_box = self.selenium.find_element_by_id('id_allow_seen_in_stats')
        if not check_box.is_selected():
            check_box.click()
            button = self.selenium.find_element_by_id('save_settings')
            button.submit()

    def turn_off_email_public(self):
        self.log_in('test1', 'testparool1')
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/test1'))
        check_box = self.selenium.find_element_by_id('id_is_email_public')
        if check_box.is_selected():
            check_box.click()
            button = self.selenium.find_element_by_class_name('my-4')
            button.submit()

    def log_out(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/logout'))

    @skip
    def test_email_public(self):
        self.turn_off_email_public()
        self.log_out()
        self.log_in('test2', 'testparool2')
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/test1/'))
        self.assertTrue('Email:' not in self.selenium.page_source)

    def test_other_user_settings_changeable(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/test2/'))
        source = self.selenium.page_source
        self.assertTrue('Change settings:' not in source)

    def test_log_out(self):
        self.log_out()
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertTrue('You are not logged in!' in self.selenium.page_source)

    def test_visibility_in_stats(self):
        self.log_out()
        self.reset_visible()
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/test1/'))
        btn = self.selenium.find_element_by_id('change_settings')
        btn.click()
        check_box = self.selenium.find_element_by_id('id_allow_seen_in_stats')
        check_box.click()
        button = self.selenium.find_element_by_id('save_settings')
        button.submit()
        self.selenium.get('%s%s' % (self.live_server_url, '/stats/'))
        content = self.selenium.find_element_by_class_name('table-striped').text
        self.assertFalse('test1' in content)
