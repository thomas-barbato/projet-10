"""import """
from django.contrib.auth.password_validation import validate_password
import re
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Users, Projects, Issues, Comments
from .validators.check_data import CheckPasswordPolicy


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["user_id", "email"]


class LoginUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Users
        fields = ["email", "password"]


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Users
        fields = ["email", "password", "password2", "first_name", "last_name"]

    def save(self):
        user = Users(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        CheckPasswordPolicy().validate(password=password, password2=password2)
        user.set_password(password)
        user.save()
        return user
