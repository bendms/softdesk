from rest_framework import routers

from project.views import ProjectViewSet, IssueViewSet, CommentViewSet
from authentication.views import UserViewSet

router = routers.SimpleRouter()
router.register('project', ProjectViewSet)
router.register('issue', IssueViewSet)
router.register('comment', CommentViewSet)
router.register('comment', UserViewSet)