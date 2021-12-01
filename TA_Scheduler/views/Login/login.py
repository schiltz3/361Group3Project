from django.shortcuts import render, redirect
from django.views import View
from TA_Scheduler.models import Account


class Login(View):

    def get(self, request):
        return render(request, "login/login.html", {})

    def post(self, request):
        invalid = False
        try:
            user = Account.objects.get(username=request.POST('username'))
            invalidPassword = (user.password() != request.POST('password'))
        except:
            invalid = True
        if invalid:
            render(request, "login/login.html", {"error: Invalid username"})
        elif invalidPassword:
            render(request, "login/login.html", {"error: Invalid password"})
        else:
            request.session["username"] = user.username
            return redirect("login/home.html")
