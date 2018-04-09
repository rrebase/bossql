from django.test import TestCase
from selenium import webdriver


class AccountTestCase(TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.register('test1', 'test1@hot.ee', 'testparool1')

    def register(self, user, mail, password):
        self.driver.get('http://localhost:8000/accounts/register')

        username = self.driver.find_element_by_id('id_username')
        username.send_keys(user)

        email = self.driver.find_element_by_id('id_email')
        email.send_keys(mail)

        password1 = self.driver.find_element_by_id('id_password1')
        password1.send_keys(password)

        password2 = self.driver.find_element_by_id('id_password2')
        password2.send_keys(password)

        button = self.driver.find_element_by_id('sign_up')
        button.submit()

    def log_in(self, user, pwd):
        self.driver.get('http://localhost:8000/accounts/login')
        username = self.driver.find_element_by_id('id_username')
        username.send_keys(user)

        password = self.driver.find_element_by_id('id_password')
        password.send_keys(pwd)

        form = self.driver.find_element_by_class_name('btn-primary')
        form.submit()

    def reset_visible(self):
        self.log_in('test1', 'testparool1')
        self.driver.get('http://localhost:8000/accounts/test1/')
        check_box = self.driver.find_element_by_id('id_allow_seen_in_stats')
        if not check_box.is_selected():
            check_box.click()
            button = self.driver.find_element_by_class_name('my-4')
            button.submit()

    def turn_off_email_public(self):
        self.log_in('test1', 'testparool1')
        self.driver.get('http://localhost:8000/accounts/test1/')
        check_box = self.driver.find_element_by_id('id_is_email_public')
        if check_box.is_selected():
            check_box.click()
            button = self.driver.find_element_by_class_name('my-4')
            button.submit()

    def log_out(self):
        self.driver.get('http://localhost:8000/logout')

    def test_email_public(self):
        self.turn_off_email_public()
        self.log_out()
        self.log_in('test2', 'testparool2')
        self.driver.get('http://localhost:8000/accounts/test1/')
        self.assertTrue('Email:' not in self.driver.page_source)

    def test_other_user_settings_changeable(self):
        self.driver.get('http://localhost:8000/accounts/test2/')
        source = self.driver.page_source
        self.assertTrue('Change settings:' not in source)

    def test_log_out(self):
        self.log_out()
        self.driver.get('http://localhost:8000/')
        self.assertTrue('You are not logged in!' in self.driver.page_source)

    def test_visibility_in_stats(self):
        self.log_out()
        self.reset_visible()
        self.driver.get('http://localhost:8000/accounts/test1/')
        check_box = self.driver.find_element_by_id('id_allow_seen_in_stats')
        check_box.click()
        button = self.driver.find_element_by_class_name('my-4')
        button.submit()
        self.driver.get('http://localhost:8000/stats/')
        content = self.driver.find_element_by_class_name('table-striped').text
        self.assertFalse('test1' in content)
