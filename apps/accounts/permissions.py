from rest_framework import permissions

class IsAdminUserTier(permissions.BasePermission):
    """Allows access only to ADMIN tier users."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.account_tier == 'ADMIN'
        )

class IsPremiumUserTier(permissions.BasePermission):
    """Allows access to PREMIUM and ADMIN tier users."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.account_tier in ['PREMIUM', 'ADMIN']
        )

class IsStandardUserTier(permissions.BasePermission):
    """Generic check for all authenticated users (since they are at least STANDARD)."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)