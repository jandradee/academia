from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Role, SyncRun
from .serializers import UserSerializer, RoleSerializer, SyncRunSerializer
from .permissions import IsAdminPlatform, IsAdminOrManager
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    data = UserSerializer(request.user).data
    data["is_superuser"] = request.user.is_superuser
    data["role_codes"] = list(request.user.roles.values_list("code", flat=True))
    return Response(data)
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all(); serializer_class=UserSerializer; permission_classes=[IsAdminOrManager]
    filterset_fields=["is_active","department"]; search_fields=["display_name","email","username"]
    @action(detail=True, methods=["post"], permission_classes=[IsAdminPlatform])
    def set_roles(self, request, pk=None):
        target = self.get_object()
        if target.pk == request.user.pk:
            return Response({"detail": "No puedes cambiar tus propios roles (protección contra bloqueo de la cuenta administradora)."}, status=400)
        codes = request.data.get("role_codes", [])
        if not isinstance(codes, list):
            return Response({"detail": "role_codes debe ser una lista de códigos de rol."}, status=400)
        roles = list(Role.objects.filter(code__in=codes))
        if len(roles) != len(set(codes)):
            return Response({"detail": "Uno o más roles no existen."}, status=400)
        target.roles.set(roles)
        return Response(UserSerializer(target).data)
class RoleViewSet(viewsets.ModelViewSet):
    queryset=Role.objects.all(); serializer_class=RoleSerializer; permission_classes=[IsAdminPlatform]
class SyncRunViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=SyncRun.objects.all().order_by("-started_at"); serializer_class=SyncRunSerializer; permission_classes=[IsAdminPlatform]
