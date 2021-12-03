from django.test import TestCase, Client
from TA_Scheduler.utilities.AccountUtil import AccountUtil

# Create your tests here.


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        AccountUtil.createAccount(username="admin", password="pass123", authority=3)

    def test_Redirect(self):
        resp = self.client.post("/", {"username": "admin", "password": "pass123"},
                                follow=True)
        self.assertRedirects(resp, "/home/")

    def test_InvalidUser(self):
        resp = self.client.post("/", {"username": "someone", "password": "abc123"},
                                follow=True)
        self.assertEqual("invalid username", resp.context["error"], "Login failed, user not found")

    def test_badPassword(self):
        resp = self.client.post("/", {"username": "admin", "password": "abc123"},
                                follow=True)
        self.assertEqual("invalid password", resp.context["error"], "Failed login, password incorrect")

    def test_blankPassword(self):
        resp = self.client.post("/", {"username": "admin", "password": ""}, follow=True)
        self.assertEqual("invalid password", resp.context["error"], "Must input password")

