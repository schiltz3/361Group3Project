from django.shortcuts import render
from django.views import View


class ListCourse(View):
    def get(self, request):
        return render(request, "course/list.html")
