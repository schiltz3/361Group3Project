from typing import List
from django.test import TestCase, Client
from django.contrib.auth.models import Group
from TA_Scheduler.models import Account, Course
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil


class EditCourseTest(TestCase):

    def setUp(self):
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        self.client = Client()

        self.courses = []

        self.password = "password"
        self.numberOfUniqueAccounts = 15

        self.admin_account = AccountUtil.getAccountByID(
            AccountUtil.createAdminAccount("admin", self.password)
        )
        self.instructor_account = AccountUtil.getAccountByID(
            AccountUtil.createInstructorAccount("instructor", self.password)
        )
        self.ta_account = AccountUtil.getAccountByID(
            AccountUtil.createTAAccount("ta", self.password)
        )

        for i in range(self.numberOfUniqueAccounts):
            tas = []
            for j in range(i % 5):
                ta_id = AccountUtil.createTAAccount(
                    "TA" + str(j + i * 10), "password" + str(i)
                )
                ta = AccountUtil.getAccountByID(ta_id)
                tas.append(ta)
            instructor_id = AccountUtil.createInstructorAccount(
                "Instructor" + str(i), "password" + str(i)
            )
            instructor = AccountUtil.getAccountByID(instructor_id)
            self.courses.append(
                self.form("Course" + str(i), "Description", instructor, tas)
            )

    @staticmethod
    def form(
            name: str = "",
            description: str = "",
            instructor: Account = None,
            tas: List[Account] = None,
    ):
        tas_strings = []
        if tas:
            for ta in tas:
                tas_strings.append(str(ta))
        return {
            "name": name,
            "description": description,
            "instructor": instructor,
            "ta": tas,
            "form": {
                "name": name,
                "description": description,
                "instructor": str(instructor),
                "ta": tas_strings,
            },
        }
