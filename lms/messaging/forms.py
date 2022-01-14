from django.core.exceptions import ValidationError
from .models import Student,Teacher
from django import forms


class MessageForm(forms.Form):
    user_name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea, required=False)

class ReplyForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea,required=False)