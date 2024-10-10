from django.urls import path
from . import views

"""
URL patterns for the user-related views in the application.

These patterns define the endpoints for user creation, updating, and authentication.
Available Endpoints:
- `users/`: Handles user creation via the UserCreation view.
- `users/<int:pk>/`: Handles user updates via the UserUpdating view, where `<int:pk>` is the primary key of the user.
- `users/login`: Handles user authentication and token retrieval via the CustomTokenObtainPairView view.
"""

urlpatterns = [
    path('users/', views.UserCreation.as_view(), name='user-create'),
    path('users/<int:pk>/', views.UserUpdating.as_view(), name='user-update'),
    path('users/login', views.CustomTokenObtainPairView.as_view(), name='token obtain pair'),
]
