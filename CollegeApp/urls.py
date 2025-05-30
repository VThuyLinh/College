# your_app_name/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views
from .views import *

r = routers.DefaultRouter()
r.register('creat_student_account', views.StudentCreateAPIView, basename='creat_student_account')
r.register('creat_faculty_account', views.FacultyCreateAPIView, basename='creat_faculty_account')
r.register('create-registrations', views.AdvisoryRegistrationCreateView, basename='create-registrations')
r.register('view-registrations', views.AdvisoryRegistrationListView, basename='view-registrations')
r.register('detail-registrations', views.AdvisoryRegistrationDetailView, basename='detail-registrations')

urlpatterns = [
    path('', include(r.urls)),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
]