from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

from project.models import Project, Issue, Comment, Contributor
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .permissions import IsAdminAuthenticated, IsContributorAuthenticated, IsContributorOfProjectAuthenticated, IsAuthorAuthenticated

# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    # user = User.objects.get(id=request.user.id)
    # Contributor.objects.create(user=user, project=Project.objects.get())

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsContributorAuthenticated]
    # def get_queryset(self):
    
    def list(self, request):
        "Return projects where user is contributor in contributor table"
        print("You are here : ProjectViewSet.list")
        print("REQUEST", request.data)
        contributor = request.user
        queryset = Project.objects.filter(contributor__user=contributor)
        serializer_class = ProjectSerializer(queryset, many=True)
        return Response(serializer_class.data)
    

    def retrieve(self, request, pk=None):
        "Return project where user is contributor in contributor table"
        print("You are here : ProjectViewSet.retrieve")
        contributor = request.user
        queryset = Project.objects.filter(contributor__user=contributor, id=pk)
        serializer_class = ProjectSerializer(queryset, many=True)
        return Response(serializer_class.data)
        
    def create(self, request, *args, **kwargs):
        "Create project with author_user_id is user and add contributor in contributor table with role = AUTHOR"
        print("You are here : ProjectViewSet.create")
        data_copy = request.data.copy()
        data_copy['author_user_id'] = request.user.id
        serializer = ProjectSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_instance = Project.objects.get(id=serializer.data['id'])
        Contributor.objects.create(user=request.user, project=project_instance, role="AUTHOR")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
class IssueViewSet(viewsets.ModelViewSet):
    
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    
    # permission_classes = [IsContributorOfProjectAuthenticated]
    
    def list(self, request, projects_pk=None):
        queryset = Issue.objects.filter(project_id=projects_pk)
        serializer = IssueSerializer(queryset, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def retrieve(self, request, pk=None, projects_pk=None):
        queryset = Issue.objects.filter(pk=pk, project_id=projects_pk)
        issues = get_object_or_404(queryset, pk=pk)
        serializer = IssueSerializer(issues)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def create(self, request, *args, **kwargs):
        "Create issue with author_user_id is user"
        print("You are here : IssueViewSet.create")
        data_copy = request.data.copy()
        "Copy data to data_copy because request.data is immutable"
        data_copy['author_user_id'] = request.user.id
        "Get id of assigned_user from username"
        assigned_user = User.objects.filter(username=data_copy['assigned_user_id'])
        assigned_user_id = assigned_user[0].id
        data_copy['assigned_user_id'] =  assigned_user_id
        serializer = IssueSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
       
class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, projects_pk=None, issues_pk=None):
        queryset = Comment.objects.filter(issue_id=issues_pk)
        serializer = CommentSerializer(queryset, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def retrieve(self, request, pk=None, projects_pk=None, issues_pk=None):
        queryset = Comment.objects.filter(issue_id=issues_pk, pk=pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
class ContributorViewSet(viewsets.ModelViewSet):

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer    
    
    def list(self, request, projects_pk=None):
        "Return contributors where user is contributor in contributor table"
        queryset = Contributor.objects.filter(project_id=projects_pk)
        serializer_class = ContributorSerializer(queryset, many=True)
        headers = self.get_success_headers(serializer_class.data)    
        return Response(serializer_class.data, status=status.HTTP_200_OK, headers=headers)
    
    def retrieve(self, request, pk=None, projects_pk=None):
        "Return contributor where user is contributor in contributor table"
        queryset = Contributor.objects.filter(project_id=projects_pk, pk=pk)
        contributor = get_object_or_404(queryset, pk=pk)
        serializer_class = ContributorSerializer(contributor)
        headers = self.get_success_headers(serializer_class.data)    
        return Response(serializer_class.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        print("Data copy : ", data_copy)
        new_contributor = User.objects.filter(username=data_copy['user'])
        data_copy['user'] = new_contributor[0].id
        print("Data copy : ", data_copy)
        serializer = ContributorSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)