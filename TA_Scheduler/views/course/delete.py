from django.shortcuts import render
from django.views import View


class DeleteCourse(View):
    def get(self, request):
        return render(request, "course/delete.html")
