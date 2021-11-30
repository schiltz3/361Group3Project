from django.test import TestCase, Client
from .models import Account
from django.contrib.auth.models import User


class NewAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        m = Account(user=User(username="user", password="pass", first_name="first", last_name="last"))
        m.save()
        # do I have to navigate to createaccounts page or can I just start there??
        # self.client.post("/login.html", {"name": "user", "password": "pass"})
        # self.client.post("/home.html", select button? to go to createaccounts)

    def test_valid(self):
        response = self.client.post("/createaccounts.html", {"username": "new", "password": "password"})
        self.assertEqual("account 'new' created", response.context["message"], "confirmation message not given")

    def test_inDatabase(self):
        self.client.post("/createaccounts.html", {"username": "new", "password": "password"})
        self.assertEqual("password", (Account.objects.get(username="new")).password)

    def test_noUsername(self):
        self.client.post("/createaccounts.html", {"username": "", "password": "password"})
        self.assertEqual(1, Account.objects.all().count(), "new user created even though no username entered")

    def test_noPassword(self):
        self.client.post("/createaccounts.html", {"username": "new", "password": ""})
        self.assertEqual(1, Account.objects.all().count(), "new user created even though no password entered")

    def test_usernameTaken(self):
        response = self.client.post("/createaccounts.html", {"username": "user", "password": "password"})
        self.assertEqual("username 'user' is already in use", response.context["message"], "username already taken")

    def test_noNewDuplicate(self):
        self.client.post("/createaccounts.html", {"username": "user", "password": "password"})
        self.assertEqual(1, Account.objects.filter(username="user").count(), "duplicate user created")

