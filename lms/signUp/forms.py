#from .models import Student,Teacher,Course,UserNames
#from django import forms
from .validators import validation_domain_email
from django.core.exceptions import ValidationError
from .models import Student,Teacher,UserNames
from classroom.models import *
from django import forms


class SignUpStudent(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField(widget=forms.Textarea,required=False)
    email = forms.EmailField(validators=[validation_domain_email])
    password = forms.CharField(widget=forms.PasswordInput)
    conf_password = forms.CharField(widget=forms.PasswordInput)
    user_name = forms.CharField()

    class Meta:
        model = Student
        fields = ('first_name','last_name','email','password','conf_password','user_name','address')

    def clean_conf_password(self):
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']
        if password != conf_password:
            raise forms.ValidationError("Passwords does not match")
        return conf_password

    # def clean_user_name(self):
    #     user_name = self.cleaned_data['user_name']
    #     count = Student.objects.filter(user_name=user_name).count()
    #     if count:
    #         raise forms.ValidationError("This user_name is already used")
    #     return user_name


class SignUpTeacher(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField(widget=forms.Textarea,required=False)
    email = forms.EmailField(validators=[validation_domain_email])
    password = forms.CharField(widget=forms.PasswordInput)
    conf_password = forms.CharField(widget=forms.PasswordInput)
    user_name = forms.CharField()

    class Meta:
        model = Teacher
        fields = ('first_name','last_name','email','password','conf_password','user_name','address')

    def clean_conf_password(self):
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']
        if password != conf_password:
            raise forms.ValidationError("Passwords does not match")
        return conf_password

    # def clean_user_name(self):
    #     user_name = self.cleaned_data['user_name']
    #     count = Teacher.objects.filter(user_name=user_name).count()
    #     if count:
    #         raise forms.ValidationError("This user_name is already used")
    #     return user_name


class Login(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfilePic(forms.ModelForm):
    profile_pic = forms.ImageField(label='')

    class Meta:
        model = Student
        fields = ('profile_pic',)


class EditProfile(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    address = forms.CharField(required=False)
    class Meta:
        model = Student
        fields = ('first_name','last_name','email','address',)

