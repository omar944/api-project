import os

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"profile_photos/{instance.pk}/{now:%d%m%Y%H%M%S}{extension}"


GENDER_SELECTION = [('M', 'Male'), ('F', 'Female')]


class Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().\
            annotate(x=Avg('rated'))


class User(AbstractUser):
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION)
    phone = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to=upload_to, null=True, blank=True)
    name = models.CharField(max_length=20, default="")
    skills = models.ManyToManyField(Skill, related_name='skills', blank=True)
    username = models.CharField(max_length=150, unique=True, blank=True)

    @property
    def avg_rate(self):
        return self.rated.aggregate(avg_rate=Avg('rate'))['avg_rate']

    def __str__(self):
        return self.name if self.name != "" else super().username


RATE_SELECTION = [(1, '1-star'), (2, '2-stars'), (3, '3-stars'), (4, '4-stars'), (5, '5-stars')]


class UserRating(models.Model):
    rate = models.IntegerField(choices=RATE_SELECTION)
    message = models.CharField(max_length=100, blank=True)
    rated_user = models.ForeignKey(User, related_name='rated', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='rate', on_delete=models.CASCADE)

    def __str__(self):
        return "{} by {}".format(self.rated_user, self.author)
