import factory

from faker import Faker

from django.contrib.auth import get_user_model

from apps.account.test.factories import UserFactory
from apps.chat.models import Room

User = get_user_model()

fake = Faker()

class UserChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    password = factory.PostGenerationMethodCall('set_password', 'password123321')
    # ToDo подумать о том, есть ли смысл писать новую фабрику для пользователей, или можно использовать фабрику в account


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.LazyAttribute(lambda _: fake.name())
    host = factory.SubFactory(UserFactory.create())
    current_users = factory.RelatedFactoryList(UserFactory, 'rooms', size=3)
