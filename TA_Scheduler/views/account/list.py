from django.shortcuts import render
from django.views import View


class ListAccount(View):
    def get(self, request):
        return render(request, "account/list.html")
