from django.contrib import admin
from main.models import Rating, Profile, Program, Queue

# Register your models here.

admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(Program)
admin.site.register(Queue)
