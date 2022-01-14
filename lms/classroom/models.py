from datetime import datetime,timedelta
from django.db import models
#from signUp.models import Teacher, Student, Course
from django.utils import timezone
# Create your models here.

class TermDate(models.Model):
    dateStart = models.DateTimeField('Term started')
    dateEnd = models.DateTimeField('Term ended')


class Resource(models.Model):
    resource = models.FileField(upload_to='resources',blank=True,null=True)
    course = models.ForeignKey('signUp.Course', on_delete=models.CASCADE)
    teacher = models.ForeignKey('signUp.Teacher',on_delete=models.CASCADE)
    pub_date = models.DateTimeField('data published')


class DiscussionId(models.Model):

    def make_discussionId():
        total = DiscussionId.objects.count()
        discussionId = total
        try:
            discussion = DiscussionId.objects.get(discussionId=discussionId)
        except:
            discussion = None
        while discussion != None:
            discussionId = discussionId + 1
            try:
                discussion = DiscussionId.objects.get(discussionId=discussionId)
            except:
                discussion = None
        return discussionId

    discussionId = models.IntegerField(default=make_discussionId,unique=True)


class Discussion(models.Model):
    discussion = models.TextField()
    pub_date = models.DateTimeField('date published')
    student = models.ForeignKey('signUp.Student',on_delete=models.CASCADE,null=True,blank=True)
    teacher = models.ForeignKey('signUp.Teacher', on_delete=models.CASCADE,null=True,blank=True)
    course = models.ForeignKey('signUp.Course', on_delete=models.CASCADE)
    discussionId = models.ForeignKey(DiscussionId,on_delete=models.CASCADE)


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    #quiz = models.FileField(upload_to='quiz')
    teacher = models.ForeignKey('signUp.Teacher', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    course = models.ForeignKey('signUp.Course', on_delete=models.CASCADE)
    exam_date = models.DateField('exam date')
    start_time = models.TimeField('start time')
    time = models.CharField(max_length=200)


class Question(models.Model):
    question = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,null=False)

    def __str__(self):
        return "Question: "+self.question


class Choice(models.Model):
    choice = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    isAnswer = models.BooleanField(default=False)

    def __str__(self):
        if self.isAnswer == False:
            return "Choice: " + self.choice
        else:
            return "Answer: " + self.choice


class Marks(models.Model):
    mark = models.CharField(max_length=200,default="A")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey('signUp.Student', on_delete=models.CASCADE)

    def __str__(self):
        return "Marks: " + str(self.mark)