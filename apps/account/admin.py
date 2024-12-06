from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff"]
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
