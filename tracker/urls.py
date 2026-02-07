from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('marks/enter/', views.enter_marks, name='enter_marks'),
    path('students/<str:roll_no>/report/', views.student_report, name='student_report'),
    path('generate-sample-data/', views.generate_sample_data, name='generate_sample_data'),
]
