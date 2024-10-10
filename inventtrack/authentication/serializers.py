from rest_framework import serializers
from django.db import transaction
from .models import User
from common.helpers import CommonValidators
from common.log_utils import LoggerUtility

logger_utility = LoggerUtility()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model to handle serialization and validation of user data.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'updated_at', 'password']
        read_only_fields = ['id', 'date_joined', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, email):
        """
        Validate the email using CommonValidators.email_validator.
        """
        logger_utility.logger.debug(f"Validating email: {email}")
        if not CommonValidators().email_validator(email):
            logger_utility.log_error(f"Invalid email format: {email}")
            raise serializers.ValidationError("Invalid email format.")
        logger_utility.logger.info(f"Email {email} validated successfully.")
        return email

    def validate_password(self, password):
        """
        Validate the password using CommonValidators.password_validator.
        """
        logger_utility.logger.debug("Validating password.")
        if not CommonValidators().password_validator(password):
            logger_utility.log_error("Password validation failed.")
            raise serializers.ValidationError("Password must be at least 8 characters long, include an uppercase letter, a number, and a special character.")
        logger_utility.logger.info("Password validated successfully.")
        return password
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Create a new User instance from the validated data.
        """
        logger_utility.logger.info(f"Creating user with data: {validated_data}")
        is_superuser = validated_data.get('is_superuser', False)
        with transaction.atomic():
            try:
                user = User.objects.create(
                    email=validated_data['email'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data.get('last_name', ''),
                    is_superuser=is_superuser
                )
                user.set_password(validated_data['password'])
                if user.is_superuser:
                    user.is_staff = True
                user.save()
                logger_utility.logger.info(f"User {user.id} created successfully.")
            except Exception as e:
                logger_utility.log_error(f"Error creating user: {str(e)}")
                raise e
            
            return user
        
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Update an existing User instance with the validated data.
        """
        logger_utility.logger.info(f"Updating user {instance.id} with data: {validated_data}")
        with transaction.atomic():
            try:
                instance.email = validated_data.get('email', instance.email)
                instance.first_name = validated_data.get('first_name', instance.first_name)
                instance.last_name = validated_data.get('last_name', instance.last_name)
                if 'password' in validated_data:
                    instance.set_password(validated_data['password'])

                instance.is_active = validated_data.get('is_active', instance.is_active)
                instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
                if instance.is_superuser:
                    instance.is_staff = True
                instance.save()
                logger_utility.logger.info(f"User {instance.id} updated successfully.")
            except Exception as e:
                logger_utility.log_error(f"Error updating user {instance.id}: {str(e)}")
                raise e

            return instance
