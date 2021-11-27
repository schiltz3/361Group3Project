from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Account(models.Model):
    """
    Represents a row in the Account database.

    Note to teammate:
    Maps one-to-one with Django's build-in User object
    User object has username, password, first_name and last_name fields,
    takes care of password encryption.

    account.id --> id in db
    account.user --> assosiated User object
    account.user.username --> username
    account.user.password --> password
    account.user.first_name --> first name of user
    account.user.last_name --> last name of user
    account.authority --> authority of user (currently 1,2,3)
    """

    # TODO: how should we prepresent authorities?? I'm using this
    # but it looks bad..
    AUTHORITY = (
        (1, 'TA'),
        (2, 'instructor'),
        (3, 'administrator')
    )

    # unique database primary key
    id = models.AutoField(verbose_name="Account ID", primary_key=True)

    # the one-to-one mapping with the built-in User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # authority
    authority = models.PositiveSmallIntegerField(choices=AUTHORITY)


class Course(models.Model):
    """
    Represents a row in the course database.

    id - generated, and is the primary key
    name - name of the course (CompSci 250)
    description - optional description of the course (prereqs, what it's about, etc.)
    instructor - the account of the instructor
    """


    id = models.AutoField("Course ID", primary_key=True)
    name = models.CharField("Course Name" ,max_length=200, blank=False)
    description = models.CharField("Course Description", max_length=5000)

    # SET_NULL --> when an instructor is deleted, set this thing to null
    # ForeignKey is many-to-one relation (an instructor can have many courses)
    instructor = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)