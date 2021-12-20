""" Unit tests for methods associated with edit course
"""
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.test import TestCase, Client

from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.views.course.edit import EditCourse


class CreateCourseTest(TestCase):
    TEMPLATE = "/course/edit/"
    MESSAGE = "message"
    WARNING = "warning"
    ERROR = "error"

    def setUp(self):
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        self.client = Client()

        tas = []
        instructor = AccountUtil.getAccountByID(
            AccountUtil.createInstructorAccount("Instructor", "password")
        )

        for i in range(4):
            ta_id = AccountUtil.createTAAccount("TA" + str(i), "password" + str(i))
            ta = AccountUtil.getAccountByID(ta_id)
            tas.append(ta)

        self.course = EditCourse()
        self.request = HttpRequest()
        self.request.user = instructor.user

    def testNoVars(self):
        with self.assertRaises(TypeError, msg="Not catching empty args"):
            self.course.validateCourseInput()

    def testAllVars(self):
        ret = self.course.validateCourseInput(
            self.request,
            name="Name",
            instructor="Instructor",
            description="Description",
            tas=["Ta1"],
        )
        self.assertTrue(ret, msg="Did not return true")

    def testNoName(self):
        ret = self.course.validateCourseInput(self.request, name=None)
        self.assertTrue(
            isinstance(ret, HttpResponse), msg="Did not return error message"
        )

    def testNoDescription(self):
        ret = self.course.validateCourseInput(
            self.request, name="Name", instructor="Instructor"
        )
        self.assertTrue(
            isinstance(ret, HttpResponse), msg="Did not return error message"
        )

    def testNoInstructor(self):
        ret = self.course.validateCourseInput(
            self.request, name="Name", description="Description"
        )
        self.assertTrue(ret, msg="Did not return true")

    def testNoTas(self):
        ret = self.course.validateCourseInput(
            self.request,
            name="Name",
            description="Description",
            instructor="Instructor",
        )
        self.assertTrue(ret, msg="Did not return true")
