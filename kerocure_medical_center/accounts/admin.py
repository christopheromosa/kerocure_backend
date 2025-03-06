from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StaffUser


class StaffUserAdmin(UserAdmin):
    model = StaffUser
    list_display = (
        "username",
        "first_name",
        "last_name",
        "roles",
        "is_staff",
        "is_active",
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Staff Details", {"fields": ("roles", "phone_number")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Staff Details", {"fields": ("roles", "phone_number")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new user
            obj.set_password("000000")  # Set a default password
        super().save_model(request, obj, form, change)


admin.site.register(StaffUser, StaffUserAdmin)
