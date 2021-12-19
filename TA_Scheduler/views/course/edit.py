from typing import Union, Optional, List

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil
from TA_Scheduler.utilities.RedirectUtil import RedirectUtil


class EditCourse(View):
    """Edit Course View"""

    TEMPLATE = "course/edit.html"
    MESSAGE = "message"
    ERROR = "error"
    WARNING = "warning"
    context = {"selected_course": None}

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """Called when the user opens the page, course/edit.html

        :param request: Request from course/edit.html
        :return: Response with "Courses"
        :pre: User is not anonymous, instructor, or ta
        :post: None
        """
        return RedirectUtil.admin(request, "edit courses", self.respond(request))

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        """Called when the user clicks submit.

        :param request: Request from course/edit.html
        :return: Response with "Courses", "course", "message", "warning" and "error" or redirect
        :pre: None
        :post: Correct return or edited course object
        :par: Side effect: Edits a course object
        """

        course: Optional[str] = str(request.POST.get("course"))
        name: Optional[str] = str(request.POST.get("name"))
        description: Optional[str] = str(request.POST.get("description"))
        instructor: Optional[str] = str(request.POST.get("instructors"))
        tas: List[str] = request.POST.getlist("ta")

        self.resetMessage()

        # Selected course from list of current courses
        if course != "None":
            # Add course to context
            course_obj = CourseUtil.getCourseByName(course)
            self.context["selected_course"] = course_obj
            self.context["selected_tas"] = course_obj.tas.all()
            return self.respond(request)
        elif name and self.context.get("selected_course"):
            course_obj = self.context.get("selected_course")
            resp = self.validateCourseInput(
                request=request,
                name=name,
                description=description,
                instructor=instructor,
                tas=tas,
            )
            if resp is True:
                ta_accounts: List[Account] = []
                for ta in tas:
                    ta_accounts.append(AccountUtil.getAccountByUsername(ta))

                course_id = CourseUtil.editCourse(
                    course_obj.id,
                    name=name,
                    description=description,
                    instructor=AccountUtil.getAccountByUsername(instructor),
                    tas=ta_accounts,
                )

                course_obj = CourseUtil.getCourseByID(course_id)
                self.context["selected_course"] = course_obj
                self.context["selected_tas"] = course_obj.tas.all()
                return self.respond(request, self.MESSAGE, "Course Updated")
            else:
                return resp

    def validateCourseInput(
        self, request, name, description, instructor, tas
    ) -> Union[bool, HttpResponse]:
        # Convert Incorrect strings to NoneType
        if instructor == "None":
            instructor = None
        if description is None:
            return self.respond(request, self.WARNING, "Description must not be blank")
        if name is None:
            return self.respond(request, self.WARNING, "Class name must not be blank")

        # Verify instructor exists
        if instructor:
            instructor_account = AccountUtil.getAccountByUsername(instructor)
            if instructor_account is None:
                return self.respond(
                    request, self.ERROR, "Instructor could not be found."
                )

        # Verify tas exist
        if tas:
            for ta in tas:
                ta_account = AccountUtil.getAccountByUsername(ta)
                if not ta_account:
                    return self.respond(
                        request, self.ERROR, "TA '" + ta + "' does not exist."
                    )

        return True

    def resetMessage(self):
        self.context[self.MESSAGE] = None
        self.context[self.WARNING] = None
        self.context[self.ERROR] = None

    def respond(
        self, request: HttpRequest, msg_type: str = "NoMessage", msg: str = "", **kwargs
    ):
        """Helper method that returns a response.

        :param request: the HTTP request object to use
        :param msg_type: the type of notification message
        :param msg: the message to show
        :param kwargs: a dict of elements to be passed to the template
        :pre: request must not be null
        :post: rendered response
        """
        kwargs["courses"] = CourseUtil.getAllCourses()
        self.context[msg_type] = msg
        self.context["instructors"] = AccountUtil.getInstructors()
        self.context["tas"] = AccountUtil.getTAs()
        self.context.update(**kwargs)

        return render(request, self.TEMPLATE, self.context)
