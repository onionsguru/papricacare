from django.contrib import admin

# Register your models here.
from chat import models

admin.site.register(models.User)
admin.site.register(models.Chatroom)