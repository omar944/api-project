from django.db import models
from django.db.models import Count

from user_api.models import User


class PostCommentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(comments_count=Count('comments'), likes_count=Count('likes'))


class Post(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=500)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='post_tags', blank=True)

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def likes_count(self):
        return self.likes.count()

    # Query managers
    # objects = models.Manager()  # The default manager.
    # post_comments_likes = PostCommentsManager()  # Manager to get comments num with posts

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    author = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.name
