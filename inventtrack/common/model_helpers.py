from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom user manager for handling the creation of regular and superuser accounts.
    """
    def create_user(self, email, first_name, last_name=None, password=None):
        """
        Creates and saves a regular user with the given email, first name, and password.
        """
        if not email:
            raise ValueError("The Email field is required.")
        if not first_name:
            raise ValueError("The First Name field is required.")
        if not password:
            raise ValueError("The Password field is required.")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name=None, password=None):
        """
        Creates and saves a superuser with the given email, first name, and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class Base(models.Model):
    """
    Abstract base model with timestamp fields for tracking creation and modification times.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for defining model options.
        """
        abstract = True
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
