import ipaddress
from django.conf import settings
from django.http import HttpResponseForbidden

def _client_ip(request):
    # Detrás de nginx/Traefik de Coolify: el proxy fija X-Forwarded-For.
    # Solo se confía porque el backend NO está expuesto directo a internet
    # (solo lo alcanza el frontend/nginx de la misma red Docker).
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")

def _allowed(ip_str):
    nets = getattr(settings, "ALLOWED_IP_NETWORKS", [])
    if not nets:
        return True  # sin restricción configurada: aplican las demás capas
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return any(ip in net for net in nets)

class IPAllowlistMiddleware:
    """Si ALLOWED_IPS está definido en Coolify, SOLO esas IPs/redes entran.
    /health/ queda exento para el healthcheck interno de Docker/Coolify."""
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        if request.path == "/health/":
            return self.get_response(request)
        if not _allowed(_client_ip(request)):
            return HttpResponseForbidden("Acceso no autorizado desde esta IP.")
        return self.get_response(request)
