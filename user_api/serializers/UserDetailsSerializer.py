from collections import OrderedDict

from rest_framework import serializers

from drf_haystack.serializers import HaystackSerializer

from api.search_indexes import TeachersIndex
from api.serializers import CourseSerializer
from user_api.models import User, Skill


class SlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')


class UserDetailsSerializer(serializers.ModelSerializer):
    skills = SlugRelatedField(many=True, slug_field='name', queryset=Skill.objects.all(), required=False)
    courses_num = serializers.IntegerField(read_only=True)
    skills_num = serializers.IntegerField(read_only=True)
    courses = CourseSerializer(many=True, read_only=True)
    avg_rate = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'name',
            'email',
            'phone',
            'gender',
            'address',
            'birth_date',
            'bio',
            'profile_photo',
            'avg_rate',
            'courses_num',
            'skills_num',
            'courses',
            'skills',
        )

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if self.ok(result[key])])

    # noinspection PyMethodMayBeStatic
    def ok(self, s):
        if type(s) is list:
            return len(s) > 0
        if s == "":
            return False
        return s is not None


class TeacherSerializer(serializers.ModelSerializer):
    skills = SlugRelatedField(many=True, slug_field='name', read_only=True)
    skills_num = serializers.IntegerField(read_only=True)
    avg_rate = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'name',
            'address',
            'profile_photo',
            'skills_num',
            'skills',
            'avg_rate',
            'birth_date',
        )

    def to_representation(self, instance):
        result = super().to_representation(instance)

        return OrderedDict([(key, result[key]) for key in result if self.ok(result[key])])

    # noinspection PyMethodMayBeStatic
    def ok(self, s):
        if type(s) is list:
            return len(s) > 0
        if s == "":
            return False
        return s is not None


# noinspection PyAbstractClass,PyMethodMayBeStatic
class TeacherSearchSerializer(HaystackSerializer):

    pk = serializers.SerializerMethodField()

    def get_pk(self, obj):
        return obj.idx

    class Meta:
        index_classes = [TeachersIndex]

        fields = [
            'pk',
            'text',
            'gender',
            'phone'
            'username',
            'birth_date',
            'skills',
            'bio',
            'address',
            'avg_rate',
            'profile_photo',
        ]
        read_only_fields = '__all__'

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['name'] = result['text']
        result.pop('text')

        if result.get('profile_photo'):
            request = self.context.get("request")
            result['profile_photo'] = 'http://' + request.get_host() + '/media/' + (result['profile_photo'])

        return OrderedDict([(key, result[key]) for key in result if self.ok(result[key])])

    # noinspection PyMethodMayBeStatic
    def ok(self, s):
        if type(s) is list:
            return len(s) > 0
        if s == "":
            return False
        return s is not None
