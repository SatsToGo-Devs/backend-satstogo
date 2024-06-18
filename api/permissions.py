from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsAuthenticatedAndUserType(BasePermission):
    """
    Allows access only to authenticated users with a specific user type.
    """
    def has_permission(self, request, view):
        required_user_type = getattr(view, 'required_user_type', None)
        if required_user_type is None:
            return False
        return bool(request.user and request.user.is_authenticated and request.user.user_type == required_user_type)
