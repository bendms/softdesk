# from rest_framework import routers
from django.urls import include, path
from rest_framework_nested import routers

from project.views import ProjectViewSet, IssueViewSet, CommentViewSet, ContributorViewSet
from authentication.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
projects_router.register(r'issues', IssueViewSet, basename='issues')
projects_router.register(r'users', ContributorViewSet)
issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issues')
issues_router.register(r'comments', CommentViewSet, basename='comments')

# router.register('issues', IssueViewSet)
# router.register('comments', CommentViewSet)
# router.register('', UserViewSet)

#TODO: implémenter nested-router pour les URLS imbriquées
