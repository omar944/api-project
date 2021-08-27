from collections import OrderedDict

from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from api.models import Post, Comment, Tag
from .fields import SlugRelatedField
from ..search_indexes import PostIndex


class PostReadSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    tags = SlugRelatedField(many=True, read_only=True, slug_field='name')
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'posted_at', 'body', 'author',
                  'author_name', 'likes_count', 'comments_count', 'tags', 'profile_photo')

    def get_profile_photo(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.author.profile_photo.url) if obj.author.profile_photo else None

    def to_representation(self, instance):
        timestamp = instance.posted_at.timestamp()
        result = super().to_representation(instance)
        result['posted_at'] = float(timestamp)
        return OrderedDict([(key, result[key]) for key in result if self.ok(result[key])])

    # noinspection PyMethodMayBeStatic
    def ok(self, s):
        if s is list:
            return len(s) > 0
        if s == "":
            return False
        return s is not None


class PostWriteSerializer(serializers.ModelSerializer):
    tags = SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ('id', 'posted_at', 'body', 'tags')


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name', required=False)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post_id', 'text', 'author_name')

    def to_representation(self, instance):
        timestamp = instance.posted_at.timestamp()
        result = super().to_representation(instance)
        result['posted_at'] = float(timestamp)
        return result


# noinspection PyAbstractClass,PyMethodMayBeStatic
class PostSearchSerializer(HaystackSerializer):
    id = serializers.SerializerMethodField()

    # body = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.idx

    # def get_body(self, obj):
    #     return obj.text

    class Meta:
        index_classes = [PostIndex]

        fields = [
            'id', 'body', 'author', 'author_name',
            'posted_at', 'text', 'tags', 'likes_count', 'comments_count',
        ]

    def to_representation(self, instance):
        timestamp = instance.posted_at.timestamp()
        result = super().to_representation(instance)
        result['posted_at'] = float(timestamp)
        result['body'] = result['text']
        result.pop('text')
        return OrderedDict([(key, result[key]) for key in result if self.ok(result[key])])

    # noinspection PyMethodMayBeStatic
    def ok(self, s):
        if s is list:
            return len(s) > 0
        if s == "":
            return False
        return s is not None


# noinspection PyAbstractClass
class LikeField(serializers.RelatedField):
    def to_representation(self, value):
        return value.author.id


class LikeSerializer(serializers.ModelSerializer):
    likes = LikeField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['likes']
