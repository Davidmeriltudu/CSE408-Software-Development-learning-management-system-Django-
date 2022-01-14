from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Resource)
admin.site.register(TermDate)
admin.site.register(Discussion)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Marks)