# Corrección a la especificación v1.4 — v1.5

## Qué se corrigió
Donde la spec decía **"Django (backend)"**, ahora es:

> **Backend: Django 5.2 LTS + Django REST Framework (DRF) 3.16 — API REST pura, sin templates de Django.**
> El backend NO renderiza HTML. Todo el HTML lo renderiza Vue 3. Django Admin se conserva solo como consola interna protegida.

## Por qué importa
- Django a secas sugería vistas con templates, formularios server-side y sesión acoplada al HTML. Con Vue 3 eso duplica la presentación y rompe la separación que la propia spec exige en su punto 2.11.
- Con DRF: serializers (nunca exponer `is_correct` de un quiz al colaborador), ViewSets + routers, permisos por rol en servidor, paginación/filtros estándar, JWT (SimpleJWT) para la SPA + sesión para Admin, y OpenAPI automática en `/api/docs/` (drf-spectacular).
- La autenticación corporativa sigue siendo Entra ID / OIDC (Fase 2, MSAL): el backend valida el token y la SPA solo guarda el access token de la API.

## Qué NO cambia
Python 3.13, Django 5.2 LTS como base, Vue 3 + Vite, SQL Server (cambiado a SQLite en v1.6, ver abajo), Docker Compose, marca Río Grande (`#003D7C`, `#F1CF00`, `#C7B99A`, `#BF0811`), regla de finalización `>95%` + 100% de quizzes, y todas las RF/RNF/RT.

## Endpoints creados (Fases 1+3+4+5 parciales, base funcional)
- `GET /health/` · `GET /api/docs/` (Swagger/OpenAPI)
- `POST /api/auth/token/` y `/refresh/` (JWT) · `/api/auth/users/`, `/roles/`, `/sync-runs/`
- `/api/courses/`, `/categories/`, `/modules/`, `/videos/`, `/resources/`, `/assignments/`, `/enrollments/`
- `/api/quizzes/`, `/questions/`, `/quiz-attempts/` (+ `POST /quiz-attempts/{id}/submit/` califica en servidor)
- `/api/course-progress/`, `/module-progress/`, `/video-progress/`, `GET /api/dashboard/me/` (RF-014: horas del año)
- `/api/certificates/`, `/notifications/`, `/audit-logs/`

## Actualización v1.6 (28-oct-2026, por instrucción de Juan)
- **Base de datos: SQLite definitivo.** Queda fuera SQL Server 2019, mssql-django, pyodbc y el driver ODBC 18. El archivo vive en un volumen Docker persistente con WAL.
- **Endurecimiento para exposición a internet** (ver SECURITY.md): ALLOWED_IPS opcional en dos capas, throttling, headers, backend sin puerto público, admin bloqueado en el frontend.
- Las integraciones (Microsoft Graph / Entra ID, correo, PDF) continúan DESPUÉS de publicar esta base.

