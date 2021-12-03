from django.shortcuts import render
from django.views import View


class DeleteAccount(View):
    def get(self, request):
        return render(request, "account/delete.html")
