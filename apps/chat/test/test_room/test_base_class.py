from django.urls import reverse

from rest_framework.test import APITestCase

from apps.account.test.factories import UserFactory
from apps.chat.models import Room


class ChatAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.room_create_url = reverse('room-list')

        cls.default_user_data = UserFactory.create()
        cls.default_current_users_data = UserFactory.create_batch(4)
        cls.default_room_data = {
            'name': 'test room',
            'host': cls.default_user_data,
            'current_users': [cls.default_current_users_data]
        }
