from rest_framework import status

from apps.account.test.test_base_class import AccountAPITest


class AccountLoginTests(AccountAPITest):
    def test_login_successful(self):
        required_fields_in_data = {"token", "user"}

        login_data = {"email": self.active_user.email, "password": "password123321"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(required_fields_in_data.issubset(response.data.keys()))
        # ToDo Test Cases: Invalid login data

    def test_successful_login_after_password_change(self):
        reset_password_data = self.generate_reset_password_data(self.active_user)
        response = self.client.post(self.confirm_reset_url, reset_password_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_data = {
            "email": self.active_user.email,
            "password": reset_password_data["password"],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
