# Seguridad — LMS expuesto a internet

## Decisión principal (28-oct-2026)
Base de datos **SQLite** (ya no SQL Server). El archivo vive en el volumen Docker `lms_data` (`/app/data/db.sqlite3`, modo WAL), fuera del código y sin puerto expuesto. No hay servidor de BD que atacar.

## Capas de protección activas
1. **Red:** el backend no publica ningún puerto; solo el nginx del frontend lo alcanza por la red interna de Docker. `/admin/` devuelve 404 en el frontend público.
2. **Restricción por IP (`ALLOWED_IPS`):** si defines tu IP pública en Coolify, la restricción se aplica en DOS capas independientes: nginx (rechaza la conexión web) y un middleware de Django (403 aunque alguien alcanzara el backend). Vacío = sin restricción.
3. **Django endurecido:** `DEBUG=False` forzado, `SECRET_KEY` y `ALLOWED_HOSTS` obligatorios (la app se niega a arrancar sin ellos o con `*`), contraseñas mínimo 12 caracteres con validadores completos y hash Argon2, cookies `Secure+HttpOnly`, HSTS de 1 año, `X-Frame-Options: DENY`, sesiones de 8 h.
4. **Anti fuerza bruta:** DRF throttling (anónimo 100/h, usuario 2000/h) + nginx `limit_req` en el login (5/min por IP) + tokens JWT cortos (acceso 30 min, refresco 1 día con rotación).
5. **Headers web (nginx):** CSP restrictiva, `nosniff`, `Referrer-Policy`, `Permissions-Policy`, `server_tokens off`, rutas `/.` bloqueadas, subida máxima 10 MB.
6. **Contenedores:** backend corre como usuario sin privilegios (`app`, no root), `no-new-privileges`, `cap_drop: ALL` en el backend, dependencias fijadas y sin driver ODBC ni paquetes de SQL Server (superficie menor).
7. **Documentación de la API:** en producción `/api/docs/` solo la ven administradores autenticados.
8. **Secretos:** solo por variables de entorno de Coolify; `.env` fuera de git; los logs no registran tokens ni contraseñas.

## Lo que esto NO sustituye
- HTTPS lo emite Coolify/Traefik (Let's Encrypt): verifica que el dominio tenga certificado válido y redirección HTTP→HTTPS activa.
- SQLite sirve para el arranque y un volumen moderado de colaboradores. Si el uso crece mucho (cientos escribiendo a la vez), el siguiente paso es Postgres — la configuración ya está aislada para cambiarlo sin tocar el código de negocio.
- Sin Entra ID todavía, el login es usuario/contraseña de Django: usa contraseñas largas, crea una cuenta por persona y desactiva las que no se usen. La integración con Microsoft 365 va en la siguiente fase, ya publicado.

## Checklist antes de abrir a toda la empresa
- [ ] Quitar `ALLOWED_IPS` solo cuando el login con Entra ID esté activo, o mantenerlo si el acceso es desde IPs fijas.
- [ ] Backup programado del volumen `lms_data` (Coolify > Backups) y prueba de restauración.
- [ ] Revisar usuarios administradores y activar revisión periódica de `audit-logs`.
