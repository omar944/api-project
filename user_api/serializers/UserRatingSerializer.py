from rest_framework import serializers

from user_api.models import UserRating


class UserRatingSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    rated_user_name = serializers.ReadOnlyField(source='rated_user.username')

    class Meta:
        model = UserRating
        fields = ('rated_user', 'rated_user_name', 'author', 'author_name', 'rate', 'message')
