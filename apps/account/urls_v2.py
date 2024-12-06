from django.urls import path

from apps.account import views_v2

urlpatterns = [
    path("register/", views_v2.RegistrationV2View.as_view(), name="account-register-v2")
]
