from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # columns shown in the list view
    list_filter = ("publication_year", "author")  # filters on the right-hand side
    search_fields = ("title", "author")  # search box for quick lookups


# Register the model with the custom admin
admin.site.register(Book, BookAdmin)

class ModelAdmin(UserAdmin):
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
admin.site.register(CustomUser, ModelAdmin)
admin.site.register(UserProfile, UserProfileAdmin)