from axes.handlers.proxy import AxesProxyHandler

from knox.views import LoginView as KnoxLoginView

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404

from apps.account.models import UserResetPasswordToken
from apps.account.serializers_v1 import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ResetPasswordSerializer,
    ConfirmPasswordResetSerializer,
)
from apps.account.tasks import (
    send_activation_email_task,
    send_password_reset_email_task,
)
from apps.generals.utils import generate_reset_password_code, custom_lockout_message

User = get_user_model()


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_activation_email_task.delay(
                    email=user.email, code=user.activation_code
                )
            except Exception as e:
                return Response({"msg": "Something went wrong!"})
        return Response({"user": serializer.data}, status=201)


class ActivationView(APIView):
    def get(self, request):
        activation_code = request.query_params.get("u")
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ""
        user.save()
        return Response({"msg": "Successfully activated your account!"}, status=200)


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        email = request.data.get("email")
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if AxesProxyHandler.is_locked(request, credentials={"email": email}):
            message = custom_lockout_message(request, {"email": email})
            return Response(
                {
                    "detail": message,
                },
                status=403,
            )

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user, backend="apps.generals.backends.EmailBackend")
            response = super().post(request, format=None)
        else:
            return Response({"errors": serializer.errors}, status=400)

        return Response(response.data, status=200)


class PasswordResetView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("Такого пользователя не существует", 404)

        reset_code = generate_reset_password_code()
        UserResetPasswordToken.objects.create(user=user, token=reset_code)
        send_password_reset_email_task.delay(email=email, reset_code=reset_code)
        return Response(
            "Вам на почту отправлено сообщение с инструкцией по сбросу пароля", 200
        )


class ConfirmPasswordResetView(APIView):
    serializer_class = ConfirmPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = request.data.get("code")
        password = request.data.get("password")

        try:
            reset_code = UserResetPasswordToken.objects.get(token=code)
        except UserResetPasswordToken.DoesNotExist:
            return Response("Invalid code", 400)

        if not reset_code.is_valid():
            return Response({"error": "Code expired"}, status=400)

        user = reset_code.user
        user.set_password(password)
        user.save()

        reset_code.delete()
        return Response({"msg": "Successfully changed password!"}, status=200)
