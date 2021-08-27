from django.db.models import Q, Count
from haystack import indexes

from user_api.models import User
from .models import Post, Course


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='body')  # use_template=True)
    author_name = indexes.CharField(model_attr='author')
    author = indexes.IntegerField(model_attr='author__id')
    posted_at = indexes.DateTimeField(model_attr='posted_at')
    tags = indexes.MultiValueField(model_attr='tags__name', default=[], null=True)
    comments_count = indexes.IntegerField(model_attr='comments_count', null=False)
    likes_count = indexes.IntegerField(model_attr='likes_count')
    idx = indexes.IntegerField(model_attr='id')

    def get_model(self):
        return Post

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().post_comments_likes.all()


class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='title')  # use_template=True)
    posted_at = indexes.DateTimeField(model_attr='posted_at')
    description = indexes.CharField(model_attr='description')
    cost = indexes.IntegerField(model_attr='cost')
    author_name = indexes.CharField(model_attr='author')
    author = indexes.IntegerField(model_attr='author__id')
    tags = indexes.MultiValueField(model_attr='tags__name', default=[], null=True)
    times = indexes.MultiValueField(model_attr='times__time', default=[], null=True)
    address = indexes.CharField(model_attr='address')
    photo = indexes.CharField(model_attr='photo')
    idx = indexes.IntegerField(model_attr='id')

    def get_model(self):
        return Course


class TeachersIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='name')
    name = indexes.CharField(model_attr='name')
    gender = indexes.CharField(model_attr='gender')
    phone = indexes.CharField(model_attr='phone', null=True)
    bio = indexes.CharField(model_attr='bio', null=True)
    address = indexes.CharField(model_attr='address', null=True)
    skills = indexes.MultiValueField(model_attr='skills__name', default=[], null=True)
    avg_rate = indexes.CharField(model_attr='avg_rate', null=True)
    profile_photo = indexes.CharField(model_attr='profile_photo', null=True)
    idx = indexes.IntegerField(model_attr='id')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.annotate(courses_num=Count('courses'), skills_num=Count('skills')) \
            .filter(Q(courses_num__gt=0) | Q(skills_num__gt=0))
