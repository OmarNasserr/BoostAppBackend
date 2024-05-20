from rest_framework import permissions


class IsReviewOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return str(obj.reviewer) == str(request.user) or request.user.is_superuser
