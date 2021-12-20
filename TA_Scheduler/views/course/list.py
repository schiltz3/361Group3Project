from django.shortcuts import render
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.views import View


class ListCourse(View):
    def get(self, request):
        return render(request, "course/list.html")
