from django.shortcuts import render
from django.views import View
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil


class CreateAccount(View):
    def get(self, request):
        return render(request, "account/create.html", {"message": " "})

    def post(self, request):
        preexisting = True
        username = request.POST['username']
        try:
            Account.objects.get(username=username)
        except:
            preexisting = False
        if preexisting:
            return render(request, "account/create.html", {"message": "username '" + username + "' is already in use"})
        else:
            usertype = int(request.POST['authority'])
            if usertype == 1:
                AccountUtil.createAdminAccount(username, request.POST['password'])
                return render(request, "account/create.html", {"message": "account '" + username + "' created"})
            elif usertype == 2:
                AccountUtil.createInstructorAccount(username, request.POST['password'])
                return render(request, "account/create.html", {"message": "account '" + username + "' created"})
            elif usertype == 3:
                AccountUtil.createTAAccount(username, request.POST['password'])
                return render(request, "account/create.html", {"message": "account '" + username + "' created"})
            else:
                return render(request, "account/create.html", {"message": "enter user type"})
