from django.contrib.auth.models import User
# from authentication.models import CustomUser, Contributor
from authentication.models import Contributor
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username'] 

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Contributor
        fields = "__all__"