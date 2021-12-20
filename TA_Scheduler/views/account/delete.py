from django.shortcuts import render
from django.views import View
from TA_Scheduler.utilities.AccountUtil import AccountUtil


class DeleteAccount(View):
    def get(self, request):
        """Called when the user opens the Delete Account page.

        :param request: request from account/delete.html
        :return: response with the account selection
        :pre: User is not anonymous, instructor, or ta
        :post: None
        """

        return render(
            request, "account/delete.html", {"accounts": AccountUtil.getAllAccounts(),
                                             "group": AccountUtil.getUserGroup(request.user)}
        )

    def post(self, request):
        """Called when the user opens the Delete Course page.

        :param request: request from account/delete.html
        :return: response with the account selection and message
        :pre: User is not anonymous, instructor, or ta
        :post: account selected, if it exists, is deleted
        """

        accountID = request.POST.get("account")
        # if the user refreshes a site, it can send None
        if accountID is None:
            return render(
                request,
                "account/delete.html",
                {
                    "message": "Please fill out all required fields",
                    "accounts": AccountUtil.getAllAccounts(),
                },
            )

        account = AccountUtil.getAccountByID(accountID)

        # if invalid account is somehow submitted
        if account is None:
            return render(
                request,
                "account/delete.html",
                {
                    "message": "Invalid account selection",
                    "accounts": AccountUtil.getAllAccounts(),
                },
            )
        else:
            account.delete()
            return render(
                request,
                "account/delete.html",
                {
                    "message": "Account deleted",
                    "accounts": AccountUtil.getAllAccounts(),
                },
            )
