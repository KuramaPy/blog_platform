from rest_framework.permissions import BasePermission

class IsSuperuserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user.is_authenticated and (
                request.user.is_superuser or 
                request.user.is_admin
            )
        if request.method in ['PATCH']:
            if request.user.is_superuser:
                return True
            if request.user.is_admin:
                data = request.data
                allowed_fields = {'is_staff', 'is_active'}
                return all(key in allowed_fields for key in data.keys())
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
