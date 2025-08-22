from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOrgAdmin(BasePermission):
    """
    Allows access only to users who are OrgAdmin or Superuser.
    """
    def has_permission(self, request, view):
        user = request.user
        # Make sure user is authenticated first
        return bool(user and user.is_authenticated and (user.is_superuser or user.is_org_admin))

class PolicyAccessPermissions(BasePermission):
    """
    GET, HEAD, OPTIONS -> any authenticated user
    POST, PUT, PATCH, DELETE -> only superuser or org_admin
    """
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return bool(user.is_superuser or user.is_org_admin)