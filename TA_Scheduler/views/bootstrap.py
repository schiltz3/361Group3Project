from django.shortcuts import render
from django.views import View


class BootstrapTest(View):
    def get(self, request):
        return render(request, "bootstrap_test.html")

    def post(self, request):
        return render(request, "bootstrap_test.html")
