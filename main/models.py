from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your models here.

class Rating(models.Model):
    rating = models.CharField(max_length=10)
    description = models.CharField(max_length=50, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.rating

class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    display_name = models.CharField(max_length=100, null=True, blank=True)
    parent=models.ForeignKey('self', null=True, blank=True, related_name='child')
    rating_limit = models.ForeignKey(Rating, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos', null=True, blank=True, max_length=500)

    def __str__(self):
        return str(self.user)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return static('main/theme_color_4/images/smiley-face-emoticon-avatar-brand.png')

class Program(models.Model):
    name = models.CharField(max_length=500)
    guidebox_id = models.IntegerField()
    rating = models.ForeignKey(Rating)
    runtime = models.IntegerField()
    thumbnail = models.ImageField(upload_to='program_thumbnails', null=True, blank=True, max_length=500)
    banner = models.ImageField(upload_to='program_banners', null=True, blank=True, max_length=500)
    overview = models.TextField()
    review = models.TextField()
    positive_message = models.TextField()
    positive_role_model = models.TextField()
    violence = models.TextField()
    sex = models.TextField()
    language = models.TextField()
    consumerism = models.TextField()
    substance = models.TextField()

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return "http://www.clker.com/cliparts/f/Z/G/4/h/Q/no-image-available-md.png"
    def banner_url(self):
        if self.banner:
            return self.banner.url
        return "http://www.clker.com/cliparts/f/Z/G/4/h/Q/no-image-available-md.png"

    def __str__(self):
        return self.name

class Queue(models.Model):
    user = models.OneToOneField('auth.User')

    def __str__(self):
        return str(self.user)

class QueueProgram(models.Model):  #thru table between queue and program
    queue = models.ForeignKey(Queue)
    program = models.ForeignKey(Program)
    network = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.program)

class FamilyQueue(models.Model):
    user = models.ManyToManyField(User)

    def get_random_program(self):
        rating_limit_list = []
        for user in self.user.all():
            if user.profile.rating_limit:
                rating_limit_list.append(user.profile.rating_limit.id)
                rating_limit_list.sort()
        if rating_limit_list:
            rating_limit = rating_limit_list[0]
            rating_limit_name = Rating.objects.get(id=rating_limit)
        else:
            rating = Rating.objects.last()
            rating_limit = rating.id
            rating_limit_name = Rating.objects.last()

        program_list = []
        for user in self.user.all():
            for program in user.queue.queueprogram_set.all():
                if program.program.rating.id <= rating_limit:
                    program_list.append(program)
            return (program_list, rating_limit_name)

    @property
    def displayed_name(self):
        for profile in self.profile_set.all():
            if profile.display_name:
                return profile.display_name
            else:
                return self.user



@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get("created")
    instance = kwargs.get("instance")
    if created:
        Profile.objects.create(user=instance)
        Queue.objects.create(user=instance)
