from rest_framework import routers

from project.views import ProjectViewSet, IssueViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register('project', ProjectViewSet)
router.register('issue', IssueViewSet)
router.register('comment', CommentViewSet)