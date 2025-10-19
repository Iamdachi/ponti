from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from PontiBackendApp.serializers import UserRegistrationSerializer

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    # Registration should be accessible to everyone
    permission_classes = [AllowAny]