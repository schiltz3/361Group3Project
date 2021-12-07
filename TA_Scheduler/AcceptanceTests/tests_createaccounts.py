from django.test import TestCase, Client
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group


class NewAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        AccountUtil.createAdminAccount(username="user", password="pass")
        # do I have to navigate to createaccounts page or can I just start there??
        # self.client.post("/login.html", {"name": "user", "password": "pass"})
        # self.client.post("/testhome.html", select button? to go to createaccounts)

    def test_admin(self):
        response = self.client.post(
            # account/create.html is the file not the uri you are trying to post to
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
            },
        )
        self.assertEqual(
            "Administrator account 'new' created",
            response.context.get("message"),
            "admin confirmation message not given",
        )

    def test_instructor(self):
        response = self.client.post(
            # account/create.html is the file not the uri you are trying to post to
            "/account/create/",
            {"username": "new", "password": "password", "authority": "2"},
        )
        self.assertEqual(
            "Instructor account 'new' created",
            response.context.get("message"),
            "instructor confirmation message not given",
        )

    def test_ta(self):
        response = self.client.post(
            # account/create.html is the file not the uri you are trying to post to
            "/account/create/",
            {"username": "new", "password": "password", "authority": "3"},
        )
        self.assertEqual(
            "TA account 'new' created",
            response.context.get("message"),
            "ta confirmation message not given",
        )

    def test_inDatabase(self):
        self.client.post(
            # account/create.html is the file not the uri you are trying to post to
            "/account/create/",
            {"username": "new", "password": "password", "authority": "1"},
        )
        self.assertNotEqual(None, AccountUtil.getAccountByUsername("new"))

    def test_noUsername(self):
        # Did not realize that creating an account with no username or password raises a typeErr exception
        with self.assertRaises(TypeError):
            self.client.post(
                # account/create.html is the file not the uri you are trying to post to
                "/account/create/",
                {"username": "", "password": "password", "authority": "1"},
            )

    def test_noPassword(self):
        # Did not realize that creating an account with no username or password raises a typeErr exception
        with self.assertRaises(TypeError):
            self.client.post(
                # account/create.html is the file not the uri you are trying to post to
                "/account/create/",
                {"username": "new", "password": "", "authority": "1"}
            )

    def test_usernameTaken(self):
        response = self.client.post(
            # account/create.html is the file not the uri you are trying to post to
            "/account/create/",
            {"username": "user", "password": "password", "authority": "1"},
        )
        self.assertEqual(
            "username 'user' is already in use",
            response.context.get("message"),
            "username already taken",
        )

    def test_noNewDuplicate(self):
        self.client.post(
            # account/create.html is the file not the uri you are trying to post to
            "/account/create/",
            {"username": "user", "password": "password", "authority": "1"},
        )
        self.assertEqual(
            1,
            Account.objects.all().count(),
            "new user created even though duplicate username entered",
        )

    def test_noAuthority(self):
        response = self.client.post(
            # account/create.html is the file not the uri you are trying to post to
            "/account/create/",
            # User "user" already exists because that is the one you create at the beginning of every single test
            # 2nd you did not handle fields being empty by using request.POST.get("authority") so ir raises a Value
            {"username": "user1", "password": "password", "authority": ""},
        )
        self.assertEqual("Please fill out all fields", response.context.get("message"))

    # added test case to cover last case in authority check
    def test_outOfRangeAuthority(self):
        response = self.client.post(
            "/account/create/",
            {"username": "user1", "password": "password", "authority": "10"},
        )
        self.assertEqual("user type does not exist", response.context.get("message"))
