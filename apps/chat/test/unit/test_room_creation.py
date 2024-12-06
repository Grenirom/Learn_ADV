import pytest
from django.db import IntegrityError

from rest_framework.test import APIClient

from apps.chat.models import Room
from apps.chat.test.factories.factory_user import UserChatFactory, RoomFactory


class TestRoom:

    @pytest.fixture
    def user(self):
        return UserChatFactory.create()

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def room_data(self, user):
        return RoomFactory.create()

    def test_successful_room_create(self, user, client, room_data):
        client.force_authenticate(user=user)

        room = Room.objects.create(**room_data)

        room_db = Room.objects.filter(name='TestRoom')

        assert room_db is not None
        assert room.name == "TestRoom"
        assert room.host == user

    def test_non_unique_room_name(self, user, client, room_data):
        room = Room.objects.create(**room_data)

        with pytest.raises(IntegrityError):
            Room.objects.create(**room_data)

