from django.urls import path
from . import views

"""
URL patterns for the Category and Item management API.

This defines the following API routes:
Category Routes:
    - POST /category/ : Creates a new category.
    - PUT /category/<int:pk>/ : Updates an existing category.
    - DELETE /category/<int:pk>/ : Deletes an existing category.
    - GET /categories/ : Retrieves a list of all categories or searches by name.

Item Routes:
    - POST /item/ : Creates a new item.
    - GET /item/<int:pk>/ : Retrieves an item by its primary key.
    - PUT /item/<int:pk>/ : Updates an existing item.
    - DELETE /item/<int:pk>/ : Deletes an existing item.
"""

urlpatterns = [
    path('category/', views.CategoryConfiguration.as_view(http_method_names=['post']), name='create-category'),
    path('category/<int:pk>/', views.CategoryConfiguration.as_view(http_method_names=['put', 'delete']), name='update-delete-category'),
    path('categories/', views.CategoryConfiguration.as_view(http_method_names=['get']), name='list-categories'),
    path('item/', views.ItemConfiguration.as_view(http_method_names=['post']), name='create-item'),
    path('item/<int:pk>/', views.ItemConfiguration.as_view(http_method_names=['get', 'put', 'delete']), name='get-update-delete-item'),
]
