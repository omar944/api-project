from collections import OrderedDict

from rest_framework import serializers

from api.models import Course


class TeacherCoursesSerializer(serializers.ModelSerializer):
    # author_name = serializers.ReadOnlyField(source='author.name')

    class Meta:
        model = Course
        fields = ('id', 'photo', 'title')
        read_only = '__all__'

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])