# LMS Río Grande Foods — Guía DNS + Producción en Google Cloud / Azure

Generada el 28-oct-2026. Aplica a la aplicación ya construida (Django REST Framework + Vue 3, SQLite, Docker Compose endurecido).

---

## Parte 1 — DNS para que `lms.jandradee.cloud` funcione

### Por qué falla la verificación hoy
Sin un registro DNS para el subdominio `lms`, el nombre no resuelve: ningún navegador (ni el tuyo ni el mío) puede llegar al servidor, aunque la aplicación esté corriendo en Coolify. El registro se crea en **Cloudflare**, donde ya administras la zona `jandradee.cloud`.

### Antes de empezar: consigue la IP de tu servidor
Es la **misma IP** que ya usan tus sitios actuales. La ves en cualquiera de estos lugares:
- Cloudflare → zona `jandradee.cloud` → **DNS → Records**: el valor IPv4 del registro **A** de la raíz (`@`) o del panel.
- O en Coolify → **Servers** → tu servidor → su IP pública.

Anótala; la necesitas en el paso 2. No la confundas con tu IP de navegación (201.247.144.9): esa es la de tu conexión, la del DNS es la del **servidor**.

### Pasos en Cloudflare
1. Entra a https://dash.cloudflare.com → selecciona la zona **jandradee.cloud**.
2. Ve a **DNS → Records → Add record** y crea:
   - **Type:** `A`
   - **Name:** `lms`
   - **IPv4 address:** la IP de tu servidor (la del paso anterior)
   - **Proxy status:** **DNS only** (nube **gris**, desactivado) ⚠️ *Este es el paso crítico, ver abajo.*
   - **TTL:** Auto
3. Guarda con **Save**.
4. **No** crees registro `AAAA` ni `CNAME` para `lms`. Un solo `A` basta.

### ⚠️ Por qué debe ser "DNS only" (nube gris)
La aplicación está restringida a tu IP pública. Si Cloudflare proxya (nube naranja), el servidor deja de ver la IP real del visitante y ve IPs de Cloudflare: la restricción bloquearía a **todos**, incluido tú. Además, con nube gris Let's Encrypt emite el certificado directo en tu servidor sin intermediarios. Es el mismo modo que ya usan tus registros actuales.

### En Coolify (si aún no está hecho)
1. Aplicación **lms-riogrande** → servicio **frontend** → campo de dominio: `https://lms.jandradee.cloud` con puerto **8080**.
2. El **backend no** lleva dominio.
3. Guarda y **Redeploy/Restart** una vez: al detectar el DNS ya apuntando, Traefik pide el certificado Let's Encrypt automáticamente (necesita los puertos 80 y 443 del servidor accesibles).

### Verificación (5–10 minutos después de crear el registro)
- En tu computadora: `nslookup lms.jandradee.cloud` → debe devolver **directamente la IP de tu servidor** (si devuelve IPs 104.x.x.x o 172.67.x.x, quedó con proxy naranja: vuelve a ponerlo en gris). También puedes comprobarlo en https://dnschecker.org buscando `lms.jandradee.cloud`.
- Desde tu conexión (tu IP): **https://lms.jandradee.cloud** debe cargar la portada del LMS.
- **https://lms.jandradee.cloud/health/** debe responder `{"status":"ok"}` desde cualquier red (esa ruta es pública a propósito).
- Desde tu celular **con el Wi-Fi apagado** (datos móviles = otra IP): la portada debe dar **403**. Eso es correcto: es la restricción funcionando. Con Wi-Fi (misma IP de tu casa/oficina) sí debe cargar.

### Diagnóstico rápido
| Síntoma | Causa probable | Arreglo |
|---|---|---|
| "No se puede acceder a este sitio" / NXDOMAIN | Falta el registro A o aún propaga | Crea el registro; espera hasta ~1 h si consultaste el nombre antes de crearlo (caché negativo) |
| Resuelve a 104.x / 172.67.x | Proxy de Cloudflare activo | Pon el registro en **DNS only** (gris) |
| 403 en todo, incluso desde tu IP | Tu IP pública cambió (IP dinámica) o el registro apunta a otro servidor | Verifica tu IP actual en https://ifconfig.me y actualiza `ALLOWED_IPS` en Coolify; confirma que el A apunta a tu servidor |
| Página por defecto de Traefik / 404 | El dominio no está asignado al frontend en Coolify | Asigna `https://lms.jandradee.cloud:8080` al servicio frontend y redeploy |
| Error de certificado / "no seguro" | Let's Encrypt aún no emite | Confirma DNS correcto + puertos 80/443 abiertos y reinicia la app; se emite en minutos |
| 502 Bad Gateway | El backend aún se está construyendo/arrancando | Espera a que ambos contenedores estén "running/healthy" en Coolify |

