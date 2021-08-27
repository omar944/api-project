from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from rest_framework import serializers

from user_api.models import GENDER_SELECTION
from user_api.models import User


class UserRegisterSerializer(RegisterSerializer):

    phone = serializers.CharField(max_length=30, required=False)
    birth_date = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    address = serializers.CharField(max_length=100, required=False)
    name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = (
            'name',
            'email',
            'password1',
            'password2',
            'phone',
            'gender',
            'birth_date',
        )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.gender = self.data.get('gender')
        user.birth_date = self.data.get('birth_date')
        user.phone = self.data.get('phone')
        user.name = self.data.get('name')
        user.save()
        return user
