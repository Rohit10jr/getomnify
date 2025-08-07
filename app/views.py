from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer 
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [AllowAny] 
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."})
        except Exception as e:
            error_message = f"Invalid or expired token: {str(e)}"
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)