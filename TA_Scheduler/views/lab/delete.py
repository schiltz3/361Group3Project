from django.shortcuts import render
from django.views import View

class DeleteLab(View):
    def get(self, request):
        return render(
            request,
            "lab/delete.html"
        )