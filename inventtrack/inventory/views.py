from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.core.cache import cache
import json
from .serializers import CategorySerializer, ItemSerializer
from .models import Category, Item
from common.jwt_helpers import check_permissions
from common.log_utils import LoggerUtility

logger_utility = LoggerUtility()

class CategoryConfiguration(APIView):
    """
    API view for managing Category operations (create, update, retrieve, delete).
    """
    permission_classes = [IsAuthenticated]

    @check_permissions(["create_category"])
    def post(self, request):
        """
        Creates a new category with the provided data.
        """
        logger_utility.log_request(request, "POST /category-creation")
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        
            logger_utility.log_response(Response(serializer.data), "Category created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger_utility.log_error(f"Failed to create category: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @check_permissions(["update_category"])
    def put(self, request, pk):
        """
        Updates an existing category identified by its primary key (pk).
        """
        logger_utility.log_request(request, f"PUT /category-update/{pk}")
        try:
            category = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            logger_utility.log_error(f"Category {pk} not found.")
            return Response({"message":"category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()

            logger_utility.log_response(Response(serializer.data), f"Category {pk} updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger_utility.log_error(f"Failed to update category {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @check_permissions(["view_category"])
    def get(self, request):
        """
        Retrieves a list of all categories or searches by name.
        """
        logger_utility.log_request(request, "GET /categories")
        search_term = request.query_params.get('search', None)
        
        if search_term:
            categories = Category.objects.filter(name__icontains=search_term)
        else:
            categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        logger_utility.log_response(Response(serializer.data), "Categories retrieved successfully")      
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @check_permissions(["delete_category"])
    def delete(self, request, pk):
        """
        Deletes a category identified by its primary key (pk).
        """
        logger_utility.log_request(request, f"DELETE /category-delete/{pk}")
        try:
            category = Category.objects.get(id=pk)
        except:
            logger_utility.log_error(f"Category {pk} not found.")
            return Response({"message":"category not found."}, status=status.HTTP_404_NOT_FOUND)
        with transaction.atomic():
            category.delete()
            logger_utility.log_response(Response({"message": "Category deleted successfully."}), f"Category {pk} deleted")   
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class ItemConfiguration(APIView):
    """
    API view for managing Item operations (create, update, retrieve, delete).
    """
    permission_classes = [IsAuthenticated]

    @check_permissions(["create_item"])
    def post(self, request):
        """
        Creates a new item with the provided data and caches it.
        """
        logger_utility.log_request(request, "POST /item-creation")
        serializer = ItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            item_id = serializer.data['id']
            cache_key = f'item_{item_id}'
            cache.set(cache_key, json.dumps(serializer.data))

            logger_utility.log_response(Response(serializer.data), f"Item {item_id} created and cached successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger_utility.log_error(f"Failed to create item: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @check_permissions(["update_item"])
    def put(self, request, pk):
        """
        Updates an existing item identified by its primary key (pk) and refreshes the cache.
        """
        logger_utility.log_request(request, f"PUT /item-update/{pk}")
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            logger_utility.log_error(f"Item {pk} not found.")
            return Response({"message":"Item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            cache_key = f'item_{pk}'
            cache.delete(cache_key)
            cache.set(cache_key, json.dumps(serializer.data))
            
            logger_utility.log_response(Response(serializer.data), f"Item {pk} updated and cache refreshed successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger_utility.log_error(f"Failed to update item {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_permissions(["delete_item"])
    def delete(self, request, pk):
        """
        Deletes an item identified by its primary key (pk) and clears it from cache.
        """
        logger_utility.log_request(request, f"DELETE /item-delete/{pk}")
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            logger_utility.log_error(f"Item {pk} not found.")
            return Response({"message":"Item not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            item.delete()
            cache_key = f'item_{pk}'
            cache.delete(cache_key)
            logger_utility.log_response(Response({"message": "Item deleted successfully."}), f"Item {pk} deleted and cache cleared")
        return Response({"message": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @check_permissions(["view_item"])
    def get(self, request, pk):
        """
        Retrieves an item by its primary key (pk) from cache or database.
        """
        logger_utility.log_request(request, f"GET /item/{pk}")
        cache_key = f'item_{pk}'
        cached_item = cache.get(cache_key)
        if cached_item:
            logger_utility.log_response(Response(json.loads(cached_item)), f"Item {pk} retrieved from cache")
            return Response(json.loads(cached_item), status=status.HTTP_200_OK)
        
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            logger_utility.log_error(f"Item {pk} not found.")
            return Response({"message":"Item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item)
        cache.set(cache_key, json.dumps(serializer.data))
        logger_utility.log_response(Response(serializer.data), f"Item {pk} retrieved from DB and cached")
        return Response(serializer.data, status=status.HTTP_200_OK)
