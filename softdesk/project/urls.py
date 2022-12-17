from rest_framework_nested import routers

from authentication.views import RegisterViewSet
from project.views import ProjectViewSet, IssueViewSet, CommentViewSet, ContributorViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
# /projects/
# /projects/{pk}/

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
projects_router.register(r'issues', IssueViewSet, basename='issues')
# /projects/{pk}/issues/
# /projects/{pk}/issues/{pk}/

projects_router.register(r'users', ContributorViewSet, basename='users')
# /projects/{pk}/users/
# /projects/{pk}/users/{pk}/

issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issues')
issues_router.register(r'comments', CommentViewSet, basename='comments')
# /projects/{pk}/issues/{pk}/comments/
# /projects/{pk}/issues/{pk}/comments/{pk}/
