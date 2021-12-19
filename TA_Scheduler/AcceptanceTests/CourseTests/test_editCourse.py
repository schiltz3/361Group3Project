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

            # self.courses.append(
            #    self.form("Course" + str(i), "Description", instructor, tas)
            # )

    def test_print(self):
        print("All local courses")
        print(self.courses)

        print("All db courses:")
        courses = CourseUtil.getAllCourses()
        for course in courses:
            print(course)

    def test_adminCanAccess(self):
        self.client.login(
            username=self.admin_account.user.username, password=self.password
        )
        resp = self.client.get(self.TEMPLATE)
        self.assertEqual(
            "", resp.context[self.MESSAGE], msg="Admin failed to access page."
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
        print(ctx)
        resp = self.client.post(self.TEMPLATE)
        print(resp)
        self.assertEquals(
            "Please select course",
            resp.context.get(self.WARNING),
            msg="Failed to detect no course selected",
        )

    @staticmethod
    def form(
        courses: List[Course],
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
            "courses": [course.name for course in courses],
            "name": name,
            "description": description,
            "instructor": instructor,
            "ta": tas,
            "form": {
                "courses": [course.name for course in courses],
                "name": name,
                "description": description,
                "instructor": str(instructor),
                "ta": tas_strings,
            },
        }
