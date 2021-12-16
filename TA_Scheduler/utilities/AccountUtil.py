from typing import Iterable, Optional, Union
from django.contrib.auth.models import Group, User
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate

from TA_Scheduler.models import Account


class AccountUtil:
    @staticmethod
    def createTAAccount(username: str, password: str) -> Union[int, TypeError]:
        """Create an account in the TA group.

        :param username: The username of the account to create
        :param password: The password of the account to create
        :return: ID of the account if it was successfully created,
            TypeError if username or password are blank
        :pre: Username and password must not be blank
        :post: None
        """
        if username == "" or password == "":
            raise TypeError("Username, password, and authority cannot be empty.")

        user = User.objects.create_user(username=username, password=password)

        ta_group = Group.objects.get(name="ta")
        ta_group.user_set.add(user)

        account = Account.objects.create(user=user)
        return account.id

    @staticmethod
    def createInstructorAccount(username: str, password: str) -> Union[int, TypeError]:
        """Create an account in the Instructor group.

        :param username: The username of the account to create
        :param password: The password of the account to create
        :return: ID of the account if it was successfully created,
            TypeError if username or password are blank
        :pre: Username and password must not be blank
        :post: None
        """
        if username == "" or password == "":
            raise TypeError("Username, password, and authority cannot be empty.")

        user = User.objects.create_user(username=username, password=password)

        instructor_group = Group.objects.get(name="instructor")
        instructor_group.user_set.add(user)

        account = Account.objects.create(user=user)
        return account.id

    @staticmethod
    def createAdminAccount(username: str, password: str) -> Union[int, TypeError]:
        """Create an account in the Admin group.

        :param username: The username of the account to create
        :param password: The password of the account to create
        :return: ID of the account if it was successfully created,
            TypeError if username or password are blank
        :pre: Username and password must not be blank
        :post: None
        """
        if username == "" or password == "":
            raise TypeError("Username, password, and authority cannot be empty.")

        user = User.objects.create_user(username=username, password=password)

        admin_group = Group.objects.get(name="admin")
        admin_group.user_set.add(user)

        account = Account.objects.create(user=user)
        return account.id

    @staticmethod
    def getAccountByID(id: int) -> Optional[Account]:
        """Looks in the Account database for an account that matches the argument ID.

        :param id: The id to look for in the Account database
        :return: If successful, an account with an ID that matches the
            argument, None otherwise
        :pre: None
        :post: None
        """
        try:
            account = Account.objects.get(id=id)
            return account
        except Account.DoesNotExist:
            return None

    @staticmethod
    def getAccountByUsername(username: str) -> Optional[Account]:
        """Looks in the Account database for an account that matches the argument username.

        :param username: The username to look for in the Account database
        :return: If successful, an account with a username that matches the
            argument, None otherwise
        :pre: None
        :post: None
        """
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

    @staticmethod
    def getAllAccounts() -> Optional[Iterable[Account]]:
        """Returns all of the accounts that are stored in the Account database.
        :return: a list of all existing accounts, or
            None if there are none
        :pre: None
        :post: None
        """
        set: QuerySet = Account.objects.all()
        return set if set.exists() else None

    @staticmethod
    def getTAs() -> Optional[Iterable[Account]]:
        """Returns all of the accounts in the TA group that are stored in the Account database.

        :return: a list of all existing TA accounts, or None if
            there are none.
        :pre: None
        :post: None
        """
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
        """Returns all of the accounts in the Instructor group that are stored in the Account database.

        :return: a list of all existing Instructor accounts, or None if
            there are none.
        :pre: None
        :post: None
        """
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
        """Returns an account that matches the argument credentials.

        :param username: the username to find in the Account database
        :param password: the password to find in the Account database
        :return: if found, and account with a username and password
            that match the arguments, None otherwise
        """
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

    def updateAccountInfo(
        id: int = None,
        first: str = None,
        last: str = None,
        email: str = None,
        address: str = None,
        phone: int = None,
    ):
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

    def getUserGroup(user: User):
        if user.groups.filter(name="admin").exists():
            group = "admin"
        elif user.groups.filter(name="instructor").exists():
            group = "instructor"
        else:
            group = "ta"
        return group
