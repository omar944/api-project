from collections import OrderedDict

from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from api.models import Course, Tag, CourseTime
from .fields import SlugRelatedField
from ..search_indexes import CourseIndex


class CourseSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    profile_photo = serializers.SerializerMethodField()
    tags = SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all(), required=False)
    times = SlugRelatedField(many=True, slug_field='time', queryset=CourseTime.objects.all(), required=False)

    class Meta:
        model = Course
        fields = ('id', 'author_name', 'author', 'profile_photo',
                  'photo', 'title', 'description',
                  'cost', 'posted_at', 'tags',
                  'address', 'times')

    def get_profile_photo(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.author.profile_photo.url) if obj.author.profile_photo else None

    def to_representation(self, instance):
        timestamp = instance.posted_at.timestamp()
        result = super().to_representation(instance)
        result['posted_at'] = float(timestamp)
        return OrderedDict([(key, result[key]) for key in result if self.ok(result[key])])

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)
        instance = super().create(validated_data)
        instance.save()
        instance.photo = photo
        instance.save()
        return instance

    # noinspection PyMethodMayBeStatic
    def ok(self, s):
        if s is list:
            return len(s) > 0
        if s == "":
            return False
        return s is not None


# noinspection PyAbstractClass,PyMethodMayBeStatic
class CourseSearchSerializer(HaystackSerializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.idx

    def get_title(self, obj):
        return obj.text

    class Meta:
        index_classes = [CourseIndex]
        fields = [
            'id',
            'text', 'description', 'posted_at',
            'cost', 'author', 'author_name',
            'address', 'tags', 'times',
            'photo',
        ]

    def to_representation(self, instance):
        request = self.context.get("request")
        timestamp = instance.posted_at.timestamp()
        result = super().to_representation(instance)
        result['posted_at'] = float(timestamp)
        result['title'] = result['text']
        result.pop('text')
        if result.get('photo'):
            result['photo'] = 'http://' + request.get_host() + '/media/' + (result['photo'])
        return OrderedDict([(key, result[key]) for key in result if self.ok(result[key])])

    def ok(self, s):
        if s is list:
            return len(s) > 0
        if s == "":
            return False
        return s is not None
