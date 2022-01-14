import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.forms.formsets import formset_factory

from datetime import datetime,timedelta
from django.utils import timezone
from .forms import ResourceForm,DiscussionForm,ReplyForm, MakingQuizForm, QuizInformationForm, QuizAnswerForm
from signUp.models import Teacher,Student,Course
from .models import *
# Create your views here.

months = ['January','February','March','April','June','July','August','September','October','Novemeber','December']


class Week:
    def __init__(self, month1,day1,month2,day2,resource_name,resource_url):
        self.month1 = month1
        self.day1 = day1
        self.month2 = month2
        self.day2 = day2
        self.resource_name_url = zip(resource_name,resource_url)


def home(request):
    storage = messages.get_messages(request)
    student_id = request.session['user_id']
    if student_id > 1300000 and student_id < 2000000:
        courses = Course.objects.all()
        quizes = []
        student = Student.objects.get(student_id=student_id)
        takenCourses = student.courses.all()
        allQuizes = Quiz.objects.all()
        for quiz in allQuizes:
            if quiz.course in takenCourses:
                quizes.append(quiz)
        template_name = "classroom/homeStudent.html"
        context = {'quizes': quizes, 'courses': courses, 'student_id': student_id, 'messages': storage}
        return render(request, template_name, context)
    else:
        teacher_id = request.session['user_id']
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        courses = Course.objects.all()
        quizes = []
        assignedCourses = teacher.assignedCourses.all()
        allQuizes = Quiz.objects.all()
        for quiz in allQuizes:
            if quiz.course in assignedCourses:
                quizes.append(quiz)
        template_name = "classroom/homeTeacher.html"
        context = {'quizes': quizes, 'courses': courses, 'teacher_id': teacher_id, 'messages': storage}
        return render(request, template_name, context)


def courseStudent(request,pk):
    storage = messages.get_messages(request)
    course = Course.objects.get(pk=pk)
    student_id = request.session['user_id']
    student = Student.objects.get(student_id=student_id)
    takenCourses = student.courses.all()
    quizes = []
    student = Student.objects.get(student_id=student_id)
    allQuizes = Quiz.objects.all()
    for quiz in allQuizes:
        if quiz.course in takenCourses:
            quizes.append(quiz)
    if course not in takenCourses:
        notRegistered = True
        context = {'quizes': quizes,'course': course, 'student_id': student_id, 'notRegistered': notRegistered, 'messages': storage}
        template_name = "classroom/courseStudent.html"
        return render(request, template_name, context)
    else:
        resource = course.resource_set.all()
        resource_name = []
        resource_url = []
        resource_date = []
        for i in range(0, len(resource)):
            name = resource[i].resource.name
            name = name[name.find('/') + 1:]
            if not name.find('_') == -1:
                extention = name[name.find('.') + 1:]
                name = "".join(reversed(name))
                name = name[name.find('_') + 1:]
                name = "".join(reversed(name))
                name = name + "." + extention
            resource_name.append(name)
            resource_url.append(resource[i].resource.url)
            resource_date.append(resource[i].pub_date)
        resource_name_url_date = list(zip(resource_name, resource_url, resource_date))
        termDate = TermDate.objects.get(pk=1)
        weekList = []
        startOfTerm = termDate.dateStart
        endOfTerm = termDate.dateEnd
        start = startOfTerm
        now = timezone.now()
        while start <= now:
            end = start + timedelta(days=6)
            temp_name = []
            temp_url = []
            for name, url, date in resource_name_url_date:
                if date >= start and date <= end:
                    temp_name.append(name)
                    temp_url.append(url)
            week = Week(months[start.month - 1], start.day, months[end.month - 1], end.day, temp_name, temp_url)
            weekList.append(week)
            start = end + timedelta(days=1)
            if start > endOfTerm:
                break
        notRegistered = False
        context = {'quizes': quizes,'course': course, 'weekList': weekList, 'student_id': student_id, 'notRegistered': notRegistered, 'messages': storage}
        template_name = "classroom/courseStudent.html"
        return render(request,template_name,context)


