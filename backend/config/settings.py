import os
from pathlib import Path
from datetime import timedelta
import ipaddress
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env.bool("DJANGO_DEBUG", default=False)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="")
if not SECRET_KEY or SECRET_KEY.startswith("django-insecure"):
    if not DEBUG:
        raise RuntimeError("DJANGO_SECRET_KEY es obligatoria en producción. Genera una larga y aleatoria y ponla en Coolify > Environment Variables.")
    SECRET_KEY = "django-insecure-solo-para-desarrollo-local"

# En producción exige hosts explícitos; "*" solo se tolera en DEBUG local
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
if not DEBUG and ALLOWED_HOSTS == ["*"]:
    raise RuntimeError("DJANGO_ALLOWED_HOSTS=* no está permitido en producción. Pon tu dominio en Coolify.")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
TIME_ZONE = env("TIME_ZONE", default="America/El_Salvador")
LANGUAGE_CODE = "es"
USE_I18N = True
USE_TZ = True

# --- Restricción por IP pública (opcional pero recomendada al inicio) ---
# ALLOWED_IPS=203.0.113.10,198.51.100.0/24  -> vacío = sin restricción de IP
_raw_ips = env.list("ALLOWED_IPS", default=[])
ALLOWED_IP_NETWORKS = []
for _item in _raw_ips:
    _item = _item.strip()
    if _item:
        ALLOWED_IP_NETWORKS.append(ipaddress.ip_network(_item if "/" in _item else _item + "/32", strict=False))

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","rest_framework_simplejwt","corsheaders","django_filters","drf_spectacular",
    "apps.core","apps.platform","apps.users","apps.courses","apps.quizzes","apps.progress","apps.certificates","apps.audit",
]
MIDDLEWARE = [
    "apps.core.middleware.IPAllowlistMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]

# --- Base de datos: SQLite DEFINITIVO (decisión de Juan, 28-oct-2026) ---
# El archivo vive en /app/data (volumen Docker persistente), NUNCA en el código.
DATA_DIR = Path(env("DATA_DIR", default=str(BASE_DIR / "data")))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DATA_DIR / "db.sqlite3",
    "OPTIONS": {"timeout": 20, "init_command": ""}}}
# WAL se activa en AppConfig.ready de core (mejor concurrencia y durabilidad en SQLite)

AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator","OPTIONS":{"min_length":12}},
    {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"},
]
PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher","django.contrib.auth.hashers.PBKDF2PasswordHasher"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(env("MEDIA_ROOT", default=str(BASE_DIR / "media_private")))
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS: por defecto SIN orígenes extra (la SPA va por el mismo dominio vía nginx).
# No usar CORS_ALLOW_ALL_ORIGINS jamás en producción.
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True

# Límites de subida (anti DoS por archivos gigantes)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication","rest_framework.authentication.SessionAuthentication"),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend","rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Anti fuerza bruta / abuso: límites globales (el login tiene además rate-limit en nginx)
    "DEFAULT_THROTTLE_CLASSES": ("rest_framework.throttling.AnonRateThrottle","rest_framework.throttling.UserRateThrottle"),
    "DEFAULT_THROTTLE_RATES": {"anon": "100/hour", "user": "2000/hour"},
}
SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(minutes=30), "REFRESH_TOKEN_LIFETIME": timedelta(days=1), "ROTATE_REFRESH_TOKENS": True, "BLACKLIST_AFTER_ROTATION": False}
SPECTACULAR_SETTINGS = {"TITLE":"Academia — LMS API","DESCRIPTION":"API REST (Django REST Framework). Documentación solo visible para administradores en producción.","VERSION":"1.6.0","SERVE_PERMISSIONS":["rest_framework.permissions.IsAdminUser"]}

# --- Seguridad de transporte y sesión (producción tras el HTTPS de Coolify) ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 8
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_HTTPONLY = False
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)  # Coolify/Traefik ya redirige HTTP->HTTPS; activarlo aquí puede crear bucles
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"

LOGGING = {"version":1,"disable_existing_loggers":False,"formatters":{"simple":{"format":"{levelname} {asctime} {message}","style":"{"}},"handlers":{"console":{"class":"logging.StreamHandler","formatter":"simple"}},"root":{"handlers":["console"],"level":"INFO"},"loggers":{"django.security":{"handlers":["console"],"level":"WARNING","propagate":False}}}

# --- Correo transaccional (avisos de asignación y recordatorios) ---
SITE_BASE_URL = env("SITE_BASE_URL", default="https://lms.jandradee.cloud")
EMAIL_HOST = env("EMAIL_HOST", default="")
if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = env.int("EMAIL_PORT", default=587)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
    EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER or "no-reply@example.com")
else:
    # Sin SMTP configurado: los correos se escriben en el log (consola) y la app no falla.
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Academia <no-reply@example.com>")
