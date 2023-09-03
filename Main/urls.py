from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('faculty_login', views.faculty_login, name="faculty_login"),
    path('post_login', views.post_login, name="post_login"),
    path('faculty_register', views.faculty_register, name="faculty_register"),
    path('post_register', views.post_register, name="post_register"),
    path('home', views.home, name="home"),
    path('total_presence', views.total_presence, name="total_presence"),
    path('add_student', views.add_student, name="add_student"),
    path('post_add_student', views.post_add_student, name="post_add_student"),
    path('attendance', views.attendance, name="attendance"),
    path('report', views.report, name="report"),
    path('post_report', views.post_report, name="post_report"),
    path('generate_report', views.generate_report, name="generate_report"),
    path('logout', views.faculty_logout, name="faculty_logout")
]