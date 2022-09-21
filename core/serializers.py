from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=6, write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField()
    username = serializers.CharField(min_length=3, unique=True, write_only=True)

    class Meta:
        model = User
        read_only_fields = ["id"]
        fields = ["id", "username", "first_name", "last_name", "email", "password", "password_repeat"]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, data):
        password = data.get("password")
        password_repeat = data.pop("password_repeat", None)
        if password != password_repeat:
            raise ValidationError("Пароли не совпадают!")
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ["id"]
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=6, write_only=True)
    password = serializers.CharField(min_length=3, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Неверное имя пользователя или пароль!")
        data["user"] = user
        return data


class UpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        read_only_fields = ["id"]
        fields = ["old_password", "new_password"]

    def validate(self, data):
        old_password = data.get("old_password")
        user: User = self.instance
        if not user.check_password(old_password):
            raise ValidationError("Указан неверный старый пароль")
        return data

    def update(self, instance, validated_data):
        if instance.check_password(validated_data["old_password"]):
            instance.set_password(validated_data["new_password"])
            instance.save()
            return instance
        else:
            raise ValidationError("Указан неверный старый пароль")
    