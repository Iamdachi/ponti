# serializers.py
from rest_framework import serializers
from .models import Event, Venue
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        # Include fields necessary for registration
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Use create_user to ensure the password is correctly hashed
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''), # Use .get to allow optional email if not required
            password=validated_data['password']
        )
        return user

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['id', 'name', 'location_latitude', 'location_longitude']

class EventSerializer(serializers.ModelSerializer):
    venue = VenueSerializer()
    created_by_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'venue', 'category', 'name', 'datetime', 'created_by_user', 'event_image', 'description']

    def create(self, validated_data):
        venue_data = validated_data.pop('venue')
        venue, _ = Venue.objects.get_or_create(**venue_data)
        event = Event.objects.create(venue=venue, **validated_data)
        return event