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
        """Creates a course and saves it in the Course database.

        :param name: The name of the course to create
        :param description: The description of the course to create
        :param instructor: The instructor of this course
        :param tas: The list of TAs of this course
        :return: On success, the ID of the new course in the database, None otherwise
        :pre: Name must not be blank
        :post: TypeError is raised if required fields are not provided (name)
        """
        if name == "":
            raise TypeError("Course name cannot be empty.")

        course = Course.objects.create(
            name=name, description=description, instructor=instructor
        )

        if tas:
            for ta in tas:
                course.tas.add(ta)

        return course.id

    @staticmethod
    def getCourseByID(id: int) -> Optional[Course]:
        """Returns a course from the database, using it's ID.

        :param id: The ID of the course to find in the database.
        :return: On success, the course with an ID that matches the agument, None otherwise
        :pre: None
        :post: None
        """
        try:
            course = Course.objects.get(id=id)
            return course
        except Course.DoesNotExist:
            return None

    @staticmethod
    def getAllCourses() -> Optional[Iterable[Course]]:
        """Gets all courses from database.

        :return: All the courses in the Course database, None if it is empty
        """
        set: QuerySet = Course.objects.all()
        return set if set.exists() else None

    @staticmethod
    def getCourseByName(name: str) -> Optional[Course]:
        """Gets a course from the database, by it's name.

        :param name: The name of the course to find in the database
        :return: On success, the course with a name that matches the argument, None otherwise
        """
        try:
            course = Course.objects.filter(name=name)[0]
        except IndexError:
            return None

        return course

    @staticmethod
    def deleteCourseByName(name: str) -> bool:
        """Looks for a course that matches the argument name, deletes it if it exists.

        :param name: the name of the course to delete
        :return: True if course was found and deleted, False otherwise
        """
        course = CourseUtil.getCourseByName(name)
        if course:
            course.delete()
            return True
        else:
            return False
