from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduler.utilities.AccountUtil import AccountUtil


class Login(View):
    def get(self, request):
        return render(request, "login/login.html", {})
    def post(self, request):
        invalid = False
        invalidPassword = False
        try:
            user1 = AccountUtil.getAccountByUsername(request.POST['username'])
            invalidPassword = (user1.user.password != request.POST['password'])
        except:
            invalid = True
        if invalid:
            return render(request, "login/login.html", {"error": "invalid username"})
        elif invalidPassword:
            return render(request, "login/login.html", {"error": "invalid password"})
        else:
            request.session["username"] = user1.user.username
            return redirect("/home/")
