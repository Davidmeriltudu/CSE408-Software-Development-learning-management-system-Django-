from django.contrib import admin
from .models import MessageSS,MessageTT,MessageST,MessageTS
# Register your models here.
admin.site.register(MessageST)
admin.site.register(MessageTS)
admin.site.register(MessageTT)
admin.site.register(MessageSS)
