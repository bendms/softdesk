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
        print("REQUEST_DATA: ", request.data)
        if User.objects.filter(username=request.data['username']).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=request.data['username'], password=request.data['password'], last_name=request.data['last_name'], first_name=request.data['first_name'], email=request.data['email'])
            serializer = UserSerializer(user, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
