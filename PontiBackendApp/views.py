from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
# Create your views here.
# views.py
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from PontiBackendApp.serializers import UserRegistrationSerializer

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    # Registration should be accessible to everyone
    permission_classes = [AllowAny]


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]