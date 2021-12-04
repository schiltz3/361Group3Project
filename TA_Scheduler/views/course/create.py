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
        :param request: Request from course/create.html
        :return: Response with "instructors"
        """
        return render(
            request,
            "course/create.html",
            {"message": "", "instructors": AccountUtil.getInstructors()},
        )

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """
        Called when the user clicks submit.
        :param request: Request from course/create.html
        :return: Response with "instructors", "message", "warning" and "error" or redirect
        """
        # if user is anonymous or not admin, show error

        if request.user.is_anonymous or request.user.account.authority == 0:
            return redirect(
                to="home.html",
                permanent=True,
                kwargs={"error": "User is not authorized to create the course."}
            )

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
