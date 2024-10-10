from django.db import models
from authentication.models import User
from common.model_helpers import Base

class Category(Base):
    """
    Represents a category for items in the inventory.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [models.Index(fields=['name']),]

class Item(Base):
    """
    Represents an inventory item in the system.
    """
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='created_items')
    updated_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='updated_items')

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['sku']),
            models.Index(fields=['category']),
        ]


