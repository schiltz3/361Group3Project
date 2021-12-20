from django.shortcuts import render
from django.views import View


class InstructorDashboard(View):
    def get(self, request):
        if request.user.groups.filter(name="admin").exists():
            group = "admin"
        elif request.user.groups.filter(name="instructor").exists():
            group = "instructor"
        else:
            group = "ta"
        return render(request, "dashboard/instructor.html", {"group": group})
