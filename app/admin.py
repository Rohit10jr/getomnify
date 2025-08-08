from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, FitnessClass, Booking

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'firstname', 'lastname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('firstname', 'lastname')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'firstname', 'lastname', 'password', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'firstname', 'lastname')
    ordering = ('email',)

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_time', 'instructor', 'total_slots', 'available_slots')
    list_filter = ('instructor', 'date_time')
    search_fields = ('name', 'instructor')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','fitness_class', 'client_name', 'client_email', 'booking_time')
    list_filter = ('fitness_class', 'booking_time')
    search_fields = ('client_name', 'client_email')

