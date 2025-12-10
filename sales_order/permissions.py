from rest_framework import permissions


class IsAdminOrSalesUserCreateOnly(permissions.BasePermission):
    """
    Sales User → can only create sales orders
    Sales User → can only create sales orders
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.method == 'POST':
            return True
        return False
