from django.test import TestCase, Client
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group


class NewAccountTest(TestCase):
    def setUp(self):
        Group.objects.create(name="admin")
        self.client = Client()
        AccountUtil.createAdminAccount(username="user", password="pass")
        # do I have to navigate to createaccounts page or can I just start there??
        # self.client.post("/login.html", {"name": "user", "password": "pass"})
        # self.client.post("/testhome.html", select button? to go to createaccounts)

    def test_admin(self):
        response = self.client.post(
            "account/create.html",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "message": "test",
            },
        )
        self.assertEqual(
            "Administrator account 'new' created",
            response.context.get("message"),
            "admin confirmation message not given",
        )

    def test_instructor(self):
        response = self.client.post(
            "account/create.html",
            {"username": "new", "password": "password", "authority": "2"},
        )
        self.assertEqual(
            "Instructor account 'new' created",
            response.context.get("message"),
            "instructor confirmation message not given",
        )

    def test_ta(self):
        response = self.client.post(
            "account/create.html",
            {"username": "new", "password": "password", "authority": "3"},
        )
        self.assertEqual(
            "TA account 'new' created",
            response.context.get("message"),
            "ta confirmation message not given",
        )

    def test_inDatabase(self):
        self.client.post(
            "account/create.html",
            {"username": "new", "password": "password", "authority": "1"},
        )
        self.assertNotEqual(None, AccountUtil.getAccountByUsername("new"))

    def test_noUsername(self):
        self.client.post(
            "account/create.html",
            {"username": "", "password": "password", "authority": "1"},
        )
        self.assertEqual(
            1,
            (AccountUtil.getAllAccounts()).count(),
            "new user created even though no username entered",
        )

    def test_noPassword(self):
        self.client.post(
            "account/create.html", {"username": "new", "password": "", "authority": "1"}
        )
        self.assertEqual(
            1,
            (AccountUtil.getAllAccounts()).count(),
            "new user created even though no password entered",
        )

    def test_usernameTaken(self):
        response = self.client.post(
            "account/create.html",
            {"username": "user", "password": "password", "authority": "1"},
        )
        self.assertEqual(
            "username 'user' is already in use",
            response.context.get("message"),
            "username already taken",
        )

    def test_noNewDuplicate(self):
        self.client.post(
            "account/create.html",
            {"username": "user", "password": "password", "authority": "1"},
        )
        self.assertEqual(
            1,
            Account.objects.all().count(),
            "new user created even though duplicate username entered",
        )

    def test_noAuthority(self):
        response = self.client.post(
            "account/create.html",
            {"username": "user", "password": "password", "authority": ""},
        )
        self.assertEqual("enter user type", response.context.get("message"))