---

## Parte 2 — Producción en Google Cloud o Azure

### La decisión clave antes de mover nada: SQLite y la nube
La aplicación usa **SQLite en un solo archivo dentro de un volumen persistente**. Eso impone una regla:

- ✅ **Funciona perfecto** en **una sola máquina virtual** con disco persistente (la misma arquitectura que hoy en Coolify). Es la ruta recomendada.
- ❌ **No funciona** en contenedores administrados con varias réplicas (Cloud Run escalando a >1 instancia, Container Apps con réplicas): no hay un archivo compartido fiable, y montar SQLite sobre almacenamiento de red pone en riesgo la base (WAL no es seguro sobre GCS FUSE / shares genéricos).
- Si un día necesitas escalar a muchas instancias, el paso correcto es migrar la base a **PostgreSQL administrado** (Cloud SQL / Azure Database for PostgreSQL). El código ya aísla la configuración de base de datos, así que ese cambio no toca la lógica de negocio — pero hazlo como proyecto aparte, no durante el traslado inicial.

### Ruta recomendada (idéntica en ambas nubes): 1 VM + el mismo Docker Compose
Reutilizas `docker-compose.coolify.yml` tal cual (sin Coolify: `docker compose up -d` directo), agregando un proxy TLS al frente. Costos orientativos (cambian por región; verifícalos al crear): VM pequeña ~US$15–35/mes + disco/snapshots/respaldos ~US$3–8/mes.

#### Google Cloud (Compute Engine)
1. **Proyecto y red:** crea un proyecto (ej. `rgf-lms-prod`), activa facturación y una alerta de presupuesto. VPC por defecto o una propia `lms-vpc`.
2. **IP estática:** reserva una IP externa estática regional y asígnala a la VM (para que el DNS nunca cambie).
3. **Firewall (VPC firewall rules):**
   - `allow-web`: TCP 80 y 443 desde `0.0.0.0/0` (web + emisión de certificados).
   - `allow-admin`: TCP 22 **solo vía IAP** (`35.235.240.0/20` con Identity-Aware Proxy) — no abras SSH a internet.
   - Todo lo demás, denegado por defecto.
4. **VM:** `e2-small` (2 vCPU, 2 GB) o `e2-medium` si habrá muchos videos; Debian 12/Ubuntu 24.04 LTS; disco de arranque 20 GB + **disco persistente adicional de datos** (20–50 GB) montado en `/data` para los volúmenes Docker.
5. **Instala Docker** (docker-ce + compose plugin) y crea el usuario de despliegue con llaves SSH; desactiva login por contraseña.
6. **Código:** sube el proyecto (repo git privado o el zip verificado por SHA-256), coloca el compose y crea el `.env` con los valores de producción. **Secretos en Secret Manager**: guarda ahí `DJANGO_SECRET_KEY` y recupérala en el arranque (script o `gcloud secrets versions access`), no la dejes en texto plano fuera del `.env` protegido con permisos 600.
7. **TLS:** agrega al compose un Traefik o Caddy con el dominio `lms.jandradee.cloud` (o el dominio corporativo final) para Let's Encrypt automático, igual que hace Coolify.
8. **DNS:** en Cloudflare cambia el registro A de `lms` a la IP estática de la VM, **DNS only**, y baja el TTL a 300 s un día antes del corte.
9. **Arranque y verificación:** `docker compose up -d --build`, `/health/` en 200, portada 403 desde una IP ajena y 200/login desde la tuya.
10. **Operación:** actualizaciones de seguridad automáticas del SO (`unattended-upgrades`), reinicio programado de parches, y monitoreo con **Cloud Monitoring**: uptime check cada 5 min sobre `/health/` con alerta a tu correo.

#### Microsoft Azure (Virtual Machine)
1. **Suscripción y grupo de recursos:** `rg-lms-prod` en la región más cercana (ej. East US / Brazil South según latencia a El Salvador); etiqueta de costo y alerta de presupuesto en Cost Management.
2. **Red:** VNet propia, **IP pública estática** (SKU Standard, asignación estática) asociada a la VM.
3. **NSG (equivalente al firewall):**
   - Entrada 80/443 desde Internet.
   - Entrada 22 **solo desde tu IP pública** (201.247.144.9) — o mejor, usa **Azure Bastion** y no abras el 22 en absoluto.
   - Denegar el resto.