def courseTeacher(request,pk):
    storage = messages.get_messages(request)
    teacher_id = request.session['user_id']
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    course = Course.objects.get(pk=pk)
    assignedCourses = teacher.assignedCourses.all()
    quizes = []
    allQuizes = Quiz.objects.all()
    for quiz in allQuizes:
        if quiz.course in assignedCourses:
            quizes.append(quiz)
    if course not in assignedCourses:
        assigned = False
        context = {'quizes': quizes,'course':course, 'teacher_id':teacher_id, 'assigned': assigned, 'messages': storage}
        template_name = "classroom/courseTeacher.html"
        return render(request,template_name,context)
    else:
        if request.method == 'POST':
            form = ResourceForm(request.POST,request.FILES)
            if form.is_valid():
                resource = form.cleaned_data['resource']
            temp = Resource()
            temp.course = course
            temp.resource = resource
            temp.teacher = teacher
            pub_data = timezone.now()
            temp.pub_date = pub_data
            temp.save()
            return HttpResponseRedirect(reverse('classroom:courseTeacher', args=(pk,)))
        else:
            form = ResourceForm()
            template_name = "classroom/courseTeacher.html"
            resource = course.resource_set.all()
            resource_name = []
            resource_url = []
            resource_date = []
            for i in range(0,len(resource)):
                name = resource[i].resource.name
                name = name[name.find('/') + 1:]
                if not name.find('_')== -1:
                    extention = name[name.find('.')+1:]
                    name = "".join(reversed(name))
                    name = name[name.find('_')+1:]
                    name = "".join(reversed(name))
                    name = name+"."+extention
                resource_name.append(name)
                resource_url.append(resource[i].resource.url)
                resource_date.append(resource[i].pub_date)
            resource_name_url_date = list(zip(resource_name,resource_url,resource_date))
            termDate = TermDate.objects.get(pk=1)
            weekList = []
            startOfTerm = termDate.dateStart
            endOfTerm = termDate.dateEnd
            start = startOfTerm
            now = timezone.now()
            while start <= now:
                end = start+timedelta(days=6)
                temp_name = []
                temp_url = []
                for name,url,date in resource_name_url_date:
                    if date >= start and date <= end:
                        temp_name.append(name)
                        temp_url.append(url)
                week = Week(months[start.month-1],start.day,months[end.month-1],end.day,temp_name,temp_url)
                weekList.append(week)
                start = end+timedelta(days=1)
                if start > endOfTerm:
                    break
            assigned = True
            context = {'quizes': quizes, 'course':course, 'form':form , 'weekList':weekList, 'teacher_id':teacher_id, 'assigned': assigned, 'messages': storage}
            return render(request,template_name,context)

def registration(request,student_id):
    storage = messages.get_messages(request)
    student = Student.objects.get(student_id=student_id)
    if student.registered == True:
        messages.info(request,"You have already registered")
        return redirect(request.META['HTTP_REFERER'])
    if request.method == 'POST':
        courseList = request.POST.getlist('courses')
        if len(courseList) <= 3:
            messages.info(request,"You have to take more than 3 courses")
            return redirect(request.META['HTTP_REFERER'])
        if len(courseList) > 7:
            messages.info(request, "You cannot take more than 7 courses")
            return redirect(request.META['HTTP_REFERER'])
        for course_no in courseList:
            course = Course.objects.get(course_no=course_no)
            student.courses.add(course)
        student.registered = True
        student.save()
        messages.success(request,"You have successfully registered")
        return HttpResponseRedirect(reverse('classroom:myCoursesStudent',args=(student_id,)))
    else:
        courseList = Course.objects.all()
        context =  {'courseList':courseList,'student_id':student.student_id, 'messages': storage}
        template_name = 'classroom/registrationForm.html'
        return render(request,template_name,context)


def myCoursesStudent(request,student_id):
    storage = messages.get_messages(request)
    student = Student.objects.get(student_id=student_id)
    courses = student.courses.all()
    quizes = []
    student = Student.objects.get(student_id=student_id)
    takenCourses = student.courses.all()
    allQuizes = Quiz.objects.all()
    for quiz in allQuizes:
        if quiz.course in takenCourses:
            quizes.append(quiz)
    template_name = "classroom/myCoursesStudent.html"
    context = {'quizes': quizes,'courses':courses, 'student_id': student.student_id, 'messages': storage, 'messages': storage}
    return render(request,template_name,context)


def myCoursesTeacher(request,teacher_id):
    storage = messages.get_messages(request)
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    courses = teacher.courses.all()
    quizes = []
    assignedCourses = teacher.assignedCourses.all()
    allQuizes = Quiz.objects.all()
    for quiz in allQuizes:
        if quiz.course in assignedCourses:
            quizes.append(quiz)
    courseObjects = []
    for course in courses:
        if course in assignedCourses:
            tuple = (course,True)
        else:
            tuple = (course,False)
        courseObjects.append(tuple)

    template_name = "classroom/myCoursesTeacher.html"
    context = {'quizes': quizes,'courses':courseObjects, 'teacher_id': teacher.teacher_id, 'messages': storage}
    return render(request,template_name,context)


