from typing import List
from django.shortcuts import redirect, render
from django.views import View
from TA_Scheduler.utilities.CourseUtil import CourseUtil
from TA_Scheduler.utilities.RedirectUtil import RedirectUtil


class DeleteCourse(View):
    TEMPLATE = "course/delete.html"
    MESSAGE = "message"
    ERROR = "error"
    WARNING = "warning"

    def get(self, request):
        """
        Called when the user opens the Delete Course page.
        @param request: request from course/delete.html
        @return: response with the course selection
        @pre: User is not anonymous, instructor, or ta
        @post: None
        """
        courses = CourseUtil.getAllCourses()
        return RedirectUtil.admin(request, "delete courses", 
            render(request, self.TEMPLATE, {"courses" : courses}))

    def post(self, request):
        """
        Called when the user clicks the action to delete selected courses.
        @param request: Request from course/delete.html
        @return: Response with remaining courses, and a message 
            to inform about success or an error
        @pre: None
        @post: Correct return or new class object
        """
        courses: List[str] = request.POST.getlist("courses")
        error: bool = False
        errorMsg: str = "Failed to delete:"


        # delete selected courses
        if courses:
            for course in courses:
                if not CourseUtil.deleteCourseByName(course):
                    error = True
                    errorMsg.append(" " + course)

        # get remaining courses
        coursesRemaining = CourseUtil.getAllCourses()

        if error:
            return render(request, self.TEMPLATE, {"courses": coursesRemaining, "error": errorMsg})
        else:
            return render(request, self.TEMPLATE, {"courses": coursesRemaining, "message": "Successfully deleted selected courses."})




    
