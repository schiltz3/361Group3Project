from django.shortcuts import render
from django.views import View


class ListLab(View):
    def get(self, request):
        return render(request, "lab/list.html")
