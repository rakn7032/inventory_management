from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from common.model_helpers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends Django's AbstractBaseUser and PermissionsMixin.
    """
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        indexes = [
                models.Index(fields=['email']),
                models.Index(fields=['date_joined']),
                models.Index(fields=['first_name']),
            ]
