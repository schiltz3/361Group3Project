from django.shortcuts import render
from django.views import View

class CreateAccount(View):
    def get(self, request):
        return render(
            request,
            "account/create.html"
        )