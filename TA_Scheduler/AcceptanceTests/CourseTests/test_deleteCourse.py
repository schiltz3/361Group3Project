from typing import List
from django.contrib.auth import login
from django.test import TestCase, Client
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group

from TA_Scheduler.utilities.CourseUtil import CourseUtil


class DeleteCourseTest(TestCase):
    TEMPLATE = "/course/delete/"
    MESSAGE = "message"
    WARNING = "warning"
    ERROR = "error"

    def setUp(self):
        self.amount = 15
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        self.client = Client()

        self.password = "password"
        self.admin_account = AccountUtil.getAccountByID(
            AccountUtil.createAdminAccount("admin", self.password)
        )
        self.instr_account = AccountUtil.getAccountByID(
            AccountUtil.createInstructorAccount("instructor", self.password)
        )
        self.ta_account = AccountUtil.getAccountByID(
            AccountUtil.createTAAccount("ta", self.password)
        )

        self.courses = []
        self.courseNames = []

        for i in range(self.amount):
            course = CourseUtil.getCourseByID(
                CourseUtil.createCourse(
                    name="Course" + str(i), description="Description"
                )
            )
            self.courses.append(course)
            self.courseNames.append(course.name)

    def test_deleteCourse(self):
        courseName = self.courseNames[0]
        self.client.post(self.TEMPLATE, {"courses": [courseName]})
        self.assertIsNone(
            CourseUtil.getCourseByName(courseName), msg="Failed to delete a course."
        )

    def test_deleteMany(self):
        limit = self.amount // 2
        if limit > 0:
            self.client.post(self.TEMPLATE, {"courses": self.courseNames[0:limit]})

            for i in range(limit):
                self.assertIsNone(
                    CourseUtil.getCourseByName(self.courseNames[i]),
                    msg="Failed to delete a selection of courses.",
                )

    def test_deleteAll(self):
        self.client.post(self.TEMPLATE, {"courses": self.courseNames})
        self.assertIsNone(
            CourseUtil.getAllCourses(), msg="Failed to delete all courses"
        )

    def test_keepNonDeleted(self):
        index = 0
        courseName = self.courseNames[index]
        self.client.post(self.TEMPLATE, {"courses": [courseName]})

        for name in self.courseNames:
            if name != courseName:
                self.assertIsNotNone(
                    CourseUtil.getCourseByName(name),
                    msg="Non-deleted course is missing from database.",
                )

    def test_failToDelete(self):
        course = "Yay2021"
        resp = self.client.post(self.TEMPLATE, {"courses": [course]})
        self.assertEquals(
            "Failed to delete: " + course,
            resp.context[self.ERROR],
            msg="Failed to detect a fake course deletion.",
        )

    def test_emptySelection(self):
        resp = self.client.post(self.TEMPLATE, {"courses": []})
        self.assertEquals(
            "No courses were selected.",
            resp.context[self.WARNING],
            msg="Failed to warn about no courses being selected.",
        )

    def test_adminCanAccess(self):
        self.client.login(
            username=self.admin_account.user.username, password=self.password
        )
        resp = self.client.get(self.TEMPLATE)
        self.assertEquals(resp.status_code, 200)

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
