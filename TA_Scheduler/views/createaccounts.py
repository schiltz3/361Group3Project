from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduler.models import Account
from TA_Scheduler.utilities import AccountUtil


class CreateAccounts(View):
    def get(self, request):
        return render(request, "createaccounts.html", {"message": "", "authorities": Account.AUTHORITY})

    def post(self, request):
        preexisting = True
        username = request.POST['username']
        try:
            Account.objects.get(username=username)
        except:
            preexisting = False
        if preexisting:
            return render(request, "createaccounts.html", {"message": "username '" + username + "' is already in use",
                                                           "authorities": Account.AUTHORITY})
        else:
            m = AccountUtil.createAccount(username, request.POST['password'], request.POST['authority'])
            m.save()
            # should I stay here or go somewhere else?
            return render(request, "createaccounts.html", {"message": "account '" + username + "' created",
                                                           "authorities": Account.AUTHORITY})
