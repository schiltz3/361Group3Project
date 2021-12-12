from django.shortcuts import redirect, render
from django.views import View
from TA_Scheduler.utilities.CourseUtil import CourseUtil


class DeleteCourse(View):

    def get(self, request):

        if request.user.is_anonymous:
            return redirect("/", {"error": "User is not authorized to delete courses"})
        elif request.user.groups.filter(name="instructor").exists():
            return redirect(
                "/dashboard/instructor/",
                {"error": "Instructors are not authorized to delete courses"},
            )
        elif request.user.groups.filter(name="ta").exists():
            return redirect(
                "/dashboard/ta/", {"error": "TAs are not authorized to delete courses"}
            )

        courses = CourseUtil.getAllCourses()
        return render(request, "course/delete.html", {"courses" : courses})

    
