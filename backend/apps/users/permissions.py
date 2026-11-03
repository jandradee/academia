from rest_framework.permissions import BasePermission
def has_role(user, *codes): return user.is_authenticated and (user.is_superuser or user.roles.filter(code__in=codes).exists())
class IsAdminPlatform(BasePermission):
    def has_permission(self, request, view): return has_role(request.user,"ADMIN")
class IsCourseManager(BasePermission):
    def has_permission(self, request, view): return has_role(request.user,"ADMIN","GESTOR")
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view): return has_role(request.user,"ADMIN","GESTOR")
