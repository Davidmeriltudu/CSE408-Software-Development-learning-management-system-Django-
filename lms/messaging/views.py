from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from signUp.models import Teacher, Student, UserNames
from .models import MessageTS,MessageST,MessageTT,MessageSS,Chat
from .forms import MessageForm, ReplyForm


def messaging(request):
    storage = messages.get_messages(request)
    try:
        user_id = request.session['user_id']
        if user_id > 1300000 and user_id < 2000000:
            student_id = request.session['user_id']
            student = Student.objects.get(student_id=student_id)
            template_name = 'messaging/messageStudent.html'
            context = {'user_name': student.user_name, 'student_id': student_id, 'profile_pic_url': student.profile_pic.url, 'messages': storage}  # 'user_name':student.user_name}
            return render(request, template_name, context)
        else:
            teacher_id = request.session['user_id']
            teacher = Teacher.objects.get(teacher_id=teacher_id)
            template_name = 'messaging/messageTeacher.html'
            context = {'user_name': teacher.user_name, 'teacher_id': teacher_id, 'profile_pic_url': teacher.profile_pic.url, 'messages': storage}  # 'user_name':student.user_name}
            return render(request, template_name, context)
    except:
        template_name = "signUp/not_logged_in.html"
        return render(request,template_name)

def inboxStudent(request):
    storage = messages.get_messages(request)
    student_id = request.session['user_id']
    student = Student.objects.get(student_id=student_id)
    template_name = 'messaging/inboxStudent.html'

    messageObjects = []

    messagesSS = MessageSS.objects.filter(receiver=student)
    chatList = list(set(messagesSS.values_list('chat', flat=True)))
    for chat in chatList:
        messagesTemp = messagesSS.filter(chat=chat)
        messagesTemp= messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])

    messagesTS = MessageTS.objects.filter(receiver=student)
    chatList = list(set(messagesTS.values_list('chat', flat=True)))
    for chat in chatList:
        messagesTemp = messagesTS.filter(chat=chat)
        messagesTemp = messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])


    messageObjects.sort(key=lambda x: x.pub_date,reverse=True)
    context = {'messageObjects':messageObjects, 'user_name':student.user_name, 'student_id': student_id, 'profile_pic_url': student.profile_pic.url, 'messages': storage}
    return render(request, template_name, context)


def inboxTeacher(request):
    storage = messages.get_messages(request)
    teacher_id = request.session['user_id']
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    template_name = 'messaging/inboxTeacher.html'

    messageObjects = []

    messagesST = MessageST.objects.filter(receiver=teacher)
    chatList = list(set(messagesST.values_list('chat', flat=True)))
    for chat in chatList:
        messagesTemp = messagesST.filter(chat=chat)
        messagesTemp = messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])

    messagesTT = MessageTT.objects.filter(receiver=teacher)
    chatList = list(set(messagesTT.values_list('chat', flat=True)))
    for chat in chatList:
        messagesTemp = messagesTT.filter(chat=chat)
        messagesTemp = messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])


    messageObjects.sort(key=lambda x: x.pub_date, reverse=True)
    context = {'messageObjects':messageObjects, 'user_name':teacher.user_name, 'teacher_id': teacher_id,'profile_pic_url': teacher.profile_pic.url, 'messages': storage}
    return render(request, template_name, context)


def sentboxStudent(request):
    storage = messages.get_messages(request)
    for message in storage:
        print(message)
    student_id = request.session['user_id']
    student = Student.objects.get(student_id=student_id)
    template_name = 'messaging/sentboxStudent.html'

    messageObjects = []

    messagesSS = MessageSS.objects.filter(sender=student)
    chatList = list(set(messagesSS.values_list('chat', flat=True)))
    for chat in chatList:
        messagesTemp = messagesSS.filter(chat=chat)
        messagesTemp = messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])

    messagesST = MessageST.objects.filter(sender=student)
    chatList = list(set(messagesST.values_list('chat', flat=True)))
    for chat in chatList:
        messagesTemp = messagesST.filter(chat=chat)
        messagesTemp = messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])

    messageObjects.sort(key=lambda x: x.pub_date,reverse=True)
    context = {'messageObjects': messageObjects, 'user_name': student.user_name, 'student_id':student_id,'profile_pic_url': student.profile_pic.url, 'messages': storage}
    return render(request, template_name, context)


def sentboxTeacher(request):
    storage = messages.get_messages(request)
    teacher_id = request.session['user_id']
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    template_name = 'messaging/sentboxTeacher.html'

    messageObjects = []

    messagesTT = MessageTT.objects.filter(sender=teacher)
    chatList = list(set(messagesTT.values_list('chat',flat=True)))
    for chat in chatList:
        messagesTemp = messagesTT.filter(chat=chat)
        messagesTemp = messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])

    messagesTS = MessageTS.objects.filter(sender=teacher)
    chatList = list(set(messagesTS.values_list('chat', flat=True)))
    for chat in chatList:
        messagesTemp = messagesTS.filter(chat=chat)
        messagesTemp = messagesTemp.order_by('-pub_date')
        messageObjects.append(messagesTemp[0])

    messageObjects.sort(key=lambda x: x.pub_date, reverse=True)
    context = {'messageObjects':messageObjects, 'user_name':teacher.user_name, 'teacher_id':teacher_id,'profile_pic_url': teacher.profile_pic.url, 'messages': storage}
    return render(request, template_name, context)


