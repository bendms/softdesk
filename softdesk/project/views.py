from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from project.models import Project, Issue, Comment, Contributor
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .permissions import IsAuthorOfProject, IsContributorOfProject, IsAuthorOfComment, IsAuthorOfIssue, IsAuthenticated
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthorOfProject | IsContributorOfProject]
            return [permission() for permission in permission_classes]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthorOfProject]
            return [permission() for permission in permission_classes]

    
    def list(self, request):
        "Return projects where user is contributor in contributor table"
        print("You are here : ProjectViewSet.list")
        print("REQUEST", request.data)
        contributor = request.user
        queryset = Project.objects.filter(contributor__user=contributor)
        serializer_class = ProjectSerializer(queryset, many=True)
        headers = self.get_success_headers(serializer_class.data)
        return Response(serializer_class.data, status=status.HTTP_200_OK, headers=headers)
    
    def retrieve(self, request, pk=None):
        "Return project where user is contributor in contributor table"
        print("You are here : ProjectViewSet.retrieve")
        contributor = request.user
        print("CONTRIBUTOR", contributor)
        print("PK", pk)
        queryset = Project.objects.filter(contributor__user=contributor, id=pk)
        print("QUERYSET", queryset)
        serializer_class = ProjectSerializer(queryset, many=True)
        print("SERIALIZER", serializer_class)
        headers = self.get_success_headers(serializer_class.data)
        print("HEADERS", headers)
        return Response(serializer_class.data, status=status.HTTP_200_OK, headers=headers)
    
    def create(self, request, *args, **kwargs):
        "Create project with author_user_id is user and add contributor in contributor table with role = AUTHOR"
        print("You are here : ProjectViewSet.create")
        data_copy = request.data.copy()
        data_copy['author_user_id'] = request.user.id
        serializer = ProjectSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project_instance = Project.objects.get(id=serializer.data['id'])
        Contributor.objects.create(user=request.user, project=project_instance, role="AUTHOR", permission="ADMIN")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, pk=None, *args, **kwargs):
        "Update project with author_user_id is user"
        print("You are here : ProjectViewSet.update")
        print("REQUEST", request.data)
        data_copy = request.data.copy()
        queryset = Project.objects.filter(id=pk)
        project = get_object_or_404(queryset, id=pk)
        serializer = ProjectSerializer(project, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        
    def destroy(self, request, pk=None, *args, **kwargs):
        "Delete project with author_user_id is user"
        print("You are here : ProjectViewSet.destroy")
        queryset = Project.objects.filter(id=pk)
        project = get_object_or_404(queryset, id=pk)
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)
class IssueViewSet(viewsets.ModelViewSet):
    
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = [IsAuthorOfProject | IsContributorOfProject]
            return [permission() for permission in permission_classes]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthorOfIssue]
            return [permission() for permission in permission_classes]
   

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
    
    def update(self, request, pk=None, *args, **kwargs):
        "Update issue with author_user_id is user"
        print("You are here : IssueViewSet.update")
        data_copy = request.data.copy()
        "Copy data to data_copy because request.data is immutable"
        data_copy['author_user_id'] = request.user.id
        "Get id of assigned_user from username"
        assigned_user = User.objects.filter(username=data_copy['assigned_user_id'])
        assigned_user_id = assigned_user[0].id
        data_copy['assigned_user_id'] =  assigned_user_id
        queryset = Issue.objects.filter(pk=pk)
        issue = get_object_or_404(queryset, pk=pk)
        serializer = IssueSerializer(issue, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        "Delete issue with author_user_id is user"
        print("You are here : IssueViewSet.delete")
        queryset = Issue.objects.filter(pk=pk)
        issue = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(issue)
        return Response(status=status.HTTP_204_NO_CONTENT)
       
class CommentViewSet(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthorOfProject | IsContributorOfProject]
            return [permission() for permission in permission_classes]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthorOfProject | IsContributorOfProject | IsAuthorOfComment]
            return [permission() for permission in permission_classes]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthorOfComment]
            return [permission() for permission in permission_classes]

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
    
    def create(self, request, *args, **kwargs):
        "Create comment with author_user_id is user"
        print("You are here : CommentViewSet.create")
        data_copy = request.data.copy()
        "Copy data to data_copy because request.data is immutable"
        data_copy['author_user_id'] = request.user.id
        serializer = CommentSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, pk=None, *args, **kwargs):
        "Update comment with author_user_id is user"
        print("You are here : CommentViewSet.update")
        data_copy = request.data.copy()
        "Copy data to data_copy because request.data is immutable"
        data_copy['author_user_id'] = request.user.id
        queryset = Comment.objects.filter(pk=pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment, data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        "Delete comment with author_user_id is user"
        print("You are here : CommentViewSet.delete")
        queryset = Comment.objects.filter(pk=pk)
        comment = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ContributorViewSet(viewsets.ModelViewSet):

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthorOfProject | IsContributorOfProject]
            return [permission() for permission in permission_classes]
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAuthorOfProject]
            return [permission() for permission in permission_classes]
    
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
    
    def destroy(self, request, pk=None, projects_pk=None):
        queryset = Contributor.objects.filter(project_id=projects_pk, user_id=pk)
        contributor_to_destroy = get_object_or_404(queryset)
        self.perform_destroy(contributor_to_destroy)
        return Response(status=status.HTTP_204_NO_CONTENT)
        