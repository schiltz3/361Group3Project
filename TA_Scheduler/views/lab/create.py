from django.shortcuts import render
from django.views import View


class CreateLab(View):
    def get(self, request):
        return render(request, "lab/create.html")
