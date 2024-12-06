from rest_framework import serializers

from django.contrib.auth import get_user_model

from apps.account.models import CustomUser
from apps.generals.backends import EmailBackend
from apps.generals.validators import UserIsActiveVallidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            # "role",
            "username",
            "is_active",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.pop("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords didn't match")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer, EmailBackend):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User not found")

        user = self.authenticate(
            request=self.context.get("request"), email=email, password=password
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        is_active_validator = UserIsActiveVallidator(user)
        is_active_validator.validate()
        attrs["user"] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExists:
            raise serializers.ValidationError({"msg": "User not found"})

        is_active_validator = UserIsActiveVallidator(user)
        is_active_validator.validate()
        return attrs


class ConfirmPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password_confirm = serializers.CharField(
        min_length=8, write_only=True, required=True
    )
    code = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        p1 = attrs.get("password")
        p2 = attrs.pop("password_confirm")

        if p1 != p2:
            raise serializers.ValidationError("Passwords didn't match")
        return attrs
