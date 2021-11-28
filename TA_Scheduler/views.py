from django.shortcuts import render, redirect
from django.views import View
from .models import Account


class CreateAccounts(View):
    def get(self, request):
        return render(request, "createaccounts.html", {})

    def post(self, request):
        userExists = True
        username=request.POST['username']
        try:
            m = Account.objects.get(username=username)
        except:
            userExists = False
        if userExists:
            return render(request, "createaccounts.html", {"message": "username '"+username+"' is already in use"})
        else:
            m = Account(username=username, password=request.POST['password'])
            m.save()
            # should I stay here or go somewhere else?
            return render(request, "createaccounts.html", {"message": "account '"+username+"' created"})
