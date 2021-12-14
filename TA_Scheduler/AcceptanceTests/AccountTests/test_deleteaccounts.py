from django.test import TestCase, Client
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group


class NewAccountTest(TestCase):
    def setUp(self):
        self.client = Client()
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        self.accountID = AccountUtil.createAdminAccount(username="user", password="pass")
        self.account = AccountUtil.getAccountByID(self.accountID)

    def test_success(self):
        self.client.post("/account/delete/", {"account": self.accountID})
        self.assertEqual(None, AccountUtil.getAccountByID(self.accountID), "Account not deleted")

    def test_successMessage(self):
        response = self.client.post("/account/delete/", {"account": self.accountID})
        self.assertEqual("Account deleted", response.context.get("message"), "confirmation message not given")

    def test_noSelection(self):
        self.client.post("/account/delete/")
        self.assertEqual(self.account, AccountUtil.getAccountByID(self.accountID),
                         "Account should not have been deleted")

    def test_noSelectionMessage(self):
        response = self.client.post("/account/delete/")
        self.assertEqual("Please fill out all required fields", response.context.get("message"),
                         "no selection message not given")

    def test_invalidSelection(self):
        self.client.post("/account/delete/", {"account": self.accountID})
        accountList = AccountUtil.getAllAccounts()
        self.client.post("/account/delete/", {"account": self.accountID})
        self.assertEqual(None, AccountUtil.getAllAccounts(),
                                 msg="invalid account should not change account list")

    def test_invalidSelectionMessage(self):
        self.client.post("/account/delete/", {"account": self.accountID})
        response = self.client.post("/account/delete/", {"account": self.accountID})
        self.assertEqual("Invalid account selection", response.context.get("message"),
                         "invalid selection message not given")
