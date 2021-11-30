from django.shortcuts import render, redirect
from django.views import View
from .models import Account
from .utilities import AccountUtil


class CreateAccounts(View):
    def get(self, request):
        return render(request, "createaccounts.html", {"authorities": Account.AUTHORITY})

    def post(self, request):
        userExists = True
        username = request.POST['username']
        try:
            m = Account.objects.get(username=username)
        except:
            userExists = False
        if userExists:
            return render(request, "createaccounts.html", {"message": "username '"+username+"' is already in use",
                                                           "authorities": Account.AUTHORITY})
        else:
            m = AccountUtil.createAccount(username, request.POST['password'], request.POST['authority'])
            m.save()
            # should I stay here or go somewhere else?
            return render(request, "createaccounts.html", {"message": "account '"+username+"' created",
                                                           "authorities": Account.AUTHORITY})