## Correcciones del primer despliegue en Coolify (28-oct-2026, en vivo)
- El frontend NO publica puerto en el host (`8080:8080` chocaba con el propio Traefik de Coolify, que ya usa el 8080 del host): el 8080 queda solo `expose` y Traefik enruta el dominio por la red interna. Más seguro: no hay acceso directo por IP:puerto.
- `DJANGO_ALLOWED_HOSTS` incluye `localhost` para que el healthcheck interno del backend (http://localhost:8000/health/) no sea rechazado por DisallowedHost. Un Host localhost solo puede originarse dentro del servidor.

## Ampliación v3 (29 oct 2026) y despliegue desde GitHub
- Consola de administración (app `apps.platform`): SiteSettings (empresa, plataforma, lema, colores, logo por URL o archivo, soporte, pie) servido en `GET /api/branding/` (público) y editable en `/api/branding/admin/` (solo ADMIN); la UI aplica el tema con variables CSS.
- Consola del gestor: CRUD de cursos/módulos, subida de videos y recursos (streaming con Range y auth por header o `?token=` para `<video>`), constructor de quizzes con opciones (`add_question`), asignación masiva (`/api/assignments/bulk/`).
- Reportes: `/api/reports/overview/` (completados/en progreso/no iniciados, populares con rating, avance por curso) y `/api/reports/export.xlsx` (openpyxl, 3 hojas). Dashboard de estudiante con obligatorios por iniciar, certificados y horas por mes del año en curso.
- Calificaciones: `CourseRating` 1–5 estrellas por curso/usuario (`/api/courses/<id>/my-rating/`).
- Datos de prueba: `python manage.py seed_demo` (idempotente) — 1 gestor demo, 8 empleados demo, 3 cursos con los videos de Case File #0001–#0003 (descargados de `SEED_VIDEO_0001/2/3`), quizzes, progreso repartido, certificados y ratings.
- Despliegue: desde el repo privado GitHub `jandradee/lms` (rama main) con aplicación en Coolify (deploy key de solo lectura, build pack Docker Compose con `docker-compose.coolify.yml`). El método por zip quedó retirado. Verificado el 29 oct 2026: backend healthy sin puerto público, /health/ = 200, seed cargado.

## Mejoras v5 (29 oct 2026, a pedido de Juan)
- Progreso real del curso (`apps/progress/services.recompute_course_progress`): video 60% (minutos vistos sobre duración, reporte del reproductor cada ~10 s con reanudación), recursos vistos 15% (se registran al descargar), quizzes aprobados 25%. Aprobación: contenido ≥95% + 100% de quizzes → certificado automático. Los endpoints de progreso solo exponen datos propios a estudiantes.
- Miniatura de curso: `Course.cover_key`, subida en la consola del gestor (`POST /api/courses/<id>/cover/`), servida pública en `/api/courses/<id>/cover-image/` y mostrada en inicio, catálogo y detalle (poster del video). El seed incluye portadas generadas para los 3 Case File.
- Quiz: intentos numerados (`attempt_number`), historial por estudiante, botón «Realizar un nuevo intento» tras reprobar y límite opcional `max_attempts`.
- Correos con branding (`apps/core/mailer.py`, plantilla HTML con SiteSettings): aviso inmediato al asignar un curso (unitaria y masiva) y recordatorio diario de vencimientos ≤3 días (comando `send_due_reminders`, máx. 1 por día/asignación; tarea programada diaria en Coolify 13:00 UTC). Transporte por variables EMAIL_* (SMTP); sin EMAIL_HOST, los correos van a la consola/log y la app no falla — pendiente que Juan defina la cuenta de envío.
- Extra: crear usuarios por API ahora guarda la contraseña con hash (campo write-only).

## Corrección v5.1 (29 oct 2026)
- Bug reportado por Juan: las portadas no se veían en el catálogo. Causa: la lista de cursos (CourseListSerializer, usada por catálogo e inicio) no incluía el campo `cover` — solo lo traía el detalle. Añadido a la lista con URL versionada (?v=mtime del archivo) para que al reemplazar una imagen el navegador no muestre la anterior desde caché; `cover-image` y el logo de marca ahora responden Cache-Control: no-cache y el tipo MIME real del archivo.

## Corrección v5.3 (29 oct 2026)
- Alcance por usuario (reportado por Juan al entrar como gestor.cursos): la página principal y certificados deben mostrar solo lo que corresponde a cada usuario. Causa: varios endpoints de registros de aprendizaje daban acceso total a gestores (progreso) o no filtraban (inscripciones, notificaciones), y las asignaciones incluían las hechas POR el usuario. Regla única aplicada: progreso (curso/módulo/video/recurso), intentos de quiz, asignaciones, inscripciones y notificaciones devuelven solo registros propios, excepto al superusuario; los gestores conservan los reportes agregados y la asignación masiva.

## Ampliación v6 (29 oct 2026, a pedido de Juan)
- Inicio según el perfil: gestores y administradores ya no ven el inicio de estudiante («Mis cursos», certificados, horas), sino un panel de gestión con (1) gráficas por curso — usuarios asignados y % no iniciados / en progreso / completados sobre las asignaciones activas (barra apilada por curso + anillo global), (2) grid RawData usuario×curso con filtro por curso y (3) botón «Exportar a Excel» con las hojas «Resumen por curso» y «RawData». Endpoints nuevos (solo gestores/admin): GET /api/reports/dashboard/ y /api/reports/dashboard.xlsx. Los estudiantes conservan su inicio habitual.
