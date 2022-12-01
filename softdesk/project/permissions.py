from rest_framework.permissions import BasePermission

from .models import Project, Contributor, Comment, Issue

class IsAdminAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
    
class IsContributorAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
        print("REQUEST", request.data)
        print("REQUEST.USER", request.user)
        print("VIEW", view.__dict__)

        user = request.user
        project_id = view.kwargs['pk']
        contributor_instance = Contributor.objects.get(user_id=user.id, project_id=project_id)
        print("CONTRIBUTOR_INSTANCE", contributor_instance)
        if contributor_instance and request.user.is_authenticated:
            print('CONTRIBUTOR_INSTANCE_EXIST')
            return True
        print('CONTRIBUTOR_INSTANCE_DOES_NOT_EXIST')
        return False