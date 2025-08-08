from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier
    for authentication.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    custom user model for email based auth
    """
    email = models.EmailField(unique=True,db_index=True)
    firstname = models.CharField(max_length=55)
    lastname = models.CharField(max_length=55)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class FitnessClass(models.Model): 
    name = models.CharField(max_length=100) 
    date_time = models.DateTimeField() 
    instructor = models.CharField(max_length=100) 
    total_slots = models.PositiveIntegerField() 
    available_slots = models.PositiveIntegerField() 
    
    def __str__(self): 
        return f"{self.id}. {self.name} - {self.instructor} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        if self.available_slots > self.total_slots:
            raise ValidationError("Available slots cannot be greater than total slots.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Booking(models.Model): 
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings') 
    client_name = models.CharField(max_length=100) 
    client_email = models.EmailField() 
    booking_time = models.DateTimeField(auto_now_add=True) 
    
    class Meta: 
        # unique_together = ('fitness_class', 'client_email') 
        indexes = [
            models.Index(fields=['client_email'], name='booking_client_email_idx'),
        ] 

    def __str__(self): 
        return f"Booking for {self.client_name} in {self.fitness_class.name}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.fitness_class.available_slots -= 1
            self.fitness_class.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Increment available slots when a booking is deleted
        self.fitness_class.available_slots += 1
        self.fitness_class.save()
        super().delete(*args, **kwargs)