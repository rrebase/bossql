import unittest

from django.conf import settings

from selenium import webdriver


class AccountTestCase(unittest.TestCase):

    def setUp(self):
        chrome_driver = settings.WEBDRIVER
        self.driver = webdriver.Chrome(chrome_driver)
        self.log_in1()
        self.reset_visible()
        self.turn_off_email_public()

    def log_in1(self):
        self.driver.get('http://localhost:8000/accounts/login')
        username = self.driver.find_element_by_id('id_username')
        username.send_keys('mikk125')

        password = self.driver.find_element_by_id('id_password')
        password.send_keys('parool125')

        form = self.driver.find_element_by_class_name('btn-primary')
        form.submit()

    def log_in2(self):
        self.driver.get('http://localhost:8000/accounts/login')
        username = self.driver.find_element_by_id('id_username')
        username.send_keys('mikktest')

        password = self.driver.find_element_by_id('id_password')
        password.send_keys('parooltest')

        form = self.driver.find_element_by_class_name('btn-primary')
        form.submit()

    def reset_visible(self):
        self.driver.get('http://localhost:8000/accounts/mikk125/')
        check_box = self.driver.find_element_by_id('id_allow_seen_in_stats')
        if not check_box.is_selected():
            check_box.click()
            button = self.driver.find_element_by_class_name('mt-3')
            button.submit()

    def turn_off_email_public(self):
        self.driver.get('http://localhost:8000/accounts/mikk125/')
        check_box = self.driver.find_element_by_id('id_is_email_public')
        if check_box.is_selected():
            check_box.click()
            button = self.driver.find_element_by_class_name('mt-3')
            button.submit()

    def log_out(self):
        self.driver.get('http://localhost:8000/logout')

    def test_other_user_settings_changeable(self):
        self.driver.get('http://localhost:8000/accounts/mikktest/')
        source = self.driver.page_source
        self.assertTrue('Change settings:' not in source)

    def test_visibility_in_stats(self):
        self.driver.get('http://localhost:8000/accounts/mikk125/')
        check_box = self.driver.find_element_by_id('id_allow_seen_in_stats')
        check_box.click()
        button = self.driver.find_element_by_class_name('mt-3')
        button.submit()
        self.driver.get('http://localhost:8000/stats/')
        content = self.driver.find_element_by_class_name('table-striped').text
        self.assertFalse('mikk125' in content)

    def test_email_public(self):
        self.log_out()
        self.log_in2()
        self.driver.get('http://localhost:8000/accounts/mikk125/')
        self.assertTrue('Email:' not in self.driver.page_source)

    def test_log_in(self):
        self.driver.get('http://localhost:8000/')
        self.assertTrue(
            'Logged in as <a href="/accounts/mikk125/" style="color: green">mikk125</a>!' in self.driver.page_source)

    def test_log_out(self):
        self.log_out()
        self.driver.get('http://localhost:8000/')
        self.assertTrue('You are not logged in!' in self.driver.page_source)

    def tearDown(self):
        self.log_out()
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
