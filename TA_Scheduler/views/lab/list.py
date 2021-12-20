from django.shortcuts import render
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.views import View


class ListLab(View):
    def get(self, request):
        return render(request, "lab/list.html", {"group": AccountUtil.getUserGroup(request.user)})
