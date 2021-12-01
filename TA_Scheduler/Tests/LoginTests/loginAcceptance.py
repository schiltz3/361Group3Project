from django.test import TestCase, Client
from django.views import View
from TA_Scheduler.utilities.AccountUtil import AccountUtil

# Create your tests here.


class LoginTests(TestCase):
    def setup(self):
        self.client = Client()
        self.user1 = AccountUtil.createAccount(username="admin", password="pass123", authority="3")
        self.user1.save()

    def test_Redirect(self):
        resp = self.client.post("/login/", {"Username": "admin", "password": "pass123"}, follow=True)
        self.assertRedirects(resp, "/home/")

    def test_InvalidUser(self):
        resp = self.client.post("/login/", {"username": "someone", "password": "abc123"}, follow=True)
        self.assertEqual(resp.context["error"], "invalid user", "Login failed, user not found")

    def test_badPassword(self):
        resp = self.client.post("/login/", {"username": "admin", "password": "abc123"}, follow=True)
        self.assertEqual(resp.context["error"], "bad password", "Failed login, password incorrect")

