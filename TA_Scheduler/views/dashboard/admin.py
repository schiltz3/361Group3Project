from django.shortcuts import render, redirect
from django.views import View


class AdminDashboard(View):
    def get(self, request):
        return render(request, "dashboard/admin.html", {})