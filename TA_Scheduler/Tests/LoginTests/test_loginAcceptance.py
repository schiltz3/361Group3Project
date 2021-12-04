from django.test import TestCase, Client
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group

# Create your tests here.


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="instructor")
        Group.objects.create(name="TA")
        Group.objects.create(name="admin")
        AccountUtil.createAdminAccount(username="admin", password="pass123")
        AccountUtil.createInstructorAccount(username="instructor", password="pass123word")
        AccountUtil.createTAAccount(username="ta", password="password")

    def test_RedirectAdmin(self):
        resp = self.client.post("/", {"username": "admin", "password": "pass123"},
                                follow=True)
        self.assertRedirects(resp, "/dashboard/admin/")

    def test_RedirectInstructor(self):
        resp = self.client.post("/", {"username": "instructor", "password": "pass123word"},
                                follow=True)
        self.assertRedirects(resp, "/dashboard/instructor/")

    def test_RedirectTA(self):
        resp = self.client.post("/", {"username": "ta", "password": "password"},
                                follow=True)
        self.assertRedirects(resp, "/dashboard/ta/")

    def test_InvalidUser(self):
        resp = self.client.post("/", {"username": "someone", "password": "abc123"},
                                follow=True)
        self.assertEqual("Invalid username", resp.context["error"], "Login failed, user not found")

    def test_badPassword(self):
        resp = self.client.post("/", {"username": "admin", "password": "abc123"},
                                follow=True)
        self.assertEqual("Invalid password", resp.context["error"], "Failed login, password incorrect")

    def test_blankPassword(self):
        resp = self.client.post("/", {"username": "admin", "password": ""}, follow=True)
        self.assertEqual("Invalid password", resp.context["error"], "Must input password")

