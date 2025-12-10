from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrCreateOnly(BasePermission):
    """
    Admin users have full access.
    Non-admin users can only create.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.method == "POST":
            return True
        return False