def studentMessageBox(request):
    storage = messages.get_messages(request)
    student_id = request.session['user_id']
    student = Student.objects.get(student_id=student_id)
    user_name=""
    message=""
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            message = form.cleaned_data['message']
        user = UserNames.objects.get(user_name=user_name)
        if user.role == 'teacher':
            teacher = Teacher.objects.get(user_name=user_name)
            now = timezone.now()
            chat = Chat()
            chat.save()
            messageBox = MessageST(message=message,sender=student,receiver=teacher,pub_date=now,chat=chat)
            messageBox.save()
        else:
            student2 = Student.objects.get(user_name=user_name)
            now = timezone.now()
            chat = Chat()
            chat.save()
            messageBox = MessageSS(message=message,sender=student,receiver=student2,pub_date=now,chat=chat)
            messageBox.save()
        messages.success(request,"Your message was sent successully")
        return HttpResponseRedirect(reverse('messaging:sentboxStudent'))

    else:
        template_name = 'messaging/studentMessageBox.html'
        form = MessageForm()
        context = {'form': form, 'user_name':student.user_name, 'student_id':student_id,'profile_pic_url': student.profile_pic.url, 'messages': storage}# 'user_name':student.user_name}
        return render(request, template_name, context)


def teacherMessageBox(request):
    storage = messages.get_messages(request)
    teacher_id = request.session['user_id']
    teacher = Teacher.objects.get(teacher_id=teacher_id)
    user_name = ""
    message = ""
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            message = form.cleaned_data['message']
        user = UserNames.objects.get(user_name=user_name)
        if user.role=='student':
            student = Student.objects.get(user_name=user_name)
            now = timezone.now()
            chat = Chat()
            chat.save()
            messageBox = MessageTS(message=message, sender=teacher, receiver=student, pub_date=now,chat=chat)
            messageBox.save()
        else:
            teacher2 = Teacher.objects.get(user_name=user_name)
            now = timezone.now()
            chat = Chat()
            chat.save()
            messageBox = MessageTT(message=message,sender=teacher,receiver=teacher2,pub_date=now,chat=chat)
            messageBox.save()
        messages.success(request, "Your message was sent successully")
        return HttpResponseRedirect(reverse('messaging:sentboxTeacher'))
    else:
        template_name = 'messaging/teacherMessageBox.html'
        form = MessageForm()
        context = {'form': form, 'user_name': teacher.user_name, 'teacher_id':teacher_id,'profile_pic_url': teacher.profile_pic.url, 'messages': storage}
        return render(request, template_name, context)


def message(request,chatId):
    storage = messages.get_messages(request)
    replyClicked =False
    user_id = request.session['user_id']

    if user_id > 1300000 and user_id < 2000000:
        sender = Student.objects.get(student_id=user_id)
    else:
        sender = Teacher.objects.get(teacher_id=user_id)

    chat = Chat.objects.get(chatId=chatId)
    messagesST = MessageST.objects.filter(chat=chat)
    messagesTS = MessageTS.objects.filter(chat=chat)
    messagesSS = MessageSS.objects.filter(chat=chat)
    messagesTT = MessageTT.objects.filter(chat=chat)

    messageObjects = []

    for message in messagesST:
        messageObjects.append(message)
    for message in messagesTS:
        messageObjects.append(message)
    for message in messagesSS:
        messageObjects.append(message)
    for message in messagesTT:
        messageObjects.append(message)

    messageObjects.sort(key=lambda x: x.pub_date)

    message = messageObjects[0]
    if message.sender == sender:
        receiver = message.receiver
    else:
        receiver = message.sender

    if request.method == 'POST':
        if request.POST.get("reply"):
            replyClicked = True
            form = ReplyForm()
            if sender.role == "Student":
                template_name = "messaging/message.html"
                context = {'messageObjects': messageObjects, 'student_id': sender.student_id, 'user_name': sender.user_name,
                           'profile_pic_url': sender.profile_pic.url, 'replyClicked': replyClicked, 'role': sender.role,
                           'chatId':chatId, 'form':form, 'receiver':receiver, 'messages': storage}
                return render(request, template_name, context)
            else:
                template_name = "messaging/message.html"
                context = {'messageObjects':messageObjects, 'teacher_id':sender.teacher_id, 'user_name': sender.user_name, 'profile_pic_url':sender.profile_pic.url, 'replyClicked': replyClicked, 'role': sender.role, 'chatId': chatId, 'form':form, 'receiver':receiver, 'messages': storage}
                return render(request, template_name, context)
        else:
            form = ReplyForm(request.POST)
            if form.is_valid():
                newMessage = form.cleaned_data['message']

            if sender.role == "Student" and receiver.role == "Teacher":
                replyMessage = MessageST()
            elif sender.role == "Teacher" and receiver.role == "Student":
                replyMessage = MessageTS()
            elif sender.role == "Student" and receiver.role == "Student":
                replyMessage = MessageSS()
            else:
                replyMessage = MessageTT()

            chat = Chat.objects.get(chatId=chatId)
            now = timezone.now()

            replyMessage.message = newMessage
            replyMessage.sender = sender
            replyMessage.receiver = receiver
            replyMessage.pub_date = now
            replyMessage.chat = chat
            replyMessage.save()

            return HttpResponseRedirect(reverse('messaging:message',args=(chatId,)))
    else:
        replyClicked = False
        if sender.role == "Student":
            template_name = "messaging/message.html"
            context = {'messageObjects':messageObjects, 'student_id':sender.student_id, 'user_name':sender.user_name, 'profile_pic_url':sender.profile_pic.url, 'replyClicked': replyClicked, 'role': sender.role, 'chatId': chatId, 'messages': storage}
            return render(request,template_name,context)
        else:
            template_name = "messaging/message.html"
            context = {'messageObjects':messageObjects, 'teacher_id':sender.teacher_id, 'user_name':sender.user_name, 'profile_pic_url':sender.profile_pic.url, 'replyClicked': replyClicked, 'role': sender.role, 'chatId': chatId, 'messages': storage}
            return render(request,template_name,context)