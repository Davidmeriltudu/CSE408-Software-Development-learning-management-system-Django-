from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Student, Teacher, Course

domain_names = ['gmail.com','yahoo.com','hotmail.com', 'outlook.com']


def validation_domain_email(value):
    words = value.split("@")
    if not words[1] in domain_names:
        raise ValidationError(_("Sorry, this is not a valid email address"))
    return value

#
# def validation_student_email(value):
#     count = Student.objects.filter(email=value).count()
#     if count:
#         raise ValidationError(_("This email is already used"))
#     return value