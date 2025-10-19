from rest_framework import generics
from .models import Event, UserEventPreference
from .serializers import EventSerializer, UserEventPreferenceSerializer

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from PontiBackendApp.serializers import UserRegistrationSerializer

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    # Registration should be accessible to everyone
    permission_classes = [AllowAny]


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventPreferenceView(generics.CreateAPIView):
    serializer_class = UserEventPreferenceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        return UserEventPreference.objects.filter(user=self.request.user)
