from django.shortcuts import render, redirect
from TA_Scheduler.models import Account
from django.views import View
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from TA_Scheduler.utilities.CourseUtil import CourseUtil


class CreateCourse(View):

    # this is called when the user opens the page, the course/create.html
    def get(self, request):
        return render(
            request,
            "course/create.html",
            {"message": "", "instructors": AccountUtil.getInstructors()},
        )

    # this is called when the user clicks submit.
    def post(self, request):
         #if user is anonymous or not admin, show error

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
        # CourseUtil.createCourse(name, description, instructor)

        return render(request, "course/create.html", {"message": "Course created."})
