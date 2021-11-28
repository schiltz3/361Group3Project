from django.test import TestCase, Client
from .models import Account


class NewAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        m = Account(username="user", password="pass")
        m.save()
        # do I have to navigate to createaccounts page or can I just start there??
        # self.client.post("/login.html", {"name": "user", "password": "pass"})
        # self.client.post("/home.html", select button? to go to createaccounts)

    def test_valid(self):
        response = self.client.post("/createaccounts.html", {"username": "new", "password": "password"})
        self.assertEqual("account 'new' created", response.context["message"], "confirmation message not given")

    def test_inDatabase(self):
        self.client.post("/createaccounts.html", {"username": "new", "password": "password"})
        self.assertEqual(Account(username="new", password="password"), Account.objects.get(username="new"))

    # how would i test for when there's no username/password? (they're required in the html)

    def test_usernameTaken(self):
        response = self.client.post("/createaccounts.html", {"username": "user", "password": "password"})
        self.assertEqual("username 'user' is already in use", response.context["message"], "username already taken")

    def test_noNewDuplicate(self):
        self.client.post("/createaccounts.html", {"username": "user", "password": "password"})
        #make sure casting to dict and getting length is correct
        self.assertEqual(1, dict(Account.objects.filter(username="user")).length, "duplicate user created")

