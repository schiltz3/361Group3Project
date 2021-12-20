from django.shortcuts import render
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.views import View


class EditLab(View):
    def get(self, request):
        return render(request, "lab/edit.html", {"group": AccountUtil.getUserGroup(request.user)})
