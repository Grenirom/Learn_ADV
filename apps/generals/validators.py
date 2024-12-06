from rest_framework.exceptions import ValidationError


class UserIsActiveVallidator:
    def __init__(self, user):
        self.user = user

    def validate(self):
        if not self.user.is_active:
            raise ValidationError("No active user found with given credentials")
