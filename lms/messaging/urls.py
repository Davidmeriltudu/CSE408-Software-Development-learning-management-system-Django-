from django.urls import path
from django.urls import path, include
from . import views

app_name = 'messaging'

urlpatterns = [
    path('',views.messaging, name='messaging'),
    path('sentboxStudnet/',views.sentboxStudent,name='sentboxStudent'),
    path('sentboxTeacher/',views.sentboxTeacher,name='sentboxTeacher'),
    path('inboxStudent/',views.inboxStudent,name='inboxStudent'),
    path('inboxTeacher/',views.inboxTeacher,name='inboxTeacher'),
    path('messageboxStudent/',views.studentMessageBox,name='studentMessageBox'),
    path('messageboxTeacher/',views.teacherMessageBox,name='teacherMessageBox'),
    path('<int:chatId>/message/',views.message,name='message'),
]