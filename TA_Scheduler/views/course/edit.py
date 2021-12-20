from typing import Union, Optional
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.views import View


class EditCourse(View):
    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        return render(
            request,
            "course/edit.html",
            {"group": AccountUtil.getUserGroup(request.user)},
        )

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        return render(request, "course/edit.html")
