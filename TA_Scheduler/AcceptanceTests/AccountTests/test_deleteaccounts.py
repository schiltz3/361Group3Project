from django.test import TestCase, Client
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group


class NewAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        self.id = AccountUtil.createAdminAccount(username="user", password="pass")
        self.user = AccountUtil.getAccountByID(id)

    def test_success(self):
        self.client.post("/account/delete/", {"account": self.user+""})
        self.assertEqual(None, AccountUtil.getAccountByID(id), "Account not deleted")

    def test_successMessage(self):
        response = self.client.post("/account/delete/", {"account": self.user+""})
        self.assertEqual("Account deleted", response.context.get("message"), "confirmation message not given")

    def test_noSelection(self):
        self.client.post("/account/delete/")
        self.assertEqual(self.user, AccountUtil.getAccountByID(self.id), "Account should not have been deleted")

    def test_noSelectionMessage(self):
        response = self.client.post("/account/delete/")
        self.assertEqual("Please fill out all required fields", response.context.get("message"),
                         "no selection message not given")

    def test_invalidSelection(self):
        self.client.post("/account/delete/", {"account": self.user+""})
        accountList = AccountUtil.getAllAccounts()
        self.client.post("/account/delete/", {"account": self.user + ""})
        self.assertEqual(accountList, AccountUtil.getAllAccounts(), "invalid account should not change account list")

    def test_invalidSelectionMessage(self):
        self.client.post("/account/delete/", {"account": self.user+""})
        response = self.client.post("/account/delete/", {"account": self.user + ""})
        self.assertEqual("Invalid account selection", response.context.get("message"),
                         "invalid selection message not given")
