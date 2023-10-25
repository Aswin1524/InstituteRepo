from django.urls import path
from . import views

urlpatterns = [
    # path('login/student', views.loginStudent, name='loginStudent'),
    # path('login/instructor', views.loginFaculty, name='loginFaculty'),
    # path('signup/student', views.signupStudent, name='signupStudent'),
    # path('signup/instructor', views.signupFaculty, name='signupFaculty'),
    path('logout', views.userLogout, name='userLogout'),
    path('student', views.user, name='user'),
]