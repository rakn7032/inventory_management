from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    """
    Admin class for managing User model in the Django admin interface.
    """
    list_display=("id", "email", "first_name", "is_active", "is_superuser")
    fields = ("email", "first_name", "last_name", "is_active", "is_superuser", "is_staff", "date_joined", "updated_at")
    readonly_fields=("date_joined","updated_at")
 
admin.site.register(models.User, UserAdmin)
