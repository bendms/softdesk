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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("SERIALIZER", serializer)
        self.perform_create(serializer)
        project = Project.objects.get(title=request.POST["title"])
        user_id = request.user.id
        print("USER", user_id)
        print("PROJECT", project.id)
        print("SELF.PERFORM_CREATE(SERIALIZER)", self.perform_create(serializer))
        contributor_instance = Contributor.objects.create(user=request.user, project=project, role=Contributor.AUTHOR)
        print("CONTRIBUTOR_INSTANCE", contributor_instance)
        headers = self.get_success_headers(serializer.data)
        print("HEADERS", headers)
        print("Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)", Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers))
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