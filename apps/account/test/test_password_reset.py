from datetime import timedelta
from http.client import responses
from unittest.mock import patch

from django.utils.timezone import now
from rest_framework import status

from apps.account.models import UserResetPasswordToken
from apps.account.test.factories import UserFactory
from apps.account.test.test_base_class import AccountAPITest


class AccountResetPasswordTests(AccountAPITest):

    @patch("apps.account.tasks.send_password_reset_email_task.apply_async")
    def test_successful_reset_password(self, mock_send_mail):
        email_data = {"email": self.active_user.email}
        response = self.client.post(self.reset_password_url, email_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "Вам на почту отправлено сообщение с инструкцией по сбросу пароля",
            response.data,
        )

    def test_invalid_email_reset_password(self):
        invalid_email_data = UserFactory.generate_user_with_invalid_email()
        response = self.client.post(self.reset_password_url, invalid_email_data)
        self.assertIn("email", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # ToDo проверка на активность пользователя и возвращаемую ошибку

    def test_successful_reset_password_confirm(self):
        data = self.generate_reset_password_data(self.active_user)
        response = self.client.post(self.confirm_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("msg", response.data)

        self.active_user.refresh_from_db()
        self.assertTrue(self.active_user.check_password(data["password"]))

        with self.assertRaises(
            UserResetPasswordToken.DoesNotExist
        ):  # Checking if the UserResetPasswordToken deletes after success
            UserResetPasswordToken.objects.get(token=data["code"])

        response = self.client.post(self.confirm_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid code", response.data)

    def test_invalid_reset_password_code(self):
        data = self.generate_reset_password_data(self.active_user)
        data["code"] = "119"
        response = self.client.post(self.confirm_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid code", response.data)

    def test_reset_expired_code(self):
        data = self.generate_reset_password_data(self.active_user)
        reset_token = UserResetPasswordToken.objects.get(user=self.active_user)
        reset_token.created_at = now() - timedelta(minutes=11)
        reset_token.save()

        response = self.client.post(self.confirm_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(reset_token.is_valid())
        self.assertIn("error", response.data)
        self.assertFalse(self.active_user.check_password(data["password"]))

    def test_different_passwords(self):
        data = self.generate_reset_password_data(self.active_user)
        data["password_confirm"] = "invalid_password"
        response = self.client.post(self.confirm_reset_url, data)

        self.assertIn("Passwords didn't match", response.data.get("non_field_errors"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
