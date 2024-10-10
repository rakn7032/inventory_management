from rest_framework import serializers
from django.db import transaction
from .models import Category, Item
from authentication.models import User
from common.log_utils import LoggerUtility

logger_utility = LoggerUtility()

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Category model.
    This serializer converts Category model instances into JSON format
    """

    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Item model.
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')

    created_by = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all(), required=False)
    updated_by = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all(), required=False)

    class Meta:
        model = Item
        fields = [
            'id', 'category', 'category_id', 'name', 'description', 'sku',
            'quantity', 'price', 'created_by', 'updated_by'
        ]
        read_only_fields = ['created_at', 'updated_at']

    @transaction.atomic
    def create(self, validated_data):
        """
        Creates a new Item instance with validated data.
        """
        user = self.context['request'].user
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        logger_utility.logger.info(f"Creating Item with data: {validated_data}")
        try:
            item = super().create(validated_data)
            logger_utility.logger.info(f"Item {item.id} created successfully by {user.email}")
        except Exception as e:
            logger_utility.log_error(f"Error creating Item: {str(e)}")
            raise e

        return item

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Updates an existing Item instance with validated data.
        """
        user = self.context['request'].user
        validated_data['updated_by'] = user
        logger_utility.logger.info(f"Updating Item {instance.id} with data: {validated_data}")
        try:
            item = super().update(instance, validated_data)
            logger_utility.logger.info(f"Item {item.id} updated successfully by {user.email}")
        except Exception as e:
            logger_utility.log_error(f"Error updating Item {instance.id}: {str(e)}")
            raise e
        
        return item
