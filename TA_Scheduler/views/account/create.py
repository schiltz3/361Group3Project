from django.shortcuts import render
from django.views import View
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil


class CreateAccount(View):
    def get(self, request):
        return render(request, "account/create.html", {"message": " "})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Not correctly checking authority for null. Can't convert NoneType to int
        usertype = request.POST.get("authority")
        if usertype is not None:
            try:
                authority = int(usertype)
            except ValueError:
                authority = None

        # if only one of the fields is filled out and the user refreshes a site, it can send None
        if username is None or password is None or authority is None or usertype is None:
            return render(
                request,
                "account/create.html",
                {"message": "Please fill out all fields"},
            )
        # getAcountByUsername return None if user does not exist
        if AccountUtil.getAccountByUsername(username) is not None:
            return render(
                request,
                "account/create.html",
                {"message": "username '" + username + "' is already in use"},
            )
        else:
            if authority == 1:
                AccountUtil.createAdminAccount(username, password)
                return render(
                    request,
                    "account/create.html",
                    # "Admin" did not match the test"
                    {"message": "Administrator account '" + username + "' created"},
                )
            elif authority == 2:
                AccountUtil.createInstructorAccount(username, password)
                return render(
                    request,
                    "account/create.html",
                    {"message": "Instructor account '" + username + "' created"},
                )
            elif authority == 3:
                AccountUtil.createTAAccount(username, password)
                return render(
                    request,
                    "account/create.html",
                    {"message": "TA account '" + username + "' created"},
                )
            elif authority < 1 or authority > 3:
                return render(
                    # Since we already check for null, now check if in correct range
                    request,
                    "account/create.html",
                    {"message": "user type does not exist"},
                )
        # Should put some default response here like an error message or a redirect to login or home with an error message
