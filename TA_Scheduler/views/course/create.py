from django.shortcuts import render, redirect
from TA_Scheduler.models import Account
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil
from typing import Union


class CreateCourse(View):
    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Called when the user opens the page, course/create.html
        @param request: Request from course/create.html
        @return: Response with "instructors"
        """
        # TODO: should be pulled out to a utis class
        # if user is anonymous or not admin, redirect to correct page
        if request.user.is_anonymous:
            return redirect('/', {"error": "User is not authorized to create a course"})
        elif request.user.groups.filter(name="instructor").exists():
            return redirect('/dashboard/instructor/', {"error": "Instructors are not authorized to create courses"})
        elif request.user.groups.filter(name="ta").exists():
            return redirect('/dashboard/ta/', {"error": "TAs are not authorized to create courses"})

        return render(
            request,
            "course/create.html",
            {"message": "", "instructors": AccountUtil.getInstructors()},
        )

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Called when the user clicks submit.
        @param request: Request from course/create.html
        @return: Response with "instructors", "message", "warning" and "error" or redirect
        """

        name = request.POST["name"]
        description = request.POST["description"]
        instructor = request.POST["instructor"]

        # if name is blank show error
        if not name:
            return render(
                request,
                "course/create.html",
                {
                    "warning": "Class name must not be blank.",
                    "instructors": AccountUtil.getInstructors(),
                },
            )
        # TODO Check here if class already exists
        elif not description:
            return render(
                request,
                "course/create.html",
                {
                    "warning": "Class description must not be blank.",
                    "instructors": AccountUtil.getInstructors(),
                },
            )
        elif instructor == "Select Instructor":
            return render(
                request,
                "course/create.html",
                {
                    "warning": "Must select course instructor",
                    "instructors": AccountUtil.getInstructors(),
                },
            )

        # adds course to database
        # TODO need to confirm this works when users can be created
        CourseUtil.createCourse(name, description, instructor)

        return render(request, "course/create.html", {"message": "Course created."})
