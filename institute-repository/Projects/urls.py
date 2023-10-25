from django.urls import path
from . import views

urlpatterns = [
    path('student/project', views.createProject, name='createProject'),
]