from typing import List
from django.contrib.auth import login
from django.test import TestCase, Client
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.contrib.auth.models import Group

from TA_Scheduler.utilities.CourseUtil import CourseUtil

class CreateCourseTest(TestCase):
    TEMPLATE = "/course/create/"
    MESSAGE = "message"
    WARNING = "warning"
    ERROR = "error"

    def setUp(self):
        self.amount = 15
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")
        self.client = Client()

        self.courses = []

        self.password = "password"
        self.admin_account = AccountUtil.getAccountByID(AccountUtil.createAdminAccount("admin", self.password))
        self.instr_account = AccountUtil.getAccountByID(AccountUtil.createInstructorAccount("instructor", self.password))
        self.ta_account = AccountUtil.getAccountByID(AccountUtil.createTAAccount("ta", self.password))

        for i in range(self.amount):
            tas = []
            for j in range(i%5):
                ta_id = AccountUtil.createTAAccount("TA" + str(j+i*10), "password" + str(i))
                ta = AccountUtil.getAccountByID(ta_id)
                tas.append(ta)
            instructor_id = AccountUtil.createInstructorAccount("Instructor" + str(i), "password" + str(i))
            instructor = AccountUtil.getAccountByID(instructor_id)
            self.courses.append(self.form("Course" + str(i), "Description", instructor, tas))


    def test_createDuplicate(self):
        self.client.post(self.TEMPLATE, self.courses[0]["form"])
        resp = self.client.post(self.TEMPLATE, self.courses[0]["form"])
        self.assertEquals("Class already exists with this instructor.", resp.context[self.WARNING], msg="Failed to detect duplicate course.")

    def test_badName(self):
        course = self.form("!@#$%^%", instructor=self.courses[0]["instructor"], tas=self.courses[0]["ta"])
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals("Name can only contain [A-z][0-9]", resp.context[self.WARNING], msg="Failed to detect bad course name.")

    def test_badDescription(self):
        course = self.form(description="!@#$%^&*", instructor=self.courses[0]["instructor"], tas=self.courses[0]["ta"])
        resp = self.client.post(self.TEMPLATE, course["form"])
        self.assertEquals("Description can only contain [A-z][0-9]", resp.context[self.WARNING], msg="Failed to detect bad course name.")




    def form(self, name: str="Course1", description: str="description", instructor: Account=None, tas: List[Account]=None) :
        tas_strs = []
        for ta in tas:
            tas_strs.append(str(ta))
        return {
            "name": name,
            "description": description,
            "instructor": instructor,
            "ta": tas,
            "form" : {
                "name": name,
                "description": description,
                "instructor": str(instructor),
                "ta": tas_strs
            }
        }
