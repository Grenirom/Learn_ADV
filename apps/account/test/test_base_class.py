from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from unittest.mock import patch

from rest_framework.test import APITestCase

from apps.account.test.factories import UserFactory
from apps.account.models import UserResetPasswordToken
from apps.generals.utils import generate_reset_password_code

User = get_user_model()


class AccountAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.register_url = reverse("account-register-v1")
        cls.activate_url = reverse("activation-account-v1")
        cls.reset_password_url = reverse("reset-password-request-v1")
        cls.confirm_reset_url = reverse("password-reset-confirm-v1")
        cls.login_url = reverse("login-v1")
        cls.logout_url = reverse("logout-v1")
        cls.logout_all_url = reverse("logout-all-v1")
        cls.user_list_url = reverse("users_v1")

        cls.default_user_data = {
            "email": "test@gmail.com",
            "first_name": "nika",
            "last_name": "grebnev",
            "password": "password123321",
            "password2": "password123321",
        }
        cls.user_with_existing_email = {
            "email": "nikitagrebnev311@gmail.com",
            "first_name": "nika",
            "last_name": "grebnev",
            "password": "password123321",
            "password2": "password123321",
        }
        cls.active_user = UserFactory.create()
        cls.inactive_user = UserFactory.create(is_active=False)

    @patch("apps.account.tasks.send_activation_email_task.apply_async")
    def setUp(self, mock_send_mail):

        self.client.post(self.register_url, self.default_user_data)
        self.user = User.objects.get(email=self.default_user_data["email"])

        self.activation_code = self.user.activation_code

    def generate_reset_password_data(self, user):
        """
        Additional method for generating registered user with reset code
        """
        reset_code = UserResetPasswordToken.objects.create(
            user=user,
            token=generate_reset_password_code(),
            created_at=timezone.now(),
        )
        return {
            "password": "new_password123",
            "password_confirm": "new_password123",
            "code": reset_code,
        }
