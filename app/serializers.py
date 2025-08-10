from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import FitnessClass, Booking
from zoneinfo import ZoneInfo

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    firstname = serializers.CharField(required=True, max_length=55) 
    lastname = serializers.CharField(required=True, max_length=55) 

    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    

class FitnessClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'date_time', 'instructor', 'total_slots', 'available_slots']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_timezone = self.context['request'].query_params.get('timezone', 'Asia/Kolkata')

        try:
            target_tz = ZoneInfo(user_timezone)
            utc_datetime = instance.date_time
            representation['date_time'] = utc_datetime.astimezone(target_tz).isoformat()
        except KeyError:
            ist_tz = ZoneInfo('Asia/Kolkata')
            utc_datetime = instance.date_time
            representation['date_time'] = utc_datetime.astimezone(ist_tz).isoformat()
            
        return representation


class BookingCreateSerializer(serializers.ModelSerializer):
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=FitnessClass.objects.all(),
        source='fitness_class' 
    )

    class Meta:
        model = Booking
        fields = ['class_id', 'client_name', 'client_email']
    
    def validate(self, data):
        if Booking.objects.filter(fitness_class=data['fitness_class'], client_email=data['client_email']).exists():
            raise serializers.ValidationError("You have already booked this class.")
        return data


class BookingListSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booking_time']
        read_only_fields = ['booking_time']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_timezone = self.context['request'].query_params.get('timezone', 'Asia/Kolkata')

        try:
            target_tz = ZoneInfo(user_timezone)
            utc_datetime = instance.booking_time
            representation['date_time'] = utc_datetime.astimezone(target_tz).isoformat()
        except KeyError:
            ist_tz = ZoneInfo('Asia/Kolkata')
            utc_datetime = instance.booking_time
            representation['date_time'] = utc_datetime.astimezone(ist_tz).isoformat()
            
        return representation