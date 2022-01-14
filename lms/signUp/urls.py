from django.urls import path
from django.urls import path, include
from . import views

app_name = 'signUp'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:student_id>/editProfileStudent/',views.editProfileStudent,name='editProfileStudent'),
    path('<int:teacher_id>/editProfileTeacher/',views.editProfileTeacher,name='editProfileTeacher'),
    path('login/', views.loginForm, name='loginForm'),
    path('signUpStudent/', views.sign_up_form_student,name='signUpStudent'),
    path('signUpTeacher/', views.sign_up_form_teacher,name='signUpTeacher'),
    path('registered/',views.registered, name='registered'),
    path('registeringStudent/',views.registering_student,name='registeringStudent'),
    path('registeringTeacher/',views.registering_teacher,name='registeringTeacher'),
    path('logging_in/',views.login,name="logging_in"),
    path('<int:teacher_id>/profileTeacher/',views.profileTeacher,name='profileTeacher'),
    path('<int:student_id>/profileStudent/',views.profileStudent,name='profileStudent'),
    # path('<int:student_id>/homeStudent/',views.homeStudent,name = 'homeStudent'),
    # path('<int:teacher_id>/homeTeacher/',views.homeTeacher,name = 'homeTeacher'),
    # path('<int:pk>/courseStudent/',views.courseStudent,name = 'courseStudent'),
    # path('<int:pk>/courseTeacher/',views.courseTeacher,name = 'courseTeacher'),
    # path('<int:student_id>/registration/',views.registration,name="registration"),
    # path('<int:student_id>/myCoursesStudent',views.myCoursesStudent,name='myCoursesStudent'),
    # path('<int:teacher_id>/myCoursesTeacher/',views.myCoursesTeacher,name='myCoursesTeacher'),
    path('invalid_user_name_password/',views.invalid_user_name_password,name='invalid_user_name_password'),
    path('logging_out/',views.logout,name="logging_out"),
    path('<int:teacher_id>/courseOption/',views.courseOption,name='courseOption'),

]