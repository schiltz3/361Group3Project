from typing import List
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
        Group.objects.create(name="TA")
        Group.objects.create(name="admin")
        self.client = Client()

        self.courses = []

        for i in range(self.amount):
            tas = []
            for j in range(i%5):
                ta_id = AccountUtil.createTAAccount("TA" + str(j+i*10), "password" + str(i))
                ta = AccountUtil.getAccountByID(ta_id)
                tas.append(ta)
            instructor_id = AccountUtil.createInstructorAccount("Instructor" + str(i), "password" + str(i))
            instructor = AccountUtil.getAccountByID(instructor_id)
            self.courses.append(self.form("Course" + str(i), "Description", instructor, tas))



    def test_createCourse(self):
        course = self.courses[0]
        self.client.post(
            self.TEMPLATE, course["form"]
        )
        result = CourseUtil.getCourseByName(course["name"])

        self.assertIsNotNone(result, msg="Failed to store created course in database.")
        self.assertEquals(result.description, course["description"], msg="Failed to store correct description in database.")
        self.assertEquals(result.instructor, course["instructor"], msg="Failed to store correct instructor in database.")
        self.assertEquals(list(result.tas.all()), course["ta"], msg="Failed to store correct TAs in database.")

    def test_createCourseMany(self):
        for i in range(self.amount):
            course = self.courses[i]
            self.client.post(
                self.TEMPLATE, course["form"]
            )

            result = CourseUtil.getCourseByName(course["name"])
            self.assertIsNotNone(result, msg="Failed to store created course in database.")
            self.assertEquals(result.description, course["description"], msg="Failed to store correct description in database.")
            self.assertEquals(result.instructor, course["instructor"], msg="Failed to store correct instructor in database.")
            self.assertEquals(list(result.tas.all()), course["ta"], msg="Failed to store correct TAs in database.")

    


        
        


        





    def form(self, name: str, description: str, instructor: Account, tas: List[Account]) :
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
