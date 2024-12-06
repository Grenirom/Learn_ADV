from django.urls import path

from apps.account import views_v1

from knox.views import LogoutView, LogoutAllView

from apps.account.views_v1 import UserListView

urlpatterns = [
    path("register/", views_v1.RegistrationView.as_view(), name="account-register-v1"),
    path("activate/", views_v1.ActivationView.as_view(), name="activation-account-v1"),
    path(
        "reset-password/",
        views_v1.PasswordResetView.as_view(),
        name="reset-password-request-v1",
    ),
    path(
        "confirm-reset/",
        views_v1.ConfirmPasswordResetView.as_view(),
        name="password-reset-confirm-v1",
    ),
    path("login/", views_v1.LoginView.as_view(), name="login-v1"),
    path("logout/", LogoutView.as_view(), name="logout-v1"),
    path("logout-all/", LogoutAllView.as_view(), name="logout-all-v1"),
    path("all-users/", UserListView.as_view(), name="users_v1"),
]
