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
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "Administrator account 'new' created",
            response.context.get("message"),
            "admin confirmation message not given",
        )

    def test_instructor(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "2",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "Instructor account 'new' created",
            response.context.get("message"),
            "instructor confirmation message not given",
        )

    def test_ta(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "3",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "TA account 'new' created",
            response.context.get("message"),
            "ta confirmation message not given",
        )

    def test_inDatabase(self):
        self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertNotEqual(None, AccountUtil.getAccountByUsername("new"))

    def test_noUsername(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "Please fill out all required fields",
            response.context.get("message"),
            "no username",
        )

    def test_noPassword(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "Please fill out all required fields",
            response.context.get("message"),
            "no password",
        )

    def test_usernameTaken(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "user",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "username 'user' is already in use",
            response.context.get("message"),
            "username already taken",
        )

    def test_noNewDuplicate(self):
        self.client.post(
            "/account/create/",
            {
                "username": "user",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            1,
            Account.objects.all().count(),
            "new user created even though duplicate username entered",
        )

    def test_noAuthority(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "Please fill out all required fields",
            response.context.get("message"),
            "no authority",
        )

    def test_outOfRangeAuthority(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "10",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "user type does not exist",
            response.context.get("message"),
            "out of range authority",
        )

    def test_noFirstName(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "",
                "lastname": "Last",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "Please fill out all required fields",
            response.context.get("message"),
            "no first name",
        )

    def test_noLastName(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "",
                "email": "fake@test.com",
            },
        )
        self.assertEqual(
            "Please fill out all required fields",
            response.context.get("message"),
            "no last name",
        )

    def test_noEmail(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "",
            },
        )
        self.assertEqual(
            "Please fill out all required fields",
            response.context.get("message"),
            "no email",
        )

    def test_withAddress(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
                "address": "123 Testing Way",
            },
        )
        self.assertEqual(
            "Administrator account 'new' created",
            response.context.get("message"),
            "confirmation message not given",
        )

    def test_withPhone(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
                "phone": "9876543210",
            },
        )
        self.assertEqual(
            "Administrator account 'new' created",
            response.context.get("message"),
            "confirmation message not given",
        )

    def test_withAll(self):
        response = self.client.post(
            "/account/create/",
            {
                "username": "new",
                "password": "password",
                "authority": "1",
                "firstname": "First",
                "lastname": "Last",
                "email": "fake@test.com",
                "address": "123 Testing Way",
                "phone": "9876543210",
            },
        )
        self.assertEqual(
            "Administrator account 'new' created",
            response.context.get("message"),
            "confirmation message not given",
        )

    def test_invalidEmail(self):
        pass

    def test_invalidPhone(self):
        pass

    def test_addressTooLong(self):
        pass
