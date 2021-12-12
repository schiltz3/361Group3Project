from typing import Iterable, List, Optional, Union
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from TA_Scheduler.models import Account, Course


class CourseUtil:
    @staticmethod
    def createCourse(
        name: str,
        description: str = None,
        instructor: Account = None,
        tas: List[Account] = None,
    ) -> Union[int, TypeError]:
        """
        Creates a course and saves it in the Course database
        TypeError is raised if required fields are not provided (name)
        Returns the id of the created course
        """
        if name == "":
            raise TypeError("Course name cannot be empty.")

        course = Course.objects.create(
            name=name, description=description, instructor=instructor
        )

        for ta in tas:
            course.tas.add(ta)

        return course.id

    @staticmethod
    def getCourseByID(id: int) -> Optional[Course]:
        """
        Returns a course from the database, using it's ID
        If the course does not exist, returns None
        """
        try:
            course = Course.objects.get(id=id)
            return course
        except Course.DoesNotExist:
            return None

    @staticmethod
    def getAllCourses() -> Optional[Iterable[Course]]:
        """
        Gets all courses from database
        If the database is empty, returns None
        """
        set: QuerySet = Course.objects.all()
        return set if set.exists() else None

    @staticmethod
    def getCourseByName(name: str) -> Optional[Course]:
        """
        Gets a course from the database, by it's name.
        If the course is not found, returns None
        """
        try:
            course = Course.objects.filter(name=name)[0]
        except IndexError:
            return None

        return course

    @staticmethod
    def deleteCourseByName(name: str) -> bool:
        """
        Looks for a course that matches the argument name,
        deletes it if it exists.
        @param name: the name of the course to delete
        @return: True if course was found and deleted,
            False otherwise
        """
        course = CourseUtil.getCourseByName(name)
        if course:
            course.delete()
            return True
        else:
            return False