4. **VM:** `B2s` (2 vCPU, 4 GB) con Ubuntu 24.04 LTS; disco OS 30 GB + **Azure Disk de datos** montado en `/data` para los volúmenes Docker.
5. **Docker + código + secretos:** igual que en GCP; los secretos van en **Azure Key Vault** y la VM los lee con su identidad administrada (Managed Identity), sin credenciales guardadas.
6. **TLS, DNS y verificación:** idénticos a GCP (Traefik/Caddy, registro A DNS-only, pruebas de 200/403).
7. **Operación:** actualizaciones automáticas (Azure Update Manager), monitoreo con **Azure Monitor** (alerta sobre `/health/` y uso de disco).

### Respaldos (las "tres capas") — obligatorio en producción
Un solo respaldo no es respaldo. Configura las tres capas; entre todas cuestan pocos dólares al mes:

**Capa 1 — Respaldo lógico de la aplicación (diario, dentro de la VM)**
- Cron/systemd timer a las 02:00 que ejecuta, **con la app corriendo** (seguro con WAL):
  `sqlite3 /data/lms_data/db.sqlite3 ".backup '/backup/lms-$(date +%F).db'"`
  y `tar czf /backup/media-$(date +%F).tar.gz` del volumen de archivos/videos.
- Retención local: 7 días. Antes de **cada despliegue**, una copia manual extra con la fecha y la versión.

**Capa 2 — Copia fuera de la VM (diaria)**
- Sincroniza `/backup` a un bucket **en la misma nube pero independiente de la VM**:
  - GCP: bucket de **Cloud Storage** con *versioning* activado y clase que pasa a Nearline/Archive a los 30 días.
  - Azure: cuenta **Blob Storage** con *soft delete* (14–30 días) y versionado, nivel Cool/Archive.
- Regla de ciclo de vida: borrar respaldos de más de 90 días (o la política que definas). Esto te protege si la VM se pierde o se compromete: el respaldo vive en otro servicio, con otra vía de acceso.

**Capa 3 — Snapshot del disco completo**
- GCP: política de **snapshots programados** del disco de datos, diaria, retención 14 días.
- Azure: **Azure Backup** (Recovery Services Vault) para la VM completa, diario, retención 30 días.
- Sirve para recuperar la máquina entera (SO + Docker + datos) en minutos.

**Prueba de restauración (mensual, no negociable)**
Levanta una VM/contenedor temporal, restaura el respaldo **más reciente** de la Capa 2, arranca la app y comprueba `/health/` y un login. Un respaldo que nunca se restauró es una hipótesis, no un respaldo.
**Objetivos sugeridos:** RPO 24 h (máximo un día de datos perdido) y RTO 2 h. Si el negocio exige menos, se sube la frecuencia de la Capa 1 a cada 6 h.

### Seguridad en la nube (además de lo que la app ya trae)
- Mantén `ALLOWED_IPS` con tu IP mientras el login sea usuario/contraseña; al activar Entra ID (siguiente fase de integraciones) evalúas abrirlo.
- Acceso administrativo solo por IAP (GCP) / Bastion o NSG con tu IP (Azure); llaves SSH únicamente, con rotación.
- Secretos solo en Secret Manager / Key Vault, con acceso por identidad administrada y auditoría de lecturas.
- Alertas: uptime de `/health/`, disco >80%, costo/presupuesto, e inicios de sesión administrativos.
- Antes del corte desde Coolify: congela cambios, haz la Capa 1, transfiere base y media verificando **SHA-256**, y deja el Coolify actual encendido 7 días como plan de reversa (si algo falla, el DNS vuelve a la IP anterior en minutos).

### Cuándo dar el salto a la Ruta B (administrada)
Solo si el uso real lo pide (cientos de colaboradores simultáneos, necesidad de alta disponibilidad): migra a PostgreSQL administrado (Cloud SQL / Azure Database for PostgreSQL Flexible Server, ambos con respaldos automáticos y point-in-time restore incluidos) y despliega los contenedores en Cloud Run / Azure Container Apps con mínimo/máximo de réplicas controlado. Es el paso natural **después** de las integraciones con Microsoft 365, no antes.
