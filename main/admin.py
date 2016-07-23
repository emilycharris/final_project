from django.contrib import admin
from main.models import Rating, Profile, Program, Queue, QueueProgram

# Register your models here.

admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Program)
admin.site.register(Queue)
admin.site.register(QueueProgram)
