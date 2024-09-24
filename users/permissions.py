from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Custom permission to only allow Admin users to invite clinicians.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "Admin"
        )


class IsTenantUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
