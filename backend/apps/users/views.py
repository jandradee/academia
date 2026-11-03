import mimetypes
from django.http import FileResponse, Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Role, SyncRun
from .serializers import UserSerializer, RoleSerializer, SyncRunSerializer
from .permissions import IsAdminPlatform, IsAdminOrManager
from rest_framework.decorators import api_view, permission_classes, action, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
def _me_data(user):
    data = UserSerializer(user).data
    data["is_superuser"] = user.is_superuser
    data["role_codes"] = list(user.roles.values_list("code", flat=True))
    if user.avatar:
        try:
            import os
            v = int(os.path.getmtime(user.avatar.path))
        except Exception:
            v = 0
        data["avatar_url"] = f"/auth/me/avatar/?v={v}"
    else:
        data["avatar_url"] = ""
    return data

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def me(request):
    user = request.user
    if request.method == "PATCH":
        allowed = ["display_name", "department", "job_title", "office_location", "language", "email_notifications"]
        for field in allowed:
            if field in request.data:
                value = request.data.get(field)
                if field == "language" and value not in ("es", "en"):
                    return Response({"detail": "Idioma no soportado (es/en)."}, status=400)
                if field == "email_notifications" and isinstance(value, str):
                    value = value.lower() in ("true", "1", "yes", "sí", "si")
                setattr(user, field, value)
        avatar_file = request.FILES.get("avatar")
        if avatar_file:
            if not (avatar_file.content_type or "").startswith("image/"):
                return Response({"detail": "La foto de perfil debe ser una imagen."}, status=400)
            if avatar_file.size > 5 * 1024 * 1024:
                return Response({"detail": "La foto de perfil no puede superar 5 MB."}, status=400)
            if user.avatar:
                user.avatar.delete(save=False)
            user.avatar = avatar_file
        user.save()
    return Response(_me_data(user))

@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def my_avatar(request):
    user = request.user
    if request.method == "DELETE":
        if user.avatar:
            user.avatar.delete(save=True)
        return Response(status=204)
    if not user.avatar:
        raise Http404("Sin foto de perfil")
    content_type = mimetypes.guess_type(user.avatar.name)[0] or "image/png"
    return FileResponse(user.avatar.open("rb"), content_type=content_type)
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
