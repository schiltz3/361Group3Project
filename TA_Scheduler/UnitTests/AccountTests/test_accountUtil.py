from django.test import TestCase
from django.contrib.auth.models import Group, User
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.models import Account
from django.core.exceptions import ValidationError


class CreateTaTest(TestCase):
    def setUp(self):
        Group.objects.create(name="ta")

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with no parameters entered"):
            AccountUtil.createTAAccount()

    def test_oneParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with one parameter entered"):
            AccountUtil.createTAAccount("one")

    def test_passwordOnly(self):
        with self.assertRaises(TypeError, msg="fails to raise error with only password entered"):
            AccountUtil.createTAAccount(password="two")

    def test_twoParam(self):
        acct = AccountUtil.createTAAccount("one", "two")
        self.assertEqual(Account.objects.get(id=acct).user.username, "one", msg="account not properly created")

    def test_threeParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.createTAAccount("one", "two", "three")


class CreateInstructorTest(TestCase):
    def setUp(self):
        Group.objects.create(name="instructor")

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with no parameters entered"):
            AccountUtil.createInstructorAccount()

    def test_oneParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with one parameter entered"):
            AccountUtil.createInstructorAccount("one")

    def test_passwordOnly(self):
        with self.assertRaises(TypeError, msg="fails to raise error with only password entered"):
            AccountUtil.createInstructorAccount(password="two")

    def test_twoParam(self):
        acct = AccountUtil.createInstructorAccount("one", "two")
        self.assertEqual(Account.objects.get(id=acct).user.username, "one", msg="account not properly created")

    def test_threeParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.createInstructorAccount("one", "two", "three")


class CreateAdminTest(TestCase):
    def setUp(self):
        Group.objects.create(name="admin")

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with no parameters entered"):
            AccountUtil.createAdminAccount()

    def test_oneParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with one parameter entered"):
            AccountUtil.createAdminAccount("one")

    def test_passwordOnly(self):
        with self.assertRaises(TypeError, msg="fails to raise error with only password entered"):
            AccountUtil.createAdminAccount(password="two")

    def test_twoParam(self):
        acct = AccountUtil.createAdminAccount("one", "two")
        self.assertEqual(Account.objects.get(id=acct).user.username, "one", msg="account not properly created")

    def test_threeParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.createAdminAccount("one", "two", "three")


class GetByIdTest(TestCase):
    def setUp(self):
        Group.objects.create(name="admin")
        self.aID = AccountUtil.createAdminAccount("user", "pass")

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with no parameters entered"):
            AccountUtil.getAccountByID()

    def test_oneParam(self):
        acct = AccountUtil.getAccountByID(self.aID)
        self.assertEqual(acct, Account.objects.get(id=self.aID), msg="account not found")

    def test_twoParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.getAccountByID(1, 2)

    def test_wrongParam(self):
        with self.assertRaises(ValueError, msg="fails to raise error given non-int id"):
            AccountUtil.getAccountByID("one")

    def test_doesNotExist(self):
        acct = AccountUtil.getAccountByID(self.aID+1)
        self.assertEqual(None, acct, msg="account found given non-existent id")


class GetByUsernameTest(TestCase):
    def setUp(self):
        Group.objects.create(name="admin")
        self.aID = AccountUtil.createAdminAccount("user", "pass")

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with no parameters entered"):
            AccountUtil.getAccountByUsername()

    def test_oneParam(self):
        acct = AccountUtil.getAccountByUsername("user")
        self.assertEqual(acct, Account.objects.get(user=User.objects.get(username="user")), msg="account not found")

    def test_twoParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.getAccountByUsername("user", "pass")

    def test_doesNotExist(self):
        acct = AccountUtil.getAccountByUsername("test")
        self.assertEqual(None, acct, msg="account found given non-existent username")


class GetAllTest(TestCase):
    def test_empty(self):
        self.assertEqual(None, AccountUtil.getAllAccounts())

    def test_exists(self):
        Group.objects.create(name="admin")
        AccountUtil.createAdminAccount("test", "test")
        self.assertQuerysetEqual(AccountUtil.getAllAccounts(), Account.objects.all(),
                                 transform=lambda x: x, msg="query sets do not match")

    def test_withParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.getAllAccounts("test")


class GetTAsTest(TestCase):
    def test_empty(self):
        self.assertEqual(None, AccountUtil.getTAs())

    def test_exists(self):
        Group.objects.create(name="ta")
        AccountUtil.createTAAccount("test", "test")
        users = User.objects.filter(groups__name="ta")
        accts = []
        for user in users:
            try:
                acct = Account.objects.get(user=user)
                accts.append(acct)
            except Account.DoesNotExist:
                pass
        self.assertEqual(list(AccountUtil.getTAs()), accts, msg="lists do not match")

    def test_withParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.getTAs("test")


