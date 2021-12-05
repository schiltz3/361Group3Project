from django.test import TestCase, Client
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group


class MyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="instructor")
        Group.objects.create(name="TA")
        Group.objects.create(name="admin")
        AccountUtil.createAdminAccount(username="admin", password="pass123")
        self.user1 = AccountUtil.getAccountByUsername("admin")

    def test_RedirectStatusCode(self):
        resp = self.client.post(
            "/", {"username": "admin", "password": "pass123"}, follow=True
        )
        self.assertEqual(resp.status_code, 200)

    def test_InvalidUsername(self):
        resp = self.client.post(
            "/", {"username": "notValid", "password": "pass123"}, follow=True
        )
        self.assertFalse(self.user1.user.username == resp.context["username"])

    def test_InvalidPass(self):
        resp = self.client.post(
            "/", {"username": "admin", "password": "password"}, follow=True
        )
        self.assertFalse(self.user1.user.check_password(resp.context["password"]))
