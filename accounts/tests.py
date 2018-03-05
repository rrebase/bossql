from django.test import TestCase
from .backends import EmailOrUsernameModelBackend;

# Create your tests here.


class AccountsTestCase(TestCase):
    def setUp(self):
        email = EmailOrUsernameModelBackend()
