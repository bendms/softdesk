from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from django.contrib.auth.models import User
from authentication.serializers import UserSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request':request})
        print("DATA: ", request.data)
        print("SERIALIZER: ", serializer)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)