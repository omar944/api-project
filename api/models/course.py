import os

from django.db import models
from django.utils import timezone

from user_api.models import User


def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"course_photos/{instance.pk}/{now:%d%m%Y%H%M%S}{extension}"


class Course(models.Model):
    title = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500)
    cost = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField('Tag', related_name='course_tags', blank=True)
    photo = models.ImageField(upload_to=upload_to, null=True, blank=True)
    address = models.CharField(max_length=100, blank=True)
    times = models.ManyToManyField('CourseTime', related_name='times', blank=True)

    def __str__(self):
        return self.title


class CourseTime(models.Model):
    time = models.CharField(max_length=100)

    def __str__(self):
        return self.time


class ViewedCourses(models.Model):
    author = models.ForeignKey(User, related_name='viewed_courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course', on_delete=models.CASCADE)

    def __str__(self):
        return self.course.title

# RATE_SELECTION = [(1, '1-star'), (2, '2-stars'), (3, '3-stars'), (4, '4-stars'), (5, '5-stars')]
# class CourseRating(models.Model):
#     rate = models.IntegerField(choices=RATE_SELECTION)
#     message = models.CharField(max_length=100)
#     course = models.ForeignKey(Course, related_name='rate', on_delete=models.CASCADE)
