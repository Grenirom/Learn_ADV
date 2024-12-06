import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from apps.account.managers import CustomManager


class CustomUser(AbstractUser):
    ROLE_CHOICES = (("subscriber", "Подписчик"), ("author", "Автор"))

    email = models.EmailField(unique=True)
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    # role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="subscriber")

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code
        return self.activation_code


class UserResetPasswordToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, validators=[MinValueValidator(6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return f"{self.token}"
