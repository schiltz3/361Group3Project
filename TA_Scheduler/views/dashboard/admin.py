from django.shortcuts import render
from django.views import View
from TA_Scheduler.utilities.AccountUtil import AccountUtil


class AdminDashboard(View):
    def get(self, request):
        group = AccountUtil.getUserGroup(user=request.user)
        return render(request, "dashboard/admin.html", {"group": group})
