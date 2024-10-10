from django.contrib import admin
from . import models

class CategoryAdmin(admin.ModelAdmin):
    """
    Admin class for managing the Category model in the Django admin interface.
    """
    list_display=("id", "name")
    fields = ("name", "created_at", "updated_at")
    readonly_fields=("created_at","updated_at")

class ItemAdmin(admin.ModelAdmin):
    """
    Admin class for managing the Item model in the Django admin interface.
    """
    list_display=("id", "name","sku", "quantity", "category", "price")
    fields = ("category","name","description", "sku", "quantity", "price", "created_by", "updated_by", "created_at", "updated_at")
    readonly_fields=("created_at","updated_at")
 
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Item, ItemAdmin)
