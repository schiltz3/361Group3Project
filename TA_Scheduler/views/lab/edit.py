from django.shortcuts import render
from django.views import View

class EditLab(View):
    def get(self, request):
        return render(
            request,
            "lab/edit.html"
        )