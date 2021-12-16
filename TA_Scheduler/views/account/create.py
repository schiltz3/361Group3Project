from django.shortcuts import render
from django.views import View
from TA_Scheduler.models import Account
from TA_Scheduler.utilities.AccountUtil import AccountUtil


class CreateAccount(View):
    def get(self, request):
        group = AccountUtil.getUserGroup(user=request.user)
        return render(request, "account/create.html", {"message": " ", "group": group})

    def post(self, request):

        # Not correctly checking authority for null. Can't convert NoneType to int
        usertype = request.POST.get("authority")
        if usertype is not None:
            try:
                authority = int(usertype)
            except ValueError:
                authority = None

        username = request.POST.get("username")
        password = request.POST.get("password")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        # if only one of the fields is filled out and the user refreshes a site, it can send None
        if (
            username is None
            or username == ""
            or password is None
            or password == ""
            or authority is None
            or firstname is None
            or firstname == ""
            or lastname is None
            or lastname == ""
            or email is None
            or email == ""
        ):
            return render(
                request,
                "account/create.html",
                {"message": "Please fill out all required fields"},
            )
        # getAccountByUsername return None if user does not exist
        if AccountUtil.getAccountByUsername(username) is not None:
            return render(
                request,
                "account/create.html",
                {"message": "username '" + username + "' is already in use"},
            )
        else:
            if authority == 1:
                id = AccountUtil.createAdminAccount(username, password)
                AccountUtil.updateAccountInfo(
                    id,
                    firstname,
                    lastname,
                    email,
                    request.POST.get("address"),
                    request.POST.get("phone"),
                )
                return render(
                    request,
                    "account/create.html",
                    {"message": "Administrator account '" + username + "' created"},
                )
            elif authority == 2:
                id = AccountUtil.createInstructorAccount(username, password)
                AccountUtil.updateAccountInfo(
                    id,
                    firstname,
                    lastname,
                    email,
                    request.POST.get("address"),
                    request.POST.get("phone"),
                )
                return render(
                    request,
                    "account/create.html",
                    {"message": "Instructor account '" + username + "' created"},
                )
            elif authority == 3:
                id = AccountUtil.createTAAccount(username, password)
                AccountUtil.updateAccountInfo(
                    id,
                    firstname,
                    lastname,
                    email,
                    request.POST.get("address"),
                    request.POST.get("phone"),
                )
                return render(
                    request,
                    "account/create.html",
                    {"message": "TA account '" + username + "' created"},
                )
            elif authority < 1 or authority > 3:
                # Since we already check for null, now check if in correct range
                return render(
                    request,
                    "account/create.html",
                    {"message": "user type does not exist"},
                )
        # default error response
        return render(
            request,
            "account/create.html",
            {"message": "error occurred, no account created"},
        )
