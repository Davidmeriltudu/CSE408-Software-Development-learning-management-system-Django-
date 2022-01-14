from django.db import models
from classroom.models import Resource, Discussion, Quiz
# Create your models here.


class Course(models.Model):
    course_no = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    level = models.IntegerField(default=0)
    term = models.IntegerField(default=0)
    course_detail = models.TextField()


class Student(models.Model):

    def make_id():
        total = Student.objects.count()
        student_id = total+1+1300000
        try:
            student = Student.objects.get(student_id=student_id)
        except:
            student = None
        while student != None:
            student_id=student_id+1
            try:
                student=Student.objects.get(student_id=student_id)
            except:
                student = None
        return student_id

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_name = models.CharField(unique=True,max_length=200)
    password = models.CharField(max_length=200)
    conf_password = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Course, related_name='students')
    quizzes = models.ManyToManyField(Quiz,related_name="students")
    student_id = models.IntegerField(unique= True,default=make_id)
    address = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="student/profile/pics",null=True,blank=True,default="student/profile/pics/profile.png")
    registered = models.BooleanField(default=False)
    role = models.CharField(max_length=200,default="Student")


class Teacher(models.Model):

    def make_id():
        total = Teacher.objects.count()
        teacher_id = total + 1 + 2000000
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
        except:
            teacher = None
        while teacher != None:
            teacher_id = teacher_id + 1
            try:
                teacher = Teacher.objects.get(teacher_id=teacher_id)
            except:
                teacher = None
        return teacher_id
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_name = models.CharField(unique=True,max_length=200)
    password = models.CharField(max_length=200)
    conf_password = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    address = models.TextField()
    courses = models.ManyToManyField(Course, related_name='teachers')
    assignedCourses = models.ManyToManyField(Course, related_name='assignedTeachers', blank=True)
    teacher_id = models.IntegerField(unique=True,default=make_id)
    profile_pic = models.ImageField(upload_to="teacher/profile/pics",null=True,blank=True,default="teacher/profile/pics/profile.png")
    role = models.CharField(max_length=200,default="Teacher")


class UserNames(models.Model):
    user_name = models.CharField(max_length=200,unique=True)
    role = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)