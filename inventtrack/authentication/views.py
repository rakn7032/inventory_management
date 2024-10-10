from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from .models import User
from common.jwt_helpers import PermissionsAssigning
from common.jwt_helpers import check_permissions
from common.log_utils import LoggerUtility

logger_utility = LoggerUtility()

class UserCreation(APIView):
    """
    API View for creating a new user.
    """
    def post(self, request):
        """
        Handle POST request to create a new user.
        """
        logger_utility.log_request(request, "POST /user-creation")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            logger_utility.log_response(Response(serializer.data), "User created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger_utility.log_error(f"Failed to create user: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdating(APIView):
    """
    API View for updating an existing user.
    """
    permission_classes = [IsAuthenticated]

    @check_permissions(['update_user'])
    def put(self, request, pk):
        """
        Handle PUT request to update an existing user.
        """
        logger_utility.log_request(request, f"PUT /user-update/{pk}")
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            logger_utility.log_error(f"User {pk} not found.")
            return Response({"message":"user not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()

            logger_utility.log_response(Response(serializer.data), f"User {pk} updated successfully")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger_utility.log_error(f"Failed to update user {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View for obtaining a token pair for user authentication.
    """
    def post(self, request):
        """
        Handle POST request to obtain a token pair.
        """
        logger_utility.log_request(request, "POST /token-obtain-pair")
        email = request.data.get('email')
        password = request.data.get('password')
        if not (email and password):
            logger_utility.log_error("Email and password are required.")
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user is None or not user.is_active:
            logger_utility.log_error("Invalid credentials or inactive user.")
            return Response({"message": "Invalid credentials", "status": False}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = PermissionsAssigning().get_token(user)
        access_token = refresh.access_token
        logger_utility.log_response(Response({'access': str(access_token)}), f"Token issued for user {user.id}")
        return Response({'access': str(access_token)}, status=status.HTTP_200_OK)
