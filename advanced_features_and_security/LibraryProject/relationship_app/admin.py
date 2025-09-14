from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bookshelf.models import CustomUser
from .models import UserProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)  # optional: makes filtering by role easier
    search_fields = ("user__username", "user__email")  # search by username/email


# Register both the custom user and the user profile
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)