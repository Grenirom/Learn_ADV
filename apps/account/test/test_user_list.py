# from apps.account.test.factories import UserFactory
# from apps.account.test.test_base_class import AccountAPITest
#
#
# class AccountListTests(AccountAPITest):
#     def test_users_get(self):
#         self.users = UserFactory.create_batch(10)
#
#         response = self.client.get(self.user_list_url)
#         print(response.data)
#         print(response.status_code)
#         self.assertEqual(response.status_code, 200)
#
#         expected_keys = {
#             "email",
#             "username",
#             "first_name",
#             "last_name",
#             # "role",
#             "is_active",
#         }
#
#         for user_data in response.data:
#             self.assertTrue(
#                 expected_keys.issubset(user_data.keys()), f"missing key in {user_data}"
#             )
