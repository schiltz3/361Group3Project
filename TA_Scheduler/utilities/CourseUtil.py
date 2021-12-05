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

        print(course.tas)

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
