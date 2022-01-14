from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import datetime
from signUp.forms import SignUpStudent, SignUpTeacher, Login, EditProfilePic, EditProfile
from .models import Teacher, Student, Course, UserNames
from classroom.models import *
# Create your views here.


def home(request):
    template_name = "signUp/home.html"
    return render(request,template_name)


def sign_up_form_student(request):
    template_name = "signUp/signUpStudent.html"
    form = SignUpStudent();
    context = {'form' : form}
    return render(request,template_name,context)


def sign_up_form_teacher(request):
    template_name = "signUp/signUpTeacher.html"
    form = SignUpTeacher()
    context = {'form' : form}
    return render(request,template_name,context)


def registered(request):
    template_name = "signUp/registered.html"
    return render(request,template_name)


def registering_student(request):
    args = {}
    if request.method == 'POST':
        form = SignUpStudent(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['user_name']
            student = Student.objects.get(user_name=user_name)
            user_student = UserNames(user_name=user_name,user_id=student.student_id,role="student")
            user_student.save()
            id = student.student_id
            return HttpResponseRedirect(reverse('signUp:registered'))
    args['form'] = form
    return render(request,'signUp/signUpStudent.html',args)



def registering_teacher(request):
    args = {}
    if request.method == 'POST':
        form = SignUpTeacher(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['user_name']
            teacher = Teacher.objects.get(user_name=user_name)
            user_teacher = UserNames(user_name=user_name,user_id=teacher.teacher_id,role='teacher')
            user_teacher.save()
            teacher_id = teacher.teacher_id
            return HttpResponseRedirect(reverse('signUp:courseOption',kwargs={'teacher_id':teacher_id}))
    args['form'] = form
    return render(request, 'signUp/signUpTeacher.html', args)


def courseOption(request, teacher_id):
    if request.method=='POST':
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        courseList = request.POST.getlist('courses')
        for course_no in courseList:
            print(course_no)
            course = Course.objects.get(course_no=course_no)
            teacher.courses.add(course)
        teacher.save()
        return HttpResponseRedirect(reverse('signUp:registered'))
    else:
        courses = Course.objects.all()
        template_name = "signUp/courseOption.html"
        context = {'courses':courses}
        return render(request,template_name,context)


# def logged_in(request):
#     template_name = "signUp/logged_in_student.html"
#     context = {}
#     return render(request,template_name,context)


def invalid_user_name_password(request):
    template_name = "signUp/notification.html"
    context = {}
    return render(request, template_name, context)


def loginForm(request):
    try:
        user_id = request.session['user_id']
        template_name = 'signUp/logged_in_student.html'
        return render(request,template_name)
    except:
         template_name = 'signUp/login.html'
         form = Login()
         context = {'form':form}
         return render(request,template_name,context)


def login(request):
    args = {}
    try:
        user_id = request.session['user_id']
        if user_id > 1300000 and user_id < 2000000:
            template_name = "signUp/logged_in_student.html"
        else:
            template_name="signUp/logged_in_teacher.html"
        context = {'user_id': user_id}
        return render(request,template_name,context)
    except:
        if request.method == 'POST':
            form = Login(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user_name = form.cleaned_data['user_name']
                try:
                    user_object = UserNames.objects.get(user_name=user_name)
                    if user_object.role == "student":
                        try:
                            student = Student.objects.get(user_name=user_name,password=password)
                            student_id = student.student_id
                            request.session['user_id'] = student_id
                            return HttpResponseRedirect(reverse('signUp:profileStudent',args=(student_id,)))
                        except:
                            return HttpResponseRedirect(reverse('signUp:invalid_user_name_password'))
                    else:
                        try:
                            teacher = Teacher.objects.get(user_name=user_name,password=password)
                            teacher_id = teacher.teacher_id
                            request.session['user_id'] = teacher_id
                            return HttpResponseRedirect(reverse('signUp:profileTeacher',args=(teacher_id,)))
                        except:
                            return HttpResponseRedirect(reverse('signUp:invalid_user_name_password'))
                except:
                    return HttpResponseRedirect(reverse('signUp:invalid_user_name_password'))
        args['form'] = form
        return render(request,'signUp/home.html',args)


def profileStudent(request,student_id):
    storage = messages.get_messages(request)
    try:
        user_id = request.session['user_id']
        template_name = "signUp/profileStudent.html"
        student = Student.objects.get(student_id=student_id)
        context = {'first_name':student.first_name, 'last_name':student.last_name,'address':student.address,'email':student.email, 'user_name':student.user_name, 'user_id':student.student_id,'profile_pic_url': student.profile_pic.url, 'messages': storage}
        return render(request,template_name,context)
    except:
        template_name = "signUp/not_logged_in.html"
        return render(request,template_name)


def profileTeacher(request,teacher_id):
    storage = messages.get_messages(request)
    try:
        user_id = request.session['user_id']
        template_name = "signUp/profileTeacher.html"
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        context = {'first_name': teacher.first_name, 'last_name': teacher.last_name, 'email': teacher.email,
                   'user_name': teacher.user_name, 'user_id': teacher.teacher_id, 'address': teacher.address,'profile_pic_url': teacher.profile_pic.url, 'messages': storage}
        return render(request, template_name, context)
    except:
        template_name2 = "signUp/not_logged_in.html"
        return render(request,template_name2)


def editProfileStudent(request,student_id):
    storage = messages.get_messages(request)
    student = Student.objects.get(student_id=student_id)
    if request.method == 'POST':
        if 'profilePic' in request.POST:
            form = EditProfilePic(request.POST,request.FILES)
            if form.is_valid():
                profile_pic = form.cleaned_data['profile_pic']
                student.profile_pic = profile_pic
                student.save()
                return HttpResponseRedirect(reverse('signUp:editProfileStudent', args=(student.student_id,)))
        if 'profileInfo' in request.POST:
            form = EditProfile(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                student.first_name = first_name
                student.last_name = last_name
                student.email = email
                student.address = address
                student.save()
                return HttpResponseRedirect(reverse('signUp:profileStudent', args=(student.student_id,)))
            else:
                formProfilePic = EditProfilePic()
                context = {'formProfilePic': formProfilePic, 'formProfileInfo': form,
                           'first_name': student.first_name, 'last_name': student.last_name, 'address': student.address,
                           'email': student.email, 'user_name': student.user_name, 'user_id': student.student_id,
                           'profile_pic_url': student.profile_pic.url, 'messages': storage}
                template_name = 'signUp/editProfileStudent.html'
                return render(request, template_name, context)


    else:
        formProfilePic = EditProfilePic()
        formProfileInfo = EditProfile(initial={'first_name':student.first_name,'last_name':student.last_name,'email':student.email,'address':student.address})
        context = {'formProfilePic':formProfilePic,'formProfileInfo':formProfileInfo, 'first_name':student.first_name, 'last_name':student.last_name,'address':student.address,'email':student.email, 'user_name':student.user_name, 'user_id':student.student_id, 'profile_pic_url':student.profile_pic.url, 'messages': storage}
        template_name = 'signUp/editProfileStudent.html'
        return render(request,template_name,context)



def editProfileTeacher(request,teacher_id):
    storage = messages.get_messages(request)
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    if request.method == 'POST':
        if 'profilePic' in request.POST:
            form = EditProfilePic(request.POST,request.FILES)
            if form.is_valid():
                profile_pic = form.cleaned_data['profile_pic']
                teacher.profile_pic = profile_pic
                teacher.save()
                return HttpResponseRedirect(reverse('signUp:editProfileTeacher', args=(teacher.teacher_id,)))
        if 'profileInfo' in request.POST:
            form = EditProfile(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                teacher.first_name = first_name
                teacher.last_name = last_name
                teacher.email = email
                teacher.address = address
                teacher.save()
                return HttpResponseRedirect(reverse('signUp:profileTeacher', args=(teacher.teacher_id,)))
            else:
                formProfilePic = EditProfilePic()
                context = {'formProfilePic': formProfilePic, 'formProfileInfo': form,
                           'first_name': teacher.first_name, 'last_name': teacher.last_name, 'address': teacher.address,
                           'email': teacher.email, 'user_name': teacher.user_name, 'user_id': teacher.teacher_id,
                           'profile_pic_url': teacher.profile_pic.url, 'messages': storage}
                template_name = 'signUp/editProfileTeacher.html'
                return render(request, template_name, context)

    else:
        formProfilePic = EditProfilePic()
        formProfileInfo = EditProfile(initial={'first_name':teacher.first_name,'last_name':teacher.last_name,'email':teacher.email,'address':teacher.address})
        context = {'formProfilePic':formProfilePic,'formProfileInfo':formProfileInfo, 'first_name':teacher.first_name, 'last_name':teacher.last_name,'address':teacher.address,'email':teacher.email, 'user_name':teacher.user_name, 'user_id':teacher.teacher_id, 'profile_pic_url':teacher.profile_pic.url, 'messages': storage}
        template_name = 'signUp/editProfileTeacher.html'
        return render(request,template_name,context)


def logout(request):
    try:
        user_id = request.session['user_id']
        del request.session['user_id']
        return HttpResponseRedirect(reverse('signUp:home'))
    except:
        template_name2 = "signUp/not_logged_in.html"
        return render(request, template_name2)