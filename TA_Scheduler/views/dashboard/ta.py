from django.shortcuts import render
from django.views import View


class TADashboard(View):
    def get(self, request):
        return render(request, "dashboard/ta.html",{})
