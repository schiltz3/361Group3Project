import collections
from typing import List

from django.contrib.auth.models import Group
from django.test import TestCase, Client

from TA_Scheduler.models import Account, Course
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil


class EditCourseTest(TestCase):
    TEMPLATE = "/course/edit/"
    MESSAGE = "message"
    WARNING = "warning"
    ERROR = "error"

    def setUp(self):
        self.amount = 15
        self.password = "password"
        self.courses = []

        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        self.client = Client()

        self.admin_account = AccountUtil.getAccountByID(
            AccountUtil.createAdminAccount("admin", self.password)
        )
        self.instr_account = AccountUtil.getAccountByID(
            AccountUtil.createInstructorAccount("instructor", self.password)
        )
        self.ta_account = AccountUtil.getAccountByID(
            AccountUtil.createTAAccount("ta", self.password)
        )

        for i in range(self.amount):
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
                CourseUtil.getCourseByID(
                    CourseUtil.createCourse(
                        "Course" + str(i), "Description", instructor, tas
                    )
                )
            )

    def test_adminCanAccess(self):
        self.client.login(
            username=self.admin_account.user.username, password=self.password
        )
        resp = self.client.get(self.TEMPLATE)
        self.assertEqual(
            None, resp.context.get(self.MESSAGE), msg="Admin failed to access page."
        )

    def test_redirectInstructor(self):
        self.client.login(
            username=self.instr_account.user.username, password=self.password
        )
        resp = self.client.get(self.TEMPLATE)
        self.assertRedirects(resp, "/dashboard/instructor/")

    def test_redirectTA(self):
        self.client.login(
            username=self.ta_account.user.username, password=self.password
        )
        resp = self.client.get(self.TEMPLATE)
        self.assertRedirects(resp, "/dashboard/ta/")

    def test_allCoursesReturned(self):
        self.client.login(
            username=self.admin_account.user.username, password=self.password
        )
        resp = self.client.get(self.TEMPLATE)
        self.assertEquals(
            collections.Counter(resp.context.get("courses")),
            collections.Counter(self.courses),
            msg="Did not get all courses",
        )

    def test_noneCourse(self):
        self.client.login(
            username=self.admin_account.user.username, password=self.password
        )
        ctx = {"courses": self.courses, "course": "None"}
        resp = self.client.post(self.TEMPLATE)
        self.assertEquals(
            "Select a course",
            resp.context.get(self.WARNING),
            msg="Failed to detect no course selected",
        )
