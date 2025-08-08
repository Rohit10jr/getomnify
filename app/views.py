from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, FitnessClassSerializer, BookingCreateSerializer, BookingListSerializer
from django.contrib.auth import get_user_model
from .models import FitnessClass, Booking
from django.db import transaction
from django.utils import timezone
from rest_framework.generics import RetrieveAPIView

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


#####################
# --- Omnify API ---
#####################


# GET / classes
class FitnessClassListView(generics.ListAPIView):
    # queryset = FitnessClass.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    serializer_class = FitnessClassSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # print(timezone.now())
        return FitnessClass.objects.filter(date_time__gte=timezone.now()).order_by('date_time')


# POST /book
class BookingCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            # class_id = request.data.get('class_id')
            fitness_class_obj = serializer.validated_data['fitness_class']

            with transaction.atomic():
                # fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)
                fitness_class = FitnessClass.objects.select_for_update().get(pk=fitness_class_obj.pk)

                if fitness_class.available_slots > 0:
                    print("inside if fitness_class.available_slots > 0")
                    serializer.save(fitness_class=fitness_class)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "No available slots for this class."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /bookings
class BookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        client_email = self.request.query_params.get('client_email', None)
        if client_email:
            return Booking.objects.filter(client_email=client_email).order_by('-booking_time')
        return Booking.objects.none()