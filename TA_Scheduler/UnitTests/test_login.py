from django.test import TestCase, Client
from django.shortcuts import reverse
from TA_Scheduler.models import Account


class TestLogin(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.session = self.client.session

    def test_get_user_and_validate(self):

    def test_validate_input(self):
        
 # -----------------------------------------       
    def test_blankLogin(self):
        resp = self.client.post("/login/", {"username" : "", "password" : ""}, follow=True)
        self.assertEqual("Fields are blank.", resp.context["message"], msg="failed to detect blank fields.")
        
    def test_successfulLogin(self):
        account = AccountUtil.getAllAccounts()
        if account:
            resp = self.client.post("/login/", {"username" : account[0].username, "password" : account[0].password}, follow=True)
            self.assertEqual("Login successful.", resp.context["message"], msg="failed to detect successful login")



