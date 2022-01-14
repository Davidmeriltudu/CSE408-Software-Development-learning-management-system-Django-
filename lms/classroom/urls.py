from django.urls import path
from django.urls import path, include
from . import views

app_name = 'classroom'

urlpatterns = [
    path('', views.home, name='home'),
    # path('<int:student_id>/homeStudent/',views.homeStudent,name = 'homeStudent'),
    # path('<int:teacher_id>/homeTeacher/',views.homeTeacher,name = 'homeTeacher'),
    path('<int:pk>/courseStudent/',views.courseStudent,name='courseStudent'),
    path('<int:pk>/courseTeacher/',views.courseTeacher,name='courseTeacher'),
    path('<int:student_id>/registration/',views.registration,name="registration"),
    path('<int:student_id>/myCoursesStudent',views.myCoursesStudent,name='myCoursesStudent'),
    path('<int:teacher_id>/myCoursesTeacher/',views.myCoursesTeacher,name='myCoursesTeacher'),
    #path('<int:course_pk>/newsForum/',views.newsForum,{'isClicked': False },name='newsForum'),
    path('<int:course_pk>/newsForum/',views.newsForum,name='newsForum'),
    path('<int:course_pk>/<int:discussionId>/discussion/',views.discussion,name='discussion'),
    path('<int:course_pk>/courseDetail/', views.courseDetail, name='courseDetail'),
    path('<int:course_pk>/makingQuiz/',views.makingQuiz, name='makingQuiz'),
    path('<int:quiz_pk>/quizStudent/', views.quizStudent, name='quizStudent'),
    path('quizStudent/timeUp/', views.timeUp, name='timeUp'),
]