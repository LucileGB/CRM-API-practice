from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CustomUser
from .serializers import LoginSerializer

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
