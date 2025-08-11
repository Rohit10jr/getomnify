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
import logging


User = get_user_model()
logger = logging.getLogger('app')

#####################
# --- User Auth ---
#####################

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

# GET /classes
class FitnessClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        now = timezone.now()
        try:
            queryset = FitnessClass.objects.filter(date_time__gte=now, available_slots__gt=0).order_by('date_time')
            logger.info(f"Request received for list of classes, Found {queryset.count()} upcoming classes.")
            return queryset
        except Exception as e:
            logger.error(f"Error fetching fitness classes: {e}")
            return FitnessClass.objects.none()


# POST /book
class BookingCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        client_email = request.data.get('client_email', 'unknown')
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            fitness_class_obj = serializer.validated_data['fitness_class']
            logger.info(f"Booking request received for client '{client_email}' for class ID '{fitness_class_obj.pk}'.")

            if fitness_class_obj.date_time < timezone.now():
                logger.warning(f"Booking failed for '{client_email}'. Class '{fitness_class_obj.name}' has already expired.")
                return Response(
                    {"detail": "This class has already expired and cannot be booked."},
                    status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                fitness_class = FitnessClass.objects.select_for_update().get(pk=fitness_class_obj.pk)

                if fitness_class.available_slots > 0:
                    serializer.save(fitness_class=fitness_class)
                    logger.info(f"Booking successful for '{client_email}' in class '{fitness_class.pk}'.")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    logger.warning(f"Booking failed for '{client_email}'. No available slots for class '{fitness_class.pk}'.")
                    return Response({"detail": "No available slots for this class."}, status=status.HTTP_400_BAD_REQUEST)
                
        logger.error(f"Booking request failed due to invalid data for client '{client_email}'. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /bookings
class BookingListView(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        client_email = self.request.query_params.get('client_email', None)

        if client_email:
            try:
                queryset = Booking.objects.filter(client_email=client_email).order_by('-booking_time')
                logger.info(f"Successfully fetched {queryset.count()} bookings for client_email: {client_email}.")
                return queryset
            except Exception as e:
                logger.error(f"Error fetching bookings for client_email '{client_email}': {e}")
                return Booking.objects.none()
        
        logger.warning("Booking list request received without a client_email parameter.")
        return Booking.objects.none()