class GetInstructorsTest(TestCase):
    def test_empty(self):
        self.assertEqual(None, AccountUtil.getInstructors())

    def test_exists(self):
        Group.objects.create(name="instructor")
        AccountUtil.createInstructorAccount("test", "test")
        users = User.objects.filter(groups__name="instructor")
        accts = []
        for user in users:
            try:
                acct = Account.objects.get(user=user)
                accts.append(acct)
            except Account.DoesNotExist:
                pass
        self.assertEqual(list(AccountUtil.getInstructors()), accts, msg="lists do not match")

    def test_withParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.getInstructors("test")


class GetByCredentialsTest(TestCase):
    def setUp(self):
        Group.objects.create(name="admin")
        self.aID = AccountUtil.createAdminAccount("user", "pass")

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with no parameters entered"):
            AccountUtil.getAccountByCredentials()

    def test_oneParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with only one parameter"):
            AccountUtil.getAccountByCredentials("user")

    def test_twoParam(self):
        acct = AccountUtil.getAccountByCredentials("user", "pass")
        self.assertEqual(acct, Account.objects.get(user=User.objects.get(username="user")), msg="account not found")

    def test_threeParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.getAccountByCredentials("user", "pass", "extra")

    def test_wrongUsername(self):
        acct = AccountUtil.getAccountByCredentials("wrong", "pass")
        self.assertEqual(None, acct, msg="account found given unused username")

    def test_wrongPassword(self):
        acct = AccountUtil.getAccountByCredentials("user", "wrong")
        self.assertEqual(None, acct, msg="account found given wrong password")


class UpdateInfoTest(TestCase):
    def setUp(self):
        Group.objects.create(name="admin")
        self.aID = AccountUtil.createAdminAccount("one", "two")
        self.user = Account.objects.get(id=self.aID).user

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="error not raised when missing id"):
            AccountUtil.updateAccountInfo()

    def test_idOnly(self):
        self.assertEqual(AccountUtil.updateAccountInfo(self.aID), True, "account not found with used id")

    def test_unusedID(self):
        self.assertEqual(AccountUtil.updateAccountInfo(self.aID+1), False, "account found with unused id")

    def test_invalidID(self):
        with self.assertRaises(ValueError, msg="fails to raise error given invalid id"):
            AccountUtil.updateAccountInfo("wrong")

    def test_invalidEmail(self):
        with self.assertRaises(ValidationError, msg="fails to raise error given invalid email"):
            AccountUtil.updateAccountInfo(self.aID, email="wrong")

    def test_invalidPhone(self):
        with self.assertRaises(ValidationError, msg="fails to raise error given invalid phone number"):
            AccountUtil.updateAccountInfo(self.aID, phone="wrong")

    def test_firstChanged(self):
        AccountUtil.updateAccountInfo(self.aID, first="new")
        self.assertEqual("new", Account.objects.get(id=self.aID).user.first_name)

    def test_lastChanged(self):
        AccountUtil.updateAccountInfo(self.aID, last="new")
        self.assertEqual("new", Account.objects.get(id=self.aID).user.last_name)

    def test_emailChanged(self):
        AccountUtil.updateAccountInfo(self.aID, email="new@test.net")
        self.assertEqual("new@test.net", Account.objects.get(id=self.aID).user.email)

    def test_addressChanged(self):
        AccountUtil.updateAccountInfo(self.aID, address="new")
        self.assertEqual("new", Account.objects.get(id=self.aID).address)

    def test_phoneChanged(self):
        AccountUtil.updateAccountInfo(self.aID, phone=9876543210)
        self.assertEqual(9876543210, Account.objects.get(id=self.aID).phone)


class GetUserGroupTest(TestCase):
    def test_admin(self):
        Group.objects.create(name="admin")
        aID = AccountUtil.createAdminAccount("one", "two")
        user = AccountUtil.getAccountByID(aID).user
        self.assertEqual("admin", AccountUtil.getUserGroup(user))

    def test_instructor(self):
        Group.objects.create(name="instructor")
        aID = AccountUtil.createInstructorAccount("one", "two")
        user = AccountUtil.getAccountByID(aID).user
        self.assertEqual("instructor", AccountUtil.getUserGroup(user))

    def test_ta(self):
        Group.objects.create(name="ta")
        aID = AccountUtil.createTAAccount("one", "two")
        user = AccountUtil.getAccountByID(aID).user
        self.assertEqual("ta", AccountUtil.getUserGroup(user))

    def test_nonexistent(self):
        # defaults to ta
        user = User.objects.create()
        self.assertEqual("ta", AccountUtil.getUserGroup(user))

    def test_noParam(self):
        with self.assertRaises(TypeError, msg="fails to raise error with no parameters"):
            AccountUtil.getUserGroup()

    def test_twoParam(self):
        Group.objects.create(name="admin")
        aID = AccountUtil.createAdminAccount("one", "two")
        user = AccountUtil.getAccountByID(aID).user
        with self.assertRaises(TypeError, msg="fails to raise error with too many parameters"):
            AccountUtil.getUserGroup(user, "extra")
