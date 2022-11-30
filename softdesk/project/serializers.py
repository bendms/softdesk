from rest_framework import serializers

from authentication.serializers import UserSerializer
from project.models import Project, Issue, Comment, Contributor

class ProjectSerializer(serializers.ModelSerializer):
    # author_user_id = UserSerializer()
    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author_user_id']

class IssueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Issue
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        
class ContributorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contributor
        fields = "__all__"