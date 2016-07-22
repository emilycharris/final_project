from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Rating(models.Model):
    rating = models.CharField(max_length=10)
    description = models.CharField(max_length=50, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.rating



class Profile(models.Model):
    user = models.ForeignKey('auth.User')
    parent=models.ForeignKey('self', null=True, blank=True, related_name='child')
    rating_limit = models.ForeignKey(Rating)
    email = models.EmailField()

class Program(models.Model):
    name = models.CharField(max_length=100)
    guidebox_id = models.IntegerField()
    rating = models.ForeignKey(Rating)
    runtime = models.IntegerField()
    thumbnail = models.ImageField(upload_to='program_thumbnails', null=True, blank=True)
    banner = models.ImageField(upload_to='program_banners', null=True, blank=True)
    overview = models.TextField()
    review = models.TextField()
    positive_message = models.TextField()
    positive_role_model = models.TextField()
    violence = models.TextField()
    sex = models.TextField()
    language = models.TextField()
    consumerism = models.TextField()
    substance = models.TextField()

    def __str__(self):
        return self.name


class Queue(models.Model):
    user = models.ForeignKey('auth.User')
    program = models.ForeignKey(Program)
    network = models.CharField(max_length=100)
