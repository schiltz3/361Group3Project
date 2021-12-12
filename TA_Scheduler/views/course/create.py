from django.shortcuts import render, redirect
from TA_Scheduler.models import Account
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect, reverse
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil
from TA_Scheduler.utilities.RedirectUtil import RedirectUtil
from typing import List, Union, Optional

from TA_Scheduler.utilities.RedirectUtil import RedirectUtil


class CreateCourse(View):

    TEMPLATE = "course/create.html"
    MESSAGE = "message"
    ERROR = "error"
    WARNING = "warning"

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """Called when the user opens the page, course/create.html

        :param request: Request from course/create.html
        :return: Response with "instructors"
        :pre: User is not anonymous, instructor, or ta
        :post: None
        """
        return RedirectUtil.admin(
            request, "create courses", self.respond(request, self.MESSAGE, "")
        )

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """Called when the user clicks submit.

        :param request: Request from course/create.html
        :return: Response with "instructors", "message", "warning" and "error" or redirect
        :pre: None
        :post: Correct return or new class object
        :par: Side effect: Create a new class object
        """

        name: Optional[str] = str(request.POST.get("name", None))
        description: Optional[str] = str(request.POST.get("description", None))
        instructor: Optional[str] = str(request.POST.get("instructor", None))
        tas: List[str] = request.POST.getlist("ta")
        ta_accounts: List[Account] = []

        if name:
            if all(x.isalpha() or x.isnumeric() or x.isspace() for x in name):
                courses = CourseUtil.getAllCourses()
                if courses:
                    for course in courses:
                        if (course.name.casefold() == name.casefold()) and (
                            course.instructor.user.username.casefold()
                            == instructor.casefold()
                        ):
                            return self.respond(
                                request,
                                self.WARNING,
                                "Class already exists with this instructor.",
                            )

            else:
                return self.respond(
                    request, self.WARNING, "Name can only contain [A-z][0-9]"
                )

        else:
            return self.respond(request, self.WARNING, "Name must not be blank.")

        # check description
        if description:
            if not all(
                x.isalpha() or x.isnumeric() or x.isspace() for x in description
            ):
                return self.respond(
                    request, self.WARNING, "Description can only contain [A-z][0-9]"
                )

        else:
            return self.respond(request, self.WARNING, "Description must not be blank.")

        # check instructor
        if instructor:
            instructor_account = AccountUtil.getAccountByUsername(instructor)
            if instructor_account is None:
                return self.respond(
                    request, self.ERROR, "Instructor could not be found."
                )
        else:
            return self.respond(request, self.WARNING, "Instructor must not be blank.")

        # check tas
        if tas:
            for ta in tas:
                ta_account = AccountUtil.getAccountByUsername(ta)
                if not ta_account:
                    return self.respond(
                        request, self.ERROR, "TA '" + ta + "' does not exist."
                    )
                else:
                    ta_accounts.append(ta_account)

        # adds course to database if instructor, name and description are not none
        if instructor_account and name and description:
            CourseUtil.createCourse(name, description, instructor_account, ta_accounts)
            return self.respond(request, self.MESSAGE, "Course created.")

        return self.respond(request, self.ERROR, "Class could not be created.")

    def respond(self, request: HttpRequest, msg_type: str, msg: str):
        """Helper method that returns a response.

        :param request: the HTTP request object to use
        :param msg_type: the type of notification message
        :param msg: the message to show
        :pre: request must not be null
        :post: rendered response
        """

        context = {
            msg_type: msg,
            "tas": AccountUtil.getTAs(),
            "instructors": AccountUtil.getInstructors(),
        }
        return render(request, self.TEMPLATE, context)
