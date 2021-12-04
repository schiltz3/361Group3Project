"""CS361Group3Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# login/homepage
from TA_Scheduler.views.Login.loginViews import Login
from TA_Scheduler.views.homepage.home import Home


# course
from TA_Scheduler.views.course.create import CreateCourse
from TA_Scheduler.views.course.list import ListCourse
from TA_Scheduler.views.course.edit import EditCourse
from TA_Scheduler.views.course.delete import DeleteCourse

# account
from TA_Scheduler.views.account.create import CreateAccount
from TA_Scheduler.views.account.list import ListAccount
from TA_Scheduler.views.account.edit import EditAccount
from TA_Scheduler.views.account.delete import DeleteAccount

# account
from TA_Scheduler.views.lab.create import CreateLab
from TA_Scheduler.views.lab.list import ListLab
from TA_Scheduler.views.lab.edit import EditLab
from TA_Scheduler.views.lab.delete import DeleteLab

# dashboard
from TA_Scheduler.views.dashboard.admin import AdminDashboard
from TA_Scheduler.views.dashboard.instructor import InstructorDashboard
from TA_Scheduler.views.dashboard.ta import TADashboard

from TA_Scheduler.views.bootstrap import BootstrapTest

from TA_Scheduler.views.tester import TestHomePage

urlpatterns = [
    path("admin/", admin.site.urls),
    #login
    path("", Login.as_view(), name="login"),

    # course
    path("course/create/", CreateCourse.as_view(), name="create-course"),
    path("course/edit/", EditCourse.as_view(), name="edit-course"),
    path("course/list/", ListCourse.as_view(), name="list-course"),
    path("course/edit/", DeleteCourse.as_view(), name="delete-course"),
    # account
    path("account/create/", CreateAccount.as_view(), name="create-account"),
    path("account/edit/", EditAccount.as_view(), name="edit-account"),
    path("account/list/", ListAccount.as_view(), name="list-account"),
    path("account/edit/", DeleteAccount.as_view(), name="delete-account"),
    # dashboards
    path("dashboard/admin/", AdminDashboard.as_view(), name="admin-dashboard"),
    path(
        "dashboard/instructor/",
        InstructorDashboard.as_view(),
        name="instructor-dashboard",
    ),
    path("dashboard/ta/", TADashboard.as_view(), name="ta-dashboard"),
    # lab
    path("lab/create/", CreateLab.as_view(), name="create-lab"),
    path("lab/edit/", EditLab.as_view(), name="edit-lab"),
    path("lab/list/", ListLab.as_view(), name="list-lab"),
    path("lab/edit/", DeleteLab.as_view(), name="delete-lab"),
    path("bootstrapTest/", BootstrapTest.as_view(), name="bootstrap-test"),
    path("testhome/", TestHomePage.as_view(), name="test-home"),
]
