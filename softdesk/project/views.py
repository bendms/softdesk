from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

from project.models import Project, Issue, Comment, Contributor
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    # user = User.objects.get(id=request.user.id)
    # Contributor.objects.create(user=user, project=Project.objects.get())

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    # def get_queryset(self):
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("SERIALIZER", serializer)
        print("REQUEST", request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project = Project.objects.get(title=request.POST["title"])
        user_id = request.user.id
        print("USER", user_id)
        print("PROJECT", project.id)
        print("SELF.PERFORM_CREATE(SERIALIZER)", self.perform_create(serializer))
        contributor_instance = Contributor.objects.create(user_id=user_id, project_id=project.id)
        print("CONTRIBUTOR_INSTANCE", contributor_instance)
        headers = self.get_success_headers(serializer.data)
        print("HEADERS", headers)
        print("Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)", Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    
class IssueViewSet(viewsets.ModelViewSet):
    
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    
class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer