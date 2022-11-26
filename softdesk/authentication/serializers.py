from authentication.models import CustomUser, Contributor
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username'] 
        
class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Contributor
        fields = ['user']