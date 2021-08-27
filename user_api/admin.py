from django.contrib import admin

from .models import UserRating, User, Skill

admin.site.register(UserRating)
admin.site.register(User)
admin.site.register(Skill)
