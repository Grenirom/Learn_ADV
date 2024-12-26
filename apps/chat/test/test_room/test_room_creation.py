from apps.chat.test.test_room.test_base_class import ChatAPITest


# ToDo successful create, duplicate name
class RoomCreateTest(ChatAPITest):

    def test_successful_create(self):
        self.client.force_authenticate(self.default_user_data)
        response = self.client.post(self.room_create_url, self.default_room_data)

        self.assertEqual(response.status_code, 201)