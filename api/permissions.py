from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import Comments, Contributors, Issues, Projects


class ProjectsPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if view.kwargs["pk"]:
                return Contributors.objects.filter(
                    user_id=request.user, project=view.kwargs["pk"]
                ).exists()
            return True
        elif request.method in ["POST"]:
            return True
        elif request.method in ["PUT", "DELETE"]:
            if Projects.objects.filter(project=view.kwargs["pk"]).exists():
                return obj.author_user == request.user
            raise ObjectDoesNotExist()
        return False


class IssuesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS", "POST"]:
            return Contributors.objects.filter(
                user_id=request.user,
                project=view.kwargs["project_pk"],
                role="contributeur",
            ).exists()
        elif request.method in ["PUT", "DELETE"]:
            if Issues.objects.filter(project_id=view.kwargs["project_pk"]).exists():
                return Contributors.objects.filter(
                    user_id=request.user,
                    project=view.kwargs["project_pk"],
                    role="contributeur",
                ).exists()
            raise ObjectDoesNotExist()


class CommentsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS", "POST"]:
            return Contributors.objects.filter(
                user_id=request.user,
                project=view.kwargs["project_pk"],
                role="contributeur",
            ).exists()
        elif request.method in ["PUT", "DELETE"]:
            if Comments.objects.filter(issue_id=view.kwargs["issue_pk"]).exists():
                return Contributors.objects.filter(
                    user_id=request.user,
                    project=view.kwargs["project_pk"],
                    role="contributeur",
                ).exists()
            raise ObjectDoesNotExist()


class ContributorPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS", "POST"]:
            return Contributors.objects.filter(
                user_id=request.user, project=view.kwargs["project_pk"]
            ).exists()
        elif request.method in ["DELETE"]:
            if Projects.objects.filter(project=view.kwargs["project_pk"]).exists():
                return Contributors.objects.filter(
                    user_id=request.user, project=view.kwargs["project_pk"]
                ).exists()
            raise ObjectDoesNotExist()
