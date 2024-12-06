from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status

from apps.account.test.factories import UserFactory
from apps.account.test.test_base_class import AccountAPITest
from apps.account.tasks import send_activation_email_task

User = get_user_model()


class RegistrationTests(AccountAPITest):
    @patch("apps.account.tasks.send_activation_email_task.apply_async")
    def test_successful_registration(self, mock_send_mail):
        user_data = UserFactory.generate_user_with_valid_data()
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(
            response.data["user"]["email"], user_data["email"], "email didn't match"
        )

        current_user = User.objects.get(email=user_data["email"])
        self.assertNotEqual(current_user.password, user_data["password"])
        self.assertIsNotNone(current_user)
        self.assertFalse(current_user.is_active)

    def test_registration_missing_fields(self):
        missing_fields = {"email", "last_name", "first_name", "password"}
        data_with_missing_fields = UserFactory.generate_user_with_missing_fields(
            missing_fields
        )

        response = self.client.post(self.register_url, data_with_missing_fields)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            missing_fields.issubset(response.data.keys()),
            "some missing fields are not present in response.data, "
            "please check <response.data>",
        )

    def test_registration_invalid_email(self):
        user_with_invalid_email = UserFactory.generate_user_with_invalid_email()
        response = self.client.post(self.register_url, user_with_invalid_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_email(self):
        response = self.client.post(self.register_url, self.default_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    @patch("apps.account.tasks.send_activation_email_task.apply_async")
    def test_send_activation_email(self, mock_send_mail):
        send_activation_email_task.delay("test-user@gmail.com", "test-code")
        mock_send_mail.assert_called_once()
