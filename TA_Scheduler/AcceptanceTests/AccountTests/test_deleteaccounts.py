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

    def test_success(self):
        pass

    def test_noSelection(self):
        pass

    ''' create acceptance criterion or get rid of? '''
    def test_invalidSelection(self):
        pass
