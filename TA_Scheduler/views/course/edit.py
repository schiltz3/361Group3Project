from django.shortcuts import render
from django.views import View

class EditCourse(View):
    def get(self, request):
        return render(
            request,
            "course/edit.html"
        )