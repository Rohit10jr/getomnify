from django.urls import path
from .views import RegisterView, LogoutView, FitnessClassListView, BookingCreateView, BookingListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # api
    path('classes/', FitnessClassListView.as_view(), name='class-list'),
    path('book/', BookingCreateView.as_view(), name='book-class'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
]