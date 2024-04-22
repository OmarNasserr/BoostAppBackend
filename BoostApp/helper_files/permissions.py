from rest_framework import permissions
from helper_files.custom_exceptions import PermissionDenied, NotAuthenticated


class AdminOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        admin_permission = bool(request.user.is_superuser)
        return request.method == "POST" and admin_permission


class AdminOrManager(permissions.IsAdminUser):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return str(obj.manager) == str(request.user) or request.user.is_superuser



class Permissions():
    ################################
    # overrided the permission_denied method to control the error message
    ################################
    def permission_denied(self, request ):
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated()
        raise PermissionDenied()

    ################################
    # overrided the check_object_permissions method because the method has arguments that
    # we don't want like 'message' and 'code'
    ################################

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                )
