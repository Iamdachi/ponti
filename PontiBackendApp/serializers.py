from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Event, Venue, UserProfile

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    age = serializers.IntegerField(write_only=True)
    sex = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)
    personality_type = serializers.CharField(write_only=True)
    preferred_personality_type = serializers.CharField(write_only=True)
    hobbies = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "password2",
            "first_name", "last_name", "age", "sex", "location",
            "personality_type", "preferred_personality_type", "hobbies"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")

        profile_data = {
            "age": validated_data.pop("age"),
            "sex": validated_data.pop("sex"),
            "location": validated_data.pop("location"),
            "personality_type": validated_data.pop("personality_type"),
            "preferred_personality_type": validated_data.pop("preferred_personality_type"),
            "hobbies": validated_data.pop("hobbies")
        }

        # Create user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=password
        )

        # Create profile
        UserProfile.objects.create(user=user, **profile_data)
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
