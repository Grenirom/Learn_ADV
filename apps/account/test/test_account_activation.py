from rest_framework import status

from apps.account.test.test_base_class import AccountAPITest


class AccountActivationTests(AccountAPITest):
    def test_successful_account_activation(self):
        url_for_activation = (
            f"{self.activate_url}?u={self.inactive_user.activation_code}"
        )

        response = self.client.get(url_for_activation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["msg"], "Successfully activated your account!")

        self.inactive_user.refresh_from_db()
        self.assertTrue(self.inactive_user.is_active)
        self.assertEqual(self.inactive_user.activation_code, "")

    def test_invalid_activation_code(self):
        url_for_activation = f"{self.activate_url}?u=invalid_code"

        response = self.client.get(url_for_activation)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
