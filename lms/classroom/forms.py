#from .models import Student,Teacher,Course,UserNames
#from django import forms
from django.core.exceptions import ValidationError
from signUp.models import Student,Teacher,UserNames
from classroom.models import *
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class ResourceForm(forms.ModelForm):
    resource = forms.FileField(label='')

    class Meta:
        model = Resource
        fields = ('resource',)


class DiscussionForm(forms.Form):
    discussion = forms.CharField(widget=forms.Textarea,required=False)


class ReplyForm(forms.Form):
    discussion = forms.CharField(widget=forms.Textarea,required=False)


class QuizInformationForm(forms.Form):
    name = forms.CharField(required=False)
    exam_date = forms.DateField(required=False,input_formats=['%d-%m-%Y'])
    start_time = forms.TimeField(required=False,input_formats=['%H:%M'])
    time = forms.CharField(required=False)


class MakingQuizForm(forms.Form):
    question = forms.CharField(required=False)
    choice1 = forms.CharField(required=False)
    choice2 = forms.CharField(required=False)
    choice3 = forms.CharField(required=False)
    choice4 = forms.CharField(required=False)
    answer = forms.IntegerField(required=False,validators=[MaxValueValidator(4),MinValueValidator(1)])


class QuizAnswerForm(forms.Form):
    choice = forms.ChoiceField(label="",widget=forms.RadioSelect(),required=False)