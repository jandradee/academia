import os, re
from django.conf import settings
from django.http import FileResponse, HttpResponse, Http404

def authenticate_request(request):
    """Autentica por header (DRF ya lo hizo) o por ?token= (necesario para <video src>)."""
    if getattr(request, "user", None) and request.user.is_authenticated:
        return request.user
    token = request.GET.get("token")
    if token:
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            from django.contrib.auth import get_user_model
            at = AccessToken(token)
            return get_user_model().objects.get(pk=at["user_id"])
        except Exception:
            return None
    return None

def range_file_response(request, file_path, content_type="application/octet-stream", download_name=None):
    if not os.path.exists(file_path):
        raise Http404("Archivo no encontrado")
    size = os.path.getsize(file_path)
    range_header = request.headers.get("Range", "")
    start, end = 0, size - 1
    status_code = 200
    if range_header:
        m = re.match(r"bytes=(\d*)-(\d*)", range_header)
        if m:
            start = int(m.group(1)) if m.group(1) else 0
            end = int(m.group(2)) if m.group(2) else size - 1
            status_code = 206
    length = end - start + 1
    f = open(file_path, "rb"); f.seek(start)
    resp = HttpResponse(f.read(length), status=status_code, content_type=content_type)
    resp["Content-Length"] = str(length)
    resp["Accept-Ranges"] = "bytes"
    if status_code == 206:
        resp["Content-Range"] = f"bytes {start}-{end}/{size}"
    if download_name:
        resp["Content-Disposition"] = f'attachment; filename="{download_name}"'
    return resp

def media_path(storage_key):
    return os.path.join(str(settings.MEDIA_ROOT), storage_key)
