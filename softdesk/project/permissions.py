from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Project, Contributor, Comment, Issue

# class IsAdminAuthenticated(BasePermission):
    
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated and request.user.is_superuser)
    
# class IsContributorAuthenticated(BasePermission):
#     def has_permission(self, request, view):            
#         print("REQUEST", request.data)
#         print("REQUEST.USER", request.user)
#         print("VIEW", view.__dict__)
#         user = request.user
#         print("USER", user)
#         project_id = view.kwargs['pk']
#         print(project_id)
#         contributor_instance = Contributor.objects.get(user_id=user.id, project_id=project_id)
#         print("CONTRIBUTOR_INSTANCE", contributor_instance)
#         if contributor_instance and request.user.is_authenticated:
#             print('CONTRIBUTOR_INSTANCE_EXIST')
#             return True
#         print('CONTRIBUTOR_INSTANCE_DOES_NOT_EXIST')
#         return False
    
# class IsContributorOfProjectAuthenticated(BasePermission):
#     def has_permission(self, request, view):            
#         print("REQUEST", request.data)
#         print("REQUEST.USER", request.user)
#         print("VIEW", view.__dict__)
#         user = request.user
#         print("USER", user)
#         project_id = view.kwargs['projects_pk']
#         print(project_id)
#         contributor_instance = Contributor.objects.get(user_id=user.id, project_id=project_id)
#         print("CONTRIBUTOR_INSTANCE", contributor_instance)
#         if contributor_instance and request.user.is_authenticated:
#             print('CONTRIBUTOR_INSTANCE_EXIST')
#             return True
#         print('CONTRIBUTOR_INSTANCE_DOES_NOT_EXIST')
#         return False
    
# class IsAuthorAuthenticated(BasePermission):
    
#     def has_permission(self, request, view):
#         print("REQUEST", request.data)
#         print("REQUEST.USER", request.user)
#         print("VIEW", view.__dict__)
#         user = request.user
#         project_id = view.kwargs['pk']
#         contributor_instance = Contributor.objects.get(user_id=user.id, project_id=project_id)
#         print("CONTRIBUTOR_INSTANCE", contributor_instance)
#         print("CONTRIBUTOR_INSTANCE_ROLE", contributor_instance.role)
#         if contributor_instance.role == 'AUTHOR' and request.user.is_authenticated:
#             print('CONTRIBUTOR_INSTANCE_ROLE = AUTHOR_EXIST')
#             return True
#         print('CONTRIBUTOR_INSTANCE_ROLE = AUTHOR_DOES_NOT_EXIST')
#         return False
    
# class IsAuthorIssue(BasePermission):
#     pass

# class IsAuthorComment(BasePermission):
#     pass

class IsAuthorOfProject(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'PUT' or request.method == 'DELETE':
            user = request.user
            print('USER', user)
            project_id = view.kwargs['pk']
            print('PROJECT_ID', project_id)
            try:
                contributor_instance = Contributor.objects.get(user_id=user.id, project_id=project_id)
                if contributor_instance.role == 'AUTHOR':
                    return True
            except:
                print('Contributor_instance does not exist')
                return False
        elif request.method == 'POST':
            return True
    
# class IsContributorOfProject(BasePermission):
#     def has_permissions(self, request, view):
#         if request.method == 'GET':
            
            
class MaPermission(BasePermission):
    message = "..."
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(...)
        elif request.method == "POST":
            return bool(...) 
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(...) #idem que ci dessous, sinon bloquant


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(...)
        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed." 
        elif request.method == "PUT" or request.method == "DELETE":
            return bool(...) #"ci dessous", c'est ici
        
        