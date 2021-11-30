from django.test import TestCase, Client
from django.shortcuts import reverse
from TA_Scheduler.models import Account


class TestLogin(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.session = self.client.session

    # idk what this is for
    def test_get_user_and_validate(self):

    def test_noUsername(self):
        resp = self.client.post("/login.html", {"username": "", "password": "password"})
        self.assertEqual("Fields are empty", resp.context["message"], "no username")

    def test_noPassword(self):
        resp = self.client.post("/login.html", {"username": "user", "password": ""})
        self.assertEqual("Fields are empty", resp.context["message"], "no password")

    def test_noInput(self):
        resp = self.client.post("/login.html", {"username": "", "password": ""})
        self.assertEqual("Fields are empty", resp.context["message"], "no inputs")

    def test_success(self):
        resp = self.client.post("/login.html", {"username": "username", "password": "password"}, follow=True)
        self.assertEqual(('/home/', 302), resp.redirect_chain[0], "new user not redirected")
