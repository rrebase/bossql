import unittest

from selenium import webdriver


class AccountTestCase(unittest.TestCase):

    def setUp(self):
        chrome_driver = '/home/mikk/Downloads/chromedriver_linux64/chromedriver'
        self.driver = webdriver.Chrome(chrome_driver)
        self.log_in('mikk125', 'parool125')
        self.resetVisible()
        self.turnOffEmailPublic()

    def log_in(self, user, pwd):
        self.driver.get('http://localhost:8000/accounts/login')
        username = self.driver.find_element_by_id('id_username')
        username.send_keys(user)

        password = self.driver.find_element_by_id('id_password')
        password.send_keys(pwd)

        form = self.driver.find_element_by_class_name('btn-primary')
        form.submit()

    def resetVisible(self):
        self.driver.get('http://localhost:8000/accounts/mikk125/')
        checkBox = self.driver.find_element_by_id('id_allow_seen_in_stats')
        if not checkBox.is_selected():
            checkBox.click()
            button = self.driver.find_element_by_class_name('mt-3')
            button.submit()

    def turnOffEmailPublic(self):
        self.driver.get('http://localhost:8000/accounts/mikk125/')
        checkBox = self.driver.find_element_by_id('id_is_email_public')
        if checkBox.is_selected():
            checkBox.click()
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
        checkBox = self.driver.find_element_by_id('id_allow_seen_in_stats')
        checkBox.click()
        button = self.driver.find_element_by_class_name('mt-3')
        button.submit()
        self.driver.get('http://localhost:8000/stats/')
        content = self.driver.find_element_by_class_name('table-striped').text
        self.assertFalse('mikk125' in content)

    def test_email_public(self):
        self.log_out()
        self.log_in('mikktest', 'parooltest')
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