def newsForum(request,course_pk):
    storage = messages.get_messages(request)
    isClicked = False
    user_id = request.session['user_id']
    course = Course.objects.get(pk=course_pk)
    discussions = Discussion.objects.filter(course=course)
    discussionIds = list(set(discussions.values_list('discussionId',flat=True)))
    firstDiscussions = []
    for id in discussionIds:
        discussions = Discussion.objects.filter(discussionId=id)
        firstDiscussions.append(discussions.order_by('pub_date').first())
    if request.method == 'POST':
        if request.POST.get('start'):
            isClicked = True
            form = DiscussionForm()
            if user_id > 1300000 and user_id < 2000000:
                student = Student.objects.get(student_id=user_id)
                template_name = "classroom/newsForumStudent.html"
                context = {'firstDiscussions': firstDiscussions, 'course': course, 'isClicked': isClicked, 'form': form, 'student': student, 'messages': storage}
                return render(request,template_name,context)
            else:
                teacher = Teacher.objects.get(teacher_id=user_id)
                template_name = "classroom/newsForumTeacher.html"
                context = {'firstDiscussions': firstDiscussions, 'course': course, 'isClicked': isClicked, 'form': form, 'teacher': teacher, 'messages': storage}
                return render(request, template_name, context)
        else:
            form  = DiscussionForm(request.POST)
            if form.is_valid():
                discussion = form.cleaned_data['discussion']
            discussionId = DiscussionId()
            discussionId.save()

            discussionObject = Discussion()
            discussionObject.discussion = discussion
            discussionObject.teacher = Teacher.objects.get(teacher_id=user_id)
            discussionObject.pub_date = timezone.now()
            discussionObject.course = course
            discussionObject.discussionId = discussionId
            discussionObject.save()

            return HttpResponseRedirect(reverse('classroom:newsForum',args=(course_pk,)))
    else:
        context = {'firstDiscussions': firstDiscussions, 'course': course, 'isClicked': isClicked, 'messages': storage}
        if user_id > 1300000 and user_id < 2000000:
            student = Student.objects.get(student_id=user_id)
            template_name = "classroom/newsForumStudent.html"
            context['student'] = student
        else:
            teacher = Teacher.objects.get(teacher_id=user_id)
            template_name = "classroom/newsForumTeacher.html"
            context['teacher'] = teacher

        return render(request,template_name,context)


def discussion(request,course_pk,discussionId):
    storage = messages.get_messages(request)
    replyClicked = False
    user_id = request.session['user_id']
    discId = DiscussionId.objects.get(discussionId=discussionId)
    course = Course.objects.get(pk=course_pk)
    discussions = Discussion.objects.filter(course=course,discussionId=discId)
    discussions = discussions.order_by('pub_date')
    template_name = "classroom/discussion.html"
    if user_id > 1300000 and user_id < 2000000:
        user = Student.objects.get(student_id=user_id)
    else:
        user = Teacher.objects.get(teacher_id=user_id)

    if request.method == 'POST':
        if request.POST.get('reply'):
            replyClicked = True
            form = ReplyForm()
            context = {'user': user, 'form': form, 'discussions': discussions, 'replyClicked': replyClicked, 'messages': storage}
            return render(request,template_name,context)
        else:
            form = ReplyForm(request.POST)
            if form.is_valid():
                newDiscussion = form.cleaned_data.get('discussion')
            newDiscussionId = DiscussionId.objects.get(discussionId=discussionId)
            newDiscussionId.save()

            discussion = Discussion()
            discussion.discussion = newDiscussion
            discussion.discussionId = newDiscussionId
            discussion.pub_date = timezone.now()
            discussion.course = course
            if user.role == "Student":
                discussion.student = user
            else:
                discussion.teacher = user
            discussion.save()
            return HttpResponseRedirect(reverse('classroom:discussion',args=(course_pk,discussionId)))
    else:
        context = {'user': user, 'discussions': discussions, 'replyClicked': replyClicked}
        return render(request, template_name, context)


def courseDetail(request,course_pk):
    storage = messages.get_messages(request)
    user_id = request.session['user_id']
    course = Course.objects.get(pk=course_pk)
    template_name = "classroom/courseDetail.html"
    if user_id > 1300000 and user_id < 2000000:
        student = Student.objects.get(student_id=user_id)
        quizes = []
        takenCourses = student.courses.all()
        allQuizes = Quiz.objects.all()
        for quiz in allQuizes:
            if quiz.course in takenCourses:
                quizes.append(quiz)
        context = {'quizes': quizes, 'course': course, 'student': student, 'role': "Student", 'messages': storage}
    else:
        teacher = Teacher.objects.get(teacher_id=user_id)
        quizes = []
        assignedCourses = teacher.assignedCourses.all()
        allQuizes = Quiz.objects.all()
        for quiz in allQuizes:
            if quiz.course in assignedCourses:
                quizes.append(quiz)
        context = {'quizes': quizes,'course': course, 'teacher': teacher, 'role': "Teacher", 'messages': storage}

    return render(request,template_name,context)


