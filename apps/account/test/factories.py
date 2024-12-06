import factory
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: fake.email())
    username = factory.LazyAttribute(lambda _: fake.user_name())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    password = factory.PostGenerationMethodCall("set_password", "password123321")
    # role = "subscriber"
    is_active = True

    @factory.post_generation
    def activation_code(self, create, extracted, **kwargs):
        self.create_activation_code()

    @staticmethod
    def generate_user_with_valid_data():
        """
        Method for generating user with valid data
        """
        return {
            "email": fake.unique.email(),
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": "password123321",
            "password2": "password123321",
            # "role": "subscriber",
        }

    @staticmethod
    def generate_user_with_duplicate_email(existing_user):
        """
        Method for generating user that already exists
        """
        return {
            "email": existing_user.email,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": "password123321",
            "password2": "password123321",
        }

    @staticmethod
    def generate_user_with_missing_fields(missing_fields={"email"}):
        """
        Method for generating user with missing field
        """
        data = {
            "email": fake.unique.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "password": "password123321",
            "password2": "password123321",
        }
        for missing_field in missing_fields:
            if missing_field in data:
                data.pop(missing_field)
        return data

    @staticmethod
    def generate_user_with_invalid_email():
        """
        Method for generating invalid email
        """
        return {
            "email": "invalid_email",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "passwod": "password123",
            "passwod2": "password123",
        }
