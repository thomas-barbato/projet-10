from rest_framework import permissions


# https://stackoverflow.com/questions/59141266/drf-only-author-can-create-or-update-the-book-permission
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_user == request.user
