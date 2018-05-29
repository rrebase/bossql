from django.test import TestCase

from accounts.models import CustomUser
from challenges.models import Challenge


class ChallengesTests(TestCase):
    fixtures = ['challenges-test.json']

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testusername',
                                                   email='testusername@hot.ee',
                                                   password='testpassword')

        self.challenge_instance = Challenge.objects.get(pk=3)

    def test_with_incorrect_sql_query(self):
        result = self.challenge_instance.attempt('SELECT lastname, firstname FROM Persons;', self.user)
        self.assertFalse(result[0])

    def test_with_correct_sql_query(self):
        result = self.challenge_instance.attempt('SELECT firstname, lastname FROM Persons;', self.user)
        self.assertTrue(result[0])

    def test_incorrect_attempt(self):
        result = self.challenge_instance.attempt('SELECT lastname, firstname FROM Persons;', self.user)
        self.assertEqual(1, len(self.user.challenge_attempts.filter(challenge=self.challenge_instance)))

    def test_correct_attempt(self):
        result = self.challenge_instance.attempt('SELECT firstname, lastname FROM Persons;', self.user)
        self.assertEqual(1, len(self.user.challenge_attempts.filter(challenge=self.challenge_instance)))

    def test_correct_attempt_sql(self):
        sql = 'SELECT firstname, lastname FROM Persons;'
        result = self.challenge_instance.attempt(sql, self.user)
        self.assertEqual(sql, self.user.challenge_attempts.get(challenge=self.challenge_instance).tried_sql)
