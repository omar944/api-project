from django.contrib import admin

from .models import Post, Comment, Course, Tag, Like, ViewedCourses

admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(ViewedCourses)
