from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FitnessClass, Booking
from django.utils import timezone
import datetime

class FitnessClassListViewTests(APITestCase):
    def setUp(self):
        self.now = timezone.now()
        FitnessClass.objects.create(name='Yoga', date_time=self.now + datetime.timedelta(days=1), instructor='Jane Doe', total_slots=10, available_slots=10)
        FitnessClass.objects.create(name='Zumba', date_time=self.now + datetime.timedelta(days=2), instructor='John Smith', total_slots=15, available_slots=15)
        FitnessClass.objects.create(name='Past Class', date_time=self.now - datetime.timedelta(days=1), instructor='Old Timer', total_slots=10, available_slots=10)

    def test_list_upcoming_fitness_classes(self):
        """
        Ensure we can retrieve a list of upcoming fitness classes.
        """
        url = reverse('class-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_fitness_classes_with_timezone(self):
        """
        Ensure the timezone parameter correctly converts the date_time.
        """
        url = reverse('class-list')
        response = self.client.get(url, {'timezone': 'America/New_York'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('-04:00', response.data[0]['date_time'])


class BookingCreateViewTests(APITestCase):
    def setUp(self):
        self.now = timezone.now()
        self.fitness_class = FitnessClass.objects.create(name='Yoga', date_time=self.now + datetime.timedelta(days=1), instructor='Jane Doe', total_slots=1, available_slots=1)
        self.full_class = FitnessClass.objects.create(name='Full Class', date_time=self.now + datetime.timedelta(days=1), instructor='John Doe', total_slots=1, available_slots=0)

    def test_create_booking_successfully(self):
        """
        Ensure we can create a booking for a class with available slots.
        """
        url = reverse('book-class')
        data = {'class_id': self.fitness_class.id, 'client_name': 'Test User', 'client_email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().client_email, 'test@example.com')
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 0)

    def test_create_booking_for_full_class(self):
        """
        Ensure we cannot create a booking for a class with no available slots.
        """
        url = reverse('book-class')
        data = {'class_id': self.full_class.id, 'client_name': 'Test User', 'client_email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'No available slots for this class.')
        self.assertEqual(Booking.objects.count(), 0)

    def test_create_duplicate_booking(self):
        """
        Ensure a user cannot book the same class twice.
        """
        Booking.objects.create(fitness_class=self.fitness_class, client_name='Test User', client_email='test@example.com')
        url = reverse('book-class')
        data = {'class_id': self.fitness_class.id, 'client_name': 'Test User', 'client_email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You have already booked this class.', response.data['non_field_errors'])
        self.assertEqual(Booking.objects.count(), 1)

class BookingListViewTests(APITestCase):
    def setUp(self):
        self.now = timezone.now()
        self.class1 = FitnessClass.objects.create(name='Yoga', date_time=self.now + datetime.timedelta(days=1), instructor='Jane Doe', total_slots=10, available_slots=10)
        self.class2 = FitnessClass.objects.create(name='Zumba', date_time=self.now + datetime.timedelta(days=2), instructor='John Smith', total_slots=15, available_slots=15)
        self.booking1 = Booking.objects.create(fitness_class=self.class1, client_name='Test User', client_email='test@example.com')
        self.booking2 = Booking.objects.create(fitness_class=self.class2, client_name='Test User', client_email='test@example.com')
        self.other_booking = Booking.objects.create(fitness_class=self.class1, client_name='Other User', client_email='other@example.com')

    def test_list_bookings_for_client(self):
        """
        Ensure we can retrieve a list of bookings for a specific client.
        """
        url = reverse('booking-list')
        response = self.client.get(url, {'client_email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_bookings_for_client_with_no_bookings(self):
        """
        Ensure an empty list is returned for a client with no bookings.
        """
        url = reverse('booking-list')
        response = self.client.get(url, {'client_email': 'nobody@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_bookings_without_email(self):
        """
        Ensure an empty list is returned if no client_email is provided.
        """
        url = reverse('booking-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)