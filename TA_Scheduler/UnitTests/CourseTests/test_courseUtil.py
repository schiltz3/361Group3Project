from typing import List
from django.test import TestCase
from django.contrib.auth.models import Group
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil
from TA_Scheduler.models import Account, Course

class SetUp:
    courseName: str = "Course1"
    description: str = "description"
    instructor: Account
    tas: List[Account] = []
    courseNames: List[str] = []

    def __init__(self):
        Group.objects.create(name="instructor")
        Group.objects.create(name="ta")
        Group.objects.create(name="admin")

        self.instructor = AccountUtil.getAccountByID(
            AccountUtil.createInstructorAccount("Instructor", "password")
        )

        self.tas = []

        for i in range(4):
            ta_id = AccountUtil.createTAAccount("TA" + str(i), "password" + str(i))
            ta = AccountUtil.getAccountByID(ta_id)
            self.tas.append(ta)

    def matches(self, course: Course, courseName: str=courseName, description: str=description, noneInstructor = False, noneTAs: bool = False):
        if course.name != courseName:
            return False

        if course.description != description:
            return False

        if (not(noneInstructor and course.instructor == None or
            not noneInstructor and course.instructor == self.instructor )):
            return False

        if (not(noneTAs and list(course.tas.all()) == None or
            not noneTAs and list(course.tas.all()) == self.tas)):
            return False

        return True



    def setManyCourseNames(self, amount: int):
        self.courseNames = []
        for i in range(amount):
            self.courseNames.append("Course" + str(i))

class CreateCourseUtilTest(TestCase):

    def setUp(self):
        self.util = SetUp()

    def test_createCourse(self):
        index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, self.util.tas)
        self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course to Course database")

    def test_emptyName(self):
        with self.assertRaises(TypeError, msg="Failed to raise type error when Course name is blank"):
            CourseUtil.createCourse("", self.util.description, self.util.instructor, self.util.tas)

    def test_noneInstructor(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, None, self.util.tas)
            self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course with None instructor to Course database")
        except Exception as e:
            self.fail(str(e) + " exception was thrown when trying to create a course without instructor.")

    def test_noneTAs(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, None)
            self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course with None TAs to Course database")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when trying to create a course with TAs set to None.")

    def test_emptyTAs(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, [])
            self.assertEquals(len(Course.objects.filter(id=index)), 1, msg="Failed to add created course with empty TAs to Course database")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when trying to create a course with TAs set to empty list [].")

    def test_accurateFields(self):
        try:
            index = CourseUtil.createCourse(self.util.courseName, self.util.description, self.util.instructor, self.util.tas)
            course = Course.objects.filter(id=index)[0]
            self.assertTrue(self.util.matches(course), msg="The fields of the created course do not match the arguments provided during creation")

        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when trying to create and get a course from the Course database")


class GetCourseByIDTest(TestCase):

    def setUp(self):
        self.util = SetUp()

    def test_getCourseByID(self):
        try:
            course = Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor)
            self.assertIsNotNone(CourseUtil.getCourseByID(course.id), msg="Failed to find an existing course with given ID")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when creating and trying to get a course by its ID")

    def test_nonexistentID(self):
        try:
            self.assertIsNone(CourseUtil.getCourseByID(1), msg="Returned a course that was never added.")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown when getting a nonexistent course by ID, should return None")

    def test_idIsNotNumber(self):
        with self.assertRaises(Exception, msg="Did not raise exception when the argument ID was not a number"):
            CourseUtil.getCourseByID("test")

    def test_accurateFields(self):
        try:
            course = Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor)
            course.tas.set(self.util.tas)
            subject = CourseUtil.getCourseByID(course.id)
            self.assertTrue(self.util.matches(subject), msg="The fields of the created course do not match the arguments provided during creation")

        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to create and get a course by ID")

class GetAllCoursesTest(TestCase):
    def setUp(self):
        self.amount = 15
        self.util = SetUp()
        self.util.setManyCourseNames(self.amount)

    def test_getAllCourses(self):
        try:
            for i in range(self.amount):
                Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor).tas.set(self.util.tas)
            courses = CourseUtil.getAllCourses()
            self.assertEquals(len(courses), self.amount, msg="Failed to retrieve all courses from database")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to retrieve all courses from database")

    def test_emptyDatabase(self):
        try:
            courses = CourseUtil.getAllCourses()
            self.assertIsNone(courses, msg="Failed to get None courses when Course database is empty")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to retrieve all courses from database")

    def test_accurateFields(self):
        try:
            for i in range(self.amount):
                Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor).tas.set(self.util.tas)

            courses = CourseUtil.getAllCourses()
            
            for i in range(self.amount):
                subject = courses[i]
                self.assertTrue(self.util.matches(subject, courseName=courses[i].name), msg="The fields of the created course do not match the arguments provided during creation")

        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to retrieve all courses from database")

class GetCourseByNameTest(TestCase):
    def setUp(self):
        self.util = SetUp()

    def test_getCourseByName(self):
        try:
            Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor)
            self.assertIsNotNone(CourseUtil.getCourseByName(self.util.courseName), msg="Could not retrieve existing course by name from database")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to retrieve a course by name from database")

    def test_nonexistentCourse(self):
        try:
            self.assertIsNone(CourseUtil.getCourseByName("course"), msg="Nonexistent course was returned as not None")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to retrieve a course by name from database")

class DeleteCourseByNameTest(TestCase):
    def setUp(self):
        self.util = SetUp()
    
    def test_deleteCourseByName(self):
        try:
            Course.objects.create(name=self.util.courseName, description=self.util.description, instructor=self.util.instructor)
            CourseUtil.deleteCourseByName(self.util.courseName)
            self.assertFalse(list(Course.objects.filter(name=self.util.courseName)), msg="Failed to delete course by name.")
        except Exception as e:
            self.fail(msg= str(e) + " exception was thrown on attempt to delete a course by name")