import random

from knox.crypto import hash_token
from knox.models import AuthToken
from rest_framework.response import Response


def generate_reset_password_code():
    return str(random.randint(100000, 999999))


def custom_lockout_message(request, credentials):
    return "Your account locked for 5 minutes due to multiple login attempts."


def health(request):
    return Response({"msg": "ok"})


def authenticate_token(raw_token):
    """
    Method for finding user via knox token
    """
    try:
        digest = hash_token(raw_token)
        token_instance = AuthToken.objects.get(digest=digest)
        return token_instance, token_instance.user
    except AuthToken.DoesNotExist:
        raise ValueError("Invalid token")
