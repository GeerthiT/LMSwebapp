"""LMSproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from LMSapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("courses/", views.course_list, name="course_list"),
    path('course_detail/<str:course_title>/', views.course_detail, name='course_detail'),
    path("admin/create_course/", views.create_course, name="create_course"),
    path('delete_course/<str:course_title>/', views.delete_course, name='delete_course'),
    path("logout/", views.user_logout, name="logout"),
    path("admin/", admin.site.urls),
]
