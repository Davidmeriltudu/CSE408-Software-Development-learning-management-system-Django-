from django.db import models
from signUp.models import Teacher, Student
# Create your models here.

class Chat(models.Model):

    def make_chatId():
        total = Chat.objects.count()
        chatId = total
        try:
            chat = Chat.objects.get(chatId=chatId)
        except:
            chat = None
        while chat != None:
            chatId = chatId + 1
            try:
                chat = Chat.objects.get(chatId=chatId)
            except:
                chat = None
        return chatId

    chatId = models.IntegerField(default=make_chatId,unique=True)


class MessageST(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(Student,related_name="sendersST", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Teacher,related_name="receiversST", on_delete=models.CASCADE)
    # parentMessageST = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # parentMessageTS = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # replyMessageST = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # replyMessageTS = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField("date sent")
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)


class MessageTS(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(Teacher, related_name="sendersTS", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Student, related_name="receiversTS", on_delete=models.CASCADE)
    # parentMessageST = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # parentMessageTS = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # replyMessageST = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # replyMessageTS = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField("date sent")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class MessageSS(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(Student, related_name="sendersSS", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Student, related_name="receiversSS", on_delete=models.CASCADE)
    # parentMessage = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # replyMessage = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField("date sent")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class MessageTT(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(Teacher, related_name="sendersTT", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Teacher, related_name="receiversTT", on_delete=models.CASCADE)
    # parentMessage = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    # replyMessage = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField("date sent")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
