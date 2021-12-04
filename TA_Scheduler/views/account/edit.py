from django.shortcuts import render
from django.views import View


class EditAccount(View):
    def get(self, request):
        return render(request, "account/edit.html")
