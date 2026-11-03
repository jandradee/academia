# Academia — Plataforma Corporativa de Capacitación (white-label)

**Stack corregido (v1.5): Django REST Framework (API) + Vue 3 — NO Django con templates.**
Backend: Python 3.13 · Django 5.2 LTS · DRF 3.16 · SimpleJWT · drf-spectacular
Frontend: Vue 3.5 · Vite · Vue Router · Pinia · Axios — Producto **white-label**: marca genérica configurable (ver «Personalizar la marca»)
Base de datos: **SQLite definitivo** (decisión del 28-oct-2026, ya no SQL Server). Archivo en volumen Docker persistente `lms_data` con modo WAL. Ver `SECURITY.md`.


## Personalizar la marca (white-label)

La plataforma nace con una marca neutra («Academia») y se adapta a cada cliente sin tocar código de vistas:

- **Marca de fábrica:** `frontend/src/config/brand.js` es el único punto de configuración del frontend (nombre de la plataforma, empresa, lema, colores, logo, texto del pie y prefijo de certificados). Los colores se publican como variables CSS y todo el diseño deriva tonalidades automáticamente.
- **En tiempo de ejecución:** un administrador puede cambiar nombre, logo y colores en **Administración → Personalización**; esos valores (API `GET /api/branding/`, modelo `SiteSettings`) tienen prioridad sobre los de fábrica.
- **Correos y PDF de certificados** toman nombre y colores de la misma personalización del servidor.

## Desplegar en Coolify (recomendado)

1. Sube esta carpeta a un repo (GitHub/Azure DevOps) — sin el archivo `.env`.
2. En Coolify: **New Resource → Docker Compose**, elige el repo y el archivo `docker-compose.coolify.yml`.
3. En **Environment Variables** pega las variables de `.env.example` con tus valores reales:
   - `DJANGO_SECRET_KEY`: clave larga aleatoria.
   - `CSRF_TRUSTED_ORIGINS`: `https://tu-dominio`.
   - `ALLOWED_IPS` (recomendado al inicio): tu IP pública — con eso, solo tú puedes entrar (doble capa: nginx + Django). Déjalo vacío cuando lo abras a la empresa.
4. Asigna el dominio al servicio **frontend**, puerto **8080**. El frontend (nginx) ya proxya `/api/` y `/health/` al backend, así que no necesitas un segundo dominio.
5. Deploy. Verifica: `https://tu-dominio/health/` → `{"status":"ok"}` y `https://tu-dominio/api/docs/` → Swagger de la API.
6. Crea el primer administrador (Coolify → backend → Terminal):
   `python manage.py createsuperuser`
   Luego entra a `/admin/` (vía un túnel/dominio temporal del backend si lo necesitas) y crea los roles `ADMIN`, `GESTOR`, `COLABORADOR`.

> ✅ SQLite persiste de verdad: el archivo vive en el volumen `lms_data`, así que sobrevive a redeploys. Haz backup de ese volumen en Coolify. El backend no publica puertos: solo el frontend (8080) es accesible, y `/admin/` está bloqueado en el acceso público.

## Desarrollo local (sin Docker)
```bash
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate && python manage.py createsuperuser && python manage.py runserver
# en otra terminal:
cd frontend && npm install && npm run dev   # http://localhost:5173
```

## Qué incluye esta entrega (y qué no)
Incluye la **base funcional desplegable**: modelos completos de la sección 9 de la spec, API DRF de cursos/módulos/videos/recursos, quizzes con calificación en servidor, progreso + dashboard de horas (RF-014), certificados/notificaciones (modelo + API de lectura), auditoría, roles/permisos, JWT y OpenAPI.
No incluye todavía (por fases de la spec, requieren tus decisiones/datos): sincronización real con Microsoft Graph (hay esqueleto seguro en `backend/apps/users/services/graph_sync.py`, Fase 2), login OIDC con Entra ID, generación PDF de certificados (Fase 6, falta logo original aprobado), envío de correo (pospuesto en la spec, RT-010) y subida real de videos con visor instrumentado al 95%.

## Estructura
```
backend/   Django + DRF (config/, apps/{users,courses,quizzes,progress,certificates,audit,core})
frontend/  Vue 3 + Vite (src/{views,router,services,assets}) + nginx.conf (proxy /api → backend)
docker-compose.yml / docker-compose.coolify.yml
.env.example · SPEC-CORRECTION.md
```
