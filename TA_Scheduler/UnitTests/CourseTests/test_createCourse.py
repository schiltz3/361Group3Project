from typing import List
from django.test import TestCase, Client
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group


class CreateCourseTest(TestCase):
    TEMPLATE = "/course/create/"
    MESSAGE = "message"
    WARNING = "warning"
    ERROR = "error"

    def setUp(self):
        self.client = Client()

        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")

        tas = []
        instructor = AccountUtil.getAccountByID(
            AccountUtil.createInstructorAccount("Instructor", "password")
        )

        for i in range(4):
            ta_id = AccountUtil.createTAAccount("TA" + str(i), "password" + str(i))
            ta = AccountUtil.getAccountByID(ta_id)
            tas.append(ta)

        self.course = self.form(instructor=instructor, tas=tas)

    def test_createDuplicate(self):
        self.client.post(self.TEMPLATE, self.course["form"])
        resp = self.client.post(self.TEMPLATE, self.course["form"])
        self.assertEquals(
            "Class already exists with this instructor.",
            resp.context[self.WARNING],
            msg="Failed to detect duplicate course.",
        )

    def test_badName(self):
        course = self.form(
            name="!@#$%^%", instructor=self.course["instructor"], tas=self.course["ta"]
        )
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "Name can only contain [A-z][0-9]",
            resp.context[self.WARNING],
            msg="Failed to detect bad course name.",
        )

    def test_blankName(self):
        course = self.form(
            name="", instructor=self.course["instructor"], tas=self.course["ta"]
        )
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "Name must not be blank",
            resp.context[self.WARNING],
            msg="Failed to detect bad course name.",
        )

    def test_badDescription(self):
        course = self.form(
            description="!@#$%^&*",
            instructor=self.course["instructor"],
            tas=self.course["ta"],
        )
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "Description can only contain [A-z][0-9]",
            resp.context[self.WARNING],
            msg="Failed to detect bad course name.",
        )

    def test_blankDescription(self):
        course = self.form(
            description="", instructor=self.course["instructor"], tas=self.course["ta"]
        )
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "Description must not be blank.",
            resp.context[self.WARNING],
            msg="Failed to detect bad course name.",
        )

    def test_instructorNotFound(self):
        course = self.form(instructor="Mario")
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "Instructor could not be found.",
            resp.context[self.ERROR],
            msg="Failed to detect nonexistent instructor.",
        )

    def test_instructorIsNone(self):
        course = self.form()
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "Course created.",
            resp.context[self.MESSAGE],
            msg="Failed to create class.",
        )

    def test_TANotFound(self):
        ta = "turtle"
        course = self.form(instructor=self.course["instructor"], tas=[ta])
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "TA '" + ta + "' does not exist.",
            resp.context[self.ERROR],
            msg="Failed to detect nonexistent TA.",
        )

    def test_courseSuccess(self):
        course = self.form(instructor=self.course["instructor"], tas=self.course["ta"])
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals(
            "Course created.",
            resp.context[self.MESSAGE],
            msg="Failed to detect successful course creation.",
        )

    def form(
            self,
            name: str = "Course1",
            description: str = "description",
            instructor: Account = None,
            tas: List[Account] = None,
    ):
        tas_strs = []
        if tas:
            for ta in tas:
                tas_strs.append(str(ta))
        return {
            "name": name,
            "description": description,
            "instructor": instructor,
            "ta": tas,
            "form": {
                "name": name,
                "description": description,
                "instructor": str(instructor) if instructor else "",
                "ta": tas_strs,
            },
        }
