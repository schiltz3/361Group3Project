from typing import Iterable, Optional, Union
from django.contrib.auth.models import Group, User
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate

from TA_Scheduler.models import Account


# Note to teammate:
# This is a utility class to access the Account database.
# Use the methods below to get accounts:

# createAccount(username, password, authority) --> returns id in database or error
# getAccountByID(id)
# getAllAccounts()
# getInstructors()
class AccountUtil:
    @staticmethod
    def createTAAccount(username: str, password: str) -> Union[int, TypeError]:
        if username == "" or password == "":
            raise TypeError("Username, password, and authority cannot be empty.")

        user = User.objects.create_user(username=username, password=password)

        ta_group = Group.objects.get(name="ta")
        ta_group.user_set.add(user)

        account = Account.objects.create(user=user)
        return account.id

    @staticmethod
    def createInstructorAccount(username: str, password: str) -> Union[int, TypeError]:
        if username == "" or password == "":
            raise TypeError("Username, password, and authority cannot be empty.")

        user = User.objects.create_user(username=username, password=password)

        instructor_group = Group.objects.get(name="instructor")
        instructor_group.user_set.add(user)

        account = Account.objects.create(user=user)
        return account.id

    @staticmethod
    def createAdminAccount(username: str, password: str) -> Union[int, TypeError]:
        if username == "" or password == "":
            raise TypeError("Username, password, and authority cannot be empty.")

        user = User.objects.create_user(username=username, password=password)

        admin_group = Group.objects.get(name="admin")
        admin_group.user_set.add(user)

        account = Account.objects.create(user=user)
        return account.id

    @staticmethod
    def getAccountByID(id: int) -> Optional[Account]:
        try:
            account = Account.objects.get(id=id)
            return account
        except Account.DoesNotExist:
            return None

    @staticmethod
    def getAccountByUsername(username: str) -> Optional[Account]:
        try:
            user = User.objects.get(username=username)
            account = Account.objects.get(user=user)
            return account

        except User.DoesNotExist:
            return None

        except Account.DoesNotExist:
            return None

    @staticmethod
    def getAllAccounts() -> Optional[Iterable[Account]]:
        set: QuerySet = Account.objects.all()
        return set if set.exists() else None

    @staticmethod
    def getTAs() -> Optional[Iterable[Account]]:
        set: QuerySet = User.objects.filter(groups__name="ta")
        result = []
        try:
            for user in set:
                result.append(Account.objects.get(user=user.id))
        except Account.DoesNotExist:
            return None

        return result if result else None

    @staticmethod
    def getInstructors() -> Optional[Iterable[Account]]:
        set: QuerySet = User.objects.filter(groups__name="instructor")
        result = []
        try:
            for user in set:
                result.append(Account.objects.get(user=user.id))

        except Account.DoesNotExist:
            return None

        return result if result else None

    @staticmethod
    def getAccountByCredentials(username: str, password: str) -> Optional[Account]:
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                account = Account.objects.get(user=user.id)
                return account

        except User.DoesNotExist:
            return None

        except Account.DoesNotExist:
            return None

        except IndexError:
            return None

        return None

    @staticmethod
    def getAccountByUsername(username: str) -> Optional[Account]:
        try:
            user = User.objects.filter(username=username)[0]
            account = Account.objects.filter(user=user.id)[0]
            return account

        except IndexError:
            return None

        except User.DoesNotExist:
            return None

        except Account.DoesNotExist:
            return None
        except IndexError:
            return None

    def updateAccountInfo(id: int = None, first: str = None, last: str = None, email: str = None,
                          address: str = None, phone: int = None) -> [bool]:
        if id is None:
            raise TypeError("must enter an id number")

        if AccountUtil.getAccountByID(id) is not None:
            account = AccountUtil.getAccountByID(id)
            if first is not None:
                account.user.first_name = first
            if last is not None:
                account.user.last_name = last
            if email is not None:
                account.user.email = email
            if address is not None:
                account.address = address
            if phone is not None:
                account.phone = phone
            account.save()
            return True
        else:
            return False
