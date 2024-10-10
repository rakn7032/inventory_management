from rest_framework_simplejwt.tokens import RefreshToken
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

class PermissionsAssigning:
    """
    A utility class for assigning permissions and generating tokens for users.
    """
    def get_token(self, user):
        """
        Generates a refresh token for a given user and attaches user-specific details.
        """
        token = RefreshToken.for_user(user)
        token['user_id'] = user.id
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['permissions'] = self.get_user_permissions(user)
        return token

    def get_user_permissions(self, user):
        """
        Retrieves a list of permissions for a user, with additional permissions if the user is a superuser.
        """
        common_permissions = ["view_category", "view_item", "update_user"]
        if user.is_superuser:
            return common_permissions + ["create_category", "update_category", "delete_category", "create_item", "update_item", "delete_item"]
        return common_permissions


def check_permissions(required_permissions):
    """
    Custom decorator to check if the user has the required permissions for class-based views.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, *args, **kwargs):
            request = self.request
            jwt_authenticator = JWTAuthentication()
            try:
                user, token = jwt_authenticator.authenticate(request)
            except Exception as e:
                return Response({"message": "Authentication failed.", "detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

            user_permissions = token.get('permissions', [])
            if not all(perm in user_permissions for perm in required_permissions):
                return Response({"message": "Permission denied. You do not have the required permissions."}, 
                                status=status.HTTP_403_FORBIDDEN)

            return view_func(self, *args, **kwargs)
        return _wrapped_view
    return decorator
