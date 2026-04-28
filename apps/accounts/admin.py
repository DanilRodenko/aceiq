# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "subscription_plan", "is_pro", "date_joined"]
    list_filter = ["subscription_plan", "is_active"]
    fieldsets = list(UserAdmin.fieldsets) + [
        ("Subscription", {"fields": ("subscription_plan", "subscription_end")}),
    ]
