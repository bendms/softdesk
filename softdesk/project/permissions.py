from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Project, Contributor, Comment, Issue


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAuthorOfProject(BasePermission):
    print("You are here : IsAuthorOfProject")

    def has_permission(self, request, view):
        print("You are here : IsAuthorOfProject.has_permission")
        if (
            request.method == "GET"
            or request.method == "PUT"
            or request.method == "DELETE"
        ):
            user = request.user
            print("USER", user)
            print("VIEW.KWARGS", view.kwargs)
            print("USER_ID", user.id)
            try:
                project_id = view.kwargs["projects_pk"]
                print("PROJECT_ID", project_id)
            except:
                project_id = view.kwargs["pk"]
                print("PROJECT_ID", project_id)
            try:
                contributor_instance = Contributor.objects.get(
                    user_id=user.id, project_id=project_id
                )
                print("======== CONTRIBUTOR_INSTANCE ========", contributor_instance)
                print()
                if contributor_instance.role == "AUTHOR":
                    print("PERMISSION GRANTED")
                    return True
            except:
                print("Contributor_instance does not exist")
                print("PERMISSION DENIED")
                return False
        elif request.method == "POST":
            return True


class IsContributorOfProject(BasePermission):
    def has_permission(self, request, view):
        print("You are here : IsContributorOfProject")
        if (
            request.method == "GET"
            or request.method == "PUT"
            or request.method == "DELETE"
        ):
            user = request.user
            print("USER", user)
            print("VIEW.KWARGS", view.kwargs)
            try:
                project_id = view.kwargs["projects_pk"]
                print("PROJECT_ID", project_id)
            except:
                project_id = view.kwargs["pk"]
                print("PROJECT_ID", project_id)
            try:
                contributor_instance = Contributor.objects.get(
                    user_id=user.id, project_id=project_id
                )
                if contributor_instance.role == "CONTRIBUTOR":
                    print("PERMISSION GRANTED")
                    return True
            except:
                print("Contributor_instance does not exist")
                print("PERMISSION DENIED")
                return False
        elif request.method == "POST":
            print("PERMISSION GRANTED")
            return True


class IsAuthorOfIssue(BasePermission):
    def has_permission(self, request, view):
        print("You are here : IsAuthorOfIssue")
        if (
            request.method == "GET"
            or request.method == "PUT"
            or request.method == "DELETE"
        ):
            user = request.user
            print("USER", user)
            print("VIEW.KWARGS", view.kwargs)
            try:
                issue_id = view.kwargs["pk"]
                print("ISSUE_ID", issue_id)
            except:
                issue_id = view.kwargs["issues_pk"]
                print("ISSUE_ID", issue_id)
            try:
                issue_instance = Issue.objects.get(id=issue_id)
                print("ISSUE_INSTANCE", issue_instance)
                print("ISSUE_INSTANCE.AUTHOR_USER_ID", issue_instance.author_user_id)
                print(bool(issue_instance.author_user_id == user))
                if issue_instance.author_user_id == user:
                    print("PERMISSION GRANTED")
                    return True
            except:
                print("Issue_instance does not exist")
                print("PERMISSION DENIED")
                return False
        elif request.method == "POST":
            print("PERMISSION GRANTED")
            return True


class IsAuthorOfComment(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method == "GET"
            or request.method == "PUT"
            or request.method == "DELETE"
        ):
            user = request.user
            print("USER", user)
            print("VIEW.KWARGS", view.kwargs)
            try:
                comment_id = view.kwargs["pk"]
                print("COMMENT_ID", comment_id)
            except:
                comment_id = view.kwargs["comments_pk"]
                print("COMMENT_ID", comment_id)
            try:
                comment_instance = Comment.objects.get(id=comment_id)
                print("COMMENT_INSTANCE", comment_instance)
                if comment_instance.author_user_id == user:
                    print("PERMISSION GRANTED")
                    return True
            except:
                print("Comment_instance does not exist")
                print("PERMISSION DENIED")
                return False
        elif request.method == "POST":
            print("PERMISSION GRANTED")
            return True
