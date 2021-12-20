from django.shortcuts import render
from TA_Scheduler.utilities.AccountUtil import AccountUtil
from django.views import View


class EditAccount(View):
    def get(self, request):
        return render(
            request,
            "account/edit.html",
            {"group": AccountUtil.getUserGroup(request.user)},
        )
