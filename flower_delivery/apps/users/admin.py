from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser", "is_active")
    actions = ["make_admin", "remove_admin"]

    def make_admin(self, request, queryset):
        queryset.update(is_staff=True, is_superuser=True)
        self.message_user(request, "Выбранные пользователи назначены администраторами.")

    make_admin.short_description = "Назначить администратора"

    def remove_admin(self, request, queryset):
        queryset.update(is_staff=False, is_superuser=False)
        self.message_user(
            request, "Права администратора сняты с выбранных пользователей."
        )

    remove_admin.short_description = "Снять права администратора"