def makingQuiz(request,course_pk):
    storage = messages.get_messages(request)
    teacher_id = request.session['user_id']
    course = Course.objects.get(pk=course_pk)
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    isForm = False
    forms = []
    if request.method == "POST":
        if request.POST.get('quiz_number'):
            isForm = True
            extra = request.POST.get('quiz_number')
            makingQuizFormset = formset_factory(MakingQuizForm,extra=int(extra))
            formset = makingQuizFormset()
            form = QuizInformationForm()
            template_name = "classroom/makingQuiz.html"
            context  = {'form': form,'formset': formset, 'teacher': teacher, 'course': course, 'messages': storage, 'isForm': isForm}
            return render(request,template_name,context)
        else:
            form = QuizInformationForm(request.POST)
            makingQuizFormset = formset_factory(MakingQuizForm)
            formset = makingQuizFormset(request.POST)
            if form.is_valid() and formset.is_valid():
                name = form.cleaned_data.get('name')
                exam_date = form.cleaned_data.get('exam_date')
                start_time = form.cleaned_data.get('start_time')
                time = form.cleaned_data.get('time')
                quiz = Quiz()
                quiz.name = name
                quiz.exam_date = exam_date
                quiz.time = time
                quiz.teacher = teacher
                quiz.pub_date = timezone.now()
                quiz.course = course
                quiz.start_time = start_time
                quiz.save()

                for form in formset:
                    question = form.cleaned_data.get('question')
                    choice1 = form.cleaned_data.get('choice1')
                    choice2 = form.cleaned_data.get('choice2')
                    choice3 = form.cleaned_data.get('choice3')
                    choice4 = form.cleaned_data.get('choice4')
                    answer = form.cleaned_data.get('answer')
                    question = Question(question=question,quiz=quiz)
                    question.save()
                    print(question)
                    if answer == '1':
                        choice1 = Choice(choice=choice1,question=question,isAnswer=True)
                    else:
                        choice1 = Choice(choice=choice1,question=question)
                    if answer == '2':
                        choice2 = Choice(choice=choice2,question=question,isAnswer=True)
                    else:
                        choice2 = Choice(choice=choice2,question=question)
                    if answer == '3':
                        choice3 = Choice(choice=choice3,question=question,isAnswer=True)
                    else:
                        choice3 = Choice(choice=choice3,question=question)
                    if answer == '4':
                        choice4 = Choice(choice=choice4,question=question,isAnswer=True)
                    else:
                        choice4 = Choice(choice=choice4,question=question)
                    choice1.save()
                    choice2.save()
                    choice3.save()
                    choice4.save()
                return HttpResponseRedirect(reverse('classroom:courseTeacher',args=(course.pk,)))
    else:
        template_name = "classroom/makingQuiz.html"
        context = {'teacher': teacher, 'course': course, 'messages': storage, 'isForm': isForm}
        return render(request,template_name,context)


def quizStudent(request,quiz_pk):
    student_id = request.session['user_id']
    student = Student.objects.get(student_id=student_id)
    quiz = Quiz.objects.get(pk=quiz_pk)
    questions = quiz.question_set.all()
    extra  =  len(questions)
    QuizAnswerFormFormset = formset_factory(QuizAnswerForm,extra=extra)
    formset = QuizAnswerFormFormset()

    count = 1
    for question,form in zip(questions,formset):
        choices = []
        for choice in question.choice_set.all():
            choices.append(choice)
        form.fields['choice'].choices = [(choice.pk,choice.choice) for choice in choices]
        #form.fields['choice'].name = "question"+str(count)
        count += 1
    zipped_questions_formset = list(zip(questions,formset))

    context = {'student': student,'form': form ,'quiz': quiz, 'zipped_questions_formset': zipped_questions_formset, 'quiz_time': quiz.time}
    template_name = "classroom/quizStudent.html"
    return render(request,template_name,context)


def timeUp(request):
    pass
    # if request.method == "POST":
    #     data = json.loads(request.body)
    #     request.session['dict'] = data['dict']
    #     return HttpResponse("/home/quizStudent/timeUp")
    # else:
    #     choicePkList = request.session['dict']['choicePkList']
    #     print(choicePkList)
    #     marks = 0
    #     for pk in choicePkList:
    #         choice = Choice.objects.get(pk=id)
    #         if choice.isAnswer == True:
    #             marks += 1
    #     print(marks)
    #     template_name = "classroom/timeUp.html"
    #     return render(request,template_name,{})