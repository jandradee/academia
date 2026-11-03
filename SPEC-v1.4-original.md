# Especificación funcional y técnica

## Plataforma corporativa de capacitación --- Río Grande Foods

**Versión:** 1.4\
**Estado:** Base para desarrollo iterativo con un LLM\
**Plataforma objetivo:** Django (backend) + Vue.js (frontend)\
**Base de datos:** Microsoft SQL Server 2019 (bases LMS_DEV, LMS_TEST y LMS)\
**Control de versiones y CI:** Azure DevOps Repos y Pipelines\
**Idioma del documento:** Español\
**Identidad visual:** Brandbook de Río Grande Foods adjunto

**Historial de cambios:** v1.4 — Docker Compose para desarrollo (Mac) y pruebas (Debian 13), dos cuentas de base por base, bases LMS_DEV y LMS_TEST. v1.3 — cambio de plataforma de ScriptCase a Django + Vue.js con apoyo de TI; versiones propuestas en la sección 4.1; correo por Microsoft Graph pospuesto; ambientes de desarrollo local y prueba en Debian 13; contenedores con Docker Compose para desarrollo y pruebas; dos cuentas de base de datos por base (migración y ejecución); bases LMS_DEV y LMS_TEST confirmadas.

------------------------------------------------------------------------

## 1. Propósito y objetivo

Construir una plataforma web de capacitación
corporativa que permita administrar cursos, módulos, videos, materiales,
evaluaciones, asignaciones y certificados; sincronizar periódicamente
los usuarios activos desde el tenant de Microsoft 365; ofrecer a los
colaboradores un catálogo de cursos; y proporcionar seguimiento,
reportes y métricas de formación.

La solución debe desarrollarse de manera incremental. El LLM debe
implementar únicamente la fase solicitada, respetar las dependencias,
ejecutar las pruebas de aceptación y actualizar la documentación técnica
antes de avanzar.

## 2. Instrucciones obligatorias para el LLM desarrollador

1.  **No generar toda la aplicación en una sola entrega.** Trabajar por
    fases y requisitos trazables.
2.  Antes de programar una fase, revisar el código, la estructura de
    versiones de Python, Django y Node.js, el motor y versión de base de datos,
    el esquema existente y las convenciones del proyecto.
3.  No asumir que existen tablas, campos, bibliotecas, credenciales,
    endpoints, jobs o servicios que no hayan sido
    comprobados.
4.  Si falta una decisión bloqueante, formular preguntas concretas. Si
    no bloquea el trabajo, documentar la decisión como supuesto
    configurable y continuar.
5.  Para cada requisito, entregar: objetivo, cambios de base de datos,
    aplicaciones/archivos afectados, lógica, controles de seguridad,
    pruebas y criterios de aceptación.
6.  Usar consultas parametrizadas/preparadas y el ORM de Django
    cuando corresponda. Evitar SQL concatenado con valores
    proporcionados por el usuario.
7.  No almacenar secretos de Microsoft 365 en el código fuente,
    repositorio ni tablas de configuración accesibles desde la interfaz.
8.  No eliminar físicamente usuarios sincronizados del tenant. Marcar
    como inactivos los usuarios que ya no estén activos o que no
    aparezcan en una sincronización válida, con registro de auditoría.
9.  No interpretar un fallo de Microsoft Graph como una sincronización
    exitosa ni desactivar a todos los usuarios por una respuesta
    incompleta.
10. No declarar un curso aprobado únicamente porque el usuario haya
    abierto un video o descargado un archivo. Aplicar reglas explícitas
    de avance y aprobación.
11. Mantener separación entre lógica de negocio, acceso a datos,
    integración con Microsoft Graph, generación de PDF, correo y
    presentación, mediante módulos y servicios separados en Django y Vue.
12. Implementar cambios pequeños, reversibles y documentados. Incluir
    scripts de migración o instrucciones reproducibles para cambios de
    esquema.
13. Respetar el brandbook adjunto; no recrear, deformar ni recolorear el
    logotipo. Si el archivo original del logo no está disponible como
    recurso independiente, solicitarlo en lugar de reconstruirlo.
14. No inventar resultados de pruebas. Reportar qué pruebas se
    ejecutaron, cuáles pasaron y cuáles quedaron pendientes.
15. No introducir servicios externos de pago ni dependencias nuevas sin
    documentar el motivo, el costo potencial, las alternativas y la
    aprobación requerida.
16. **Seguridad desde el diseño y por defecto:** toda función nueva debe
    identificar amenazas, datos protegidos, permisos, validaciones y
    pruebas de seguridad antes de considerarse terminada.
17. **Prohibido incluir secretos en el código:** no escribir tokens,
    API keys, contraseñas, client secrets, certificados privados,
    cadenas de conexión con credenciales ni claves criptográficas en
    código fuente, SQL, archivos versionados, ejemplos, capturas,
    documentación, logs o mensajes de error.
18. No usar credenciales reales en pruebas, ejemplos o repositorios.
    Los archivos `.env` con valores reales deben excluirse del control de
    versiones; entregar únicamente plantillas sin secretos, por ejemplo
    `.env.example`.
19. Antes de modificar una aplicación existente, identificar riesgos y
    compatibilidad. No desactivar controles de seguridad para hacer que
    una función funcione.
20. La salida a producción requiere una lista de verificación de
    seguridad aprobada, evidencia de pruebas y autorización explícita
    del responsable técnico/negocio. No afirmar que la aplicación es
    segura solo porque compila o funciona en pruebas funcionales.

## 3. Alcance funcional

### Incluido

-   Sincronización programada de usuarios activos de Microsoft 365.
-   Inicio de sesión e identificación del colaborador.
-   Roles y permisos.
-   Administración de cursos y sus estados.
-   Módulos, videos y recursos descargables.
-   Quiz, intentos, calificación y aprobación.
-   Asignación de cursos obligatorios u opcionales a empleados.
-   Catálogo para descubrir cursos e inscribirse cuando esté permitido.
-   Seguimiento del avance por usuario y curso.
-   Certificados PDF y entrega por correo.
-   Inicio del colaborador con horas de capacitación del año calendario.
-   Reportes administrativos de asignación, inicio, avance, finalización
    y horas.
-   Auditoría, parámetros, errores y tareas de administración.

### Fuera de alcance inicial, salvo aprobación posterior

-   Integración con nómina, ERP o sistemas de gestión de desempeño.
-   Videoconferencia en vivo.
-   SCORM/xAPI/LTI.
-   Aplicación móvil nativa.
-   Traducción automática de cursos.
-   Reconocimiento facial o vigilancia de actividad.
-   Seguimiento invasivo del usuario o reproducción forzada de video.
-   Firma electrónica legal de certificados.

## 4. Decisiones técnicas y supuestos que deben validarse

### 4.1 Decisiones confirmadas por el responsable del proyecto

Las siguientes decisiones ya están confirmadas y deben tratarse como requisitos, no como preguntas pendientes:

- **Backend:** Django 5.2 LTS con Python 3.13.x; ScriptCase queda fuera del alcance.
- **Frontend:** Vue.js 3 con Vite.
- **Base de datos:** Microsoft SQL Server 2019 en `192.168.15.19`; bases `LMS_DEV` y `LMS_TEST` para desarrollo y pruebas, y `LMS` para producción (ver ambientes en 4.1).
- **Control de versiones y CI:** Azure DevOps.
- **Correo:** pospuesto; se define en la fase de correo (RT-010).
- **Almacenamiento de videos:** directorio dedicado dentro del servidor de la aplicación. El directorio debe estar fuera del acceso público directo del servidor web cuando sea técnicamente posible; el acceso debe realizarse mediante la aplicación después de validar sesión y permisos. Definir ruta por ambiente, permisos del sistema operativo, cuotas, respaldo y política de retención.
- **Regla de finalización del curso:** el curso se considera completado cuando el colaborador ha consumido más del 95% del contenido requerido (videos y recursos) y ha completado el 100% de todos los quizzes asociados al curso. Si el curso contiene únicamente un video y no tiene otros recursos ni quizzes, se considera completado cuando el colaborador ha reproducido más del 95% de ese video.

#### Interpretación técnica para medir consumo

- **Videos:** registrar progreso de reproducción en el reproductor; el porcentaje se calcula sobre la duración del video, usando la mayor posición reproducida verificada y evitando que adelantar el video sin reproducirlo cuente como consumo. La regla de finalización es estrictamente `> 95%`, no `>= 95%`.
- **Recursos PDF/Word/Excel:** una descarga por sí sola no demuestra que el empleado haya leído el recurso. Para medir consumo superior al 95%, se debe implementar un visor integrado que registre páginas/secciones vistas cuando el formato y la tecnología lo permitan. Para archivos que no puedan instrumentarse de forma fiable, el sistema debe mostrar explícitamente la limitación y usar una regla alternativa aprobada (por ejemplo, marcar como revisado tras abrirlo en un visor controlado); no afirmar que se ha verificado una lectura del 95% si no hay datos que lo prueben.
- **Quizzes:** todos los quizzes obligatorios asociados al curso deben quedar completados al 100%. La aprobación del curso debe aplicar además las reglas de calificación configuradas para cada quiz; completar un intento sin aprobar no equivale a aprobarlo, salvo que el responsable funcional decida expresamente lo contrario.
- **Cursos con un único video:** aplicar la regla específica de más del 95% de reproducción. Si el curso tiene quizzes, estos también deben completarse conforme a la regla general.
- **Cálculo global:** documentar la fórmula y el detalle de cada unidad de contenido en la interfaz, para que el colaborador y el administrador entiendan qué elementos faltan para completar el curso.


Antes de la implementación, confirmar y registrar:

| Decisión | Recomendación / decisión | Validación requerida |
|---|---|---|
| Framework backend | Django 5.2 LTS (5.2.18; soporte de seguridad hasta el 30-abr-2028) | Sí, TI |
| Lenguaje backend | Python 3.13.x (runtime de Debian 13) | Sí, TI |
| Frontend | Vue.js 3.5.x (3.5.44 al 13-oct-2026), Vite, Vue Router y Pinia (versiones a fijar al instalar) | Sí |
| Runtime de build frontend | Node.js 24 LTS (24.22.x) | Sí, TI |
| Base de datos | SQL Server 2019, base LMS existente | Sí |
| Conector Django–SQL Server | mssql-django 2.0.0 (soporta Django 5.2, 6.0 y 6.1) | Sí |
| Driver ODBC | Microsoft ODBC Driver 18 para SQL Server (msodbcsql18) | Sí; compatibilidad con Debian 13 pendiente de confirmar |
| Autenticación | Entra ID con OpenID Connect en el backend (biblioteca MSAL para Python, msal 1.39.0); el backend mantiene los tokens y el navegador recibe solo sesión | Sí |
| Integración M365 | Microsoft Graph, aplicación con certificado y permiso `User.Read.All` (permisos mínimos) | Sí |
| Frecuencia de sincronización | Cada noche, configurable | Sí |
| Almacenamiento multimedia | Directorio privado en el servidor de la aplicación, fuera del acceso público | Sí |
| Correo | Pospuesto; Microsoft Graph `sendMail` o SMTP autorizado, decidir en la fase de correo | Sí, fase 6 |
| Generación de PDF | Por aprobar: ReportLab o WeasyPrint, según licencia, fuentes y soporte de TI | Sí |
| Zona horaria | America/El_Salvador para reportes y fechas | Sí |
| Idioma | Español inicialmente; estructura preparada para localización | Sí |
| Catálogo y visibilidad | Solo usuarios activos autenticados; cursos públicos para la audiencia interna, restringidos o por asignación | Sí |
| Contenedores | Docker Compose para desarrollo y pruebas (Mac y Debian 13). Kubernetes no aplica en este alcance | Aprobado |
| Control de versiones y CI | Azure DevOps Repos y Pipelines; escaneo de secretos en el pipeline | Sí |

**Ambientes (confirmados en v1.4):**
- **Desarrollo:** Mac del responsable, con Docker Compose. Las imágenes deben ser multiarquitectura (Apple Silicon `arm64` y `amd64`).
- **Pruebas:** servidor Debian 13 en la red local, con Docker Compose y el mismo archivo base con un override para pruebas.
- **Producción:** se define en la fase 8, con su propio servidor y base.
- **Base de datos:** SQL Server 2019 en `192.168.15.19`, fuera de los contenedores. Desarrollo usa `LMS_DEV`; pruebas usa `LMS_TEST`. La base `LMS` queda reservada para producción y no se usa para desarrollo ni pruebas.
- **Cuentas de base de datos:** dos cuentas por base de datos, una para migraciones (con permisos de cambio de esquema) y otra para ejecución de la aplicación (solo lectura y escritura de datos). Ninguna de las dos es `sa`.
- **Secretos por ambiente:** `.env` local por ambiente, fuera del repositorio. Solo se versiona `.env.example`.

No dar por hecho que "eliminar un usuario del tenant" significa
necesariamente borrarlo de Microsoft Entra ID. La sincronización debe
definir cómo tratar cuentas deshabilitadas, eliminadas, invitadas,
compartidas y cuentas de servicio.

## 5. Roles y permisos

Aplicar autorización en el servidor para cada operación; ocultar un
botón en la interfaz no constituye control de acceso suficiente.

### 5.1 Administrador de plataforma

-   Gestionar configuración general y roles.
-   Administrar sincronización de usuarios y consultar resultados.
-   Crear, editar, publicar, archivar y retirar cursos.
-   Administrar categorías, módulos, recursos, videos, quizzes y
    certificados.
-   Asignar cursos individualmente, por grupo o mediante selección
    múltiple.
-   Consultar reportes globales y exportarlos según permisos.
-   Consultar bitácora de auditoría y errores técnicos.
-   Reprocesar tareas fallidas con controles para evitar duplicados.

### 5.2 Gestor de cursos

-   Crear y editar cursos según su ámbito autorizado.
-   Administrar contenido, módulos, recursos, videos y evaluaciones.
-   Publicar o enviar a revisión, si se activa un flujo de aprobación.
-   Asignar cursos y consultar el avance de su audiencia autorizada.
-   No puede cambiar configuración de seguridad ni asignar privilegios
    administrativos.

### 5.3 Colaborador / estudiante

-   Consultar su perfil y estado.
-   Ver el catálogo y los detalles de cursos disponibles.
-   Inscribirse en cursos opcionales habilitados.
-   Acceder a cursos obligatorios que le hayan sido asignados.
-   Consumir módulos, videos y recursos.
-   Realizar quizzes y consultar resultados permitidos.
-   Ver su progreso, historial, certificados y horas acumuladas.
-   No puede ver el avance ni los datos personales de otros empleados.

### 5.4 Permisos ampliables

Diseñar el modelo para agregar posteriormente roles como auditor,
supervisor o responsable de área sin reescribir toda la autorización.

## 6. Requisitos funcionales

Cada identificador debe mantenerse en código, documentación, pruebas y
seguimiento de incidencias.

### RF-001 --- Sincronización de usuarios con Microsoft 365

**Prioridad:** Must\
**Dependencias:** RT-001, RT-002, RT-003, RNF-001

-   Conectarse a Microsoft Graph mediante una aplicación registrada en
    Microsoft Entra ID.
-   Leer usuarios del tenant mediante paginación completa; no asumir que
    una sola respuesta contiene todos los registros.
-   Sincronizar al menos: ID inmutable de Entra ID, nombre, apellido si
    está disponible, nombre para mostrar, correo/UPN, departamento,
    cargo, país/sede si está disponible, estado de cuenta y fecha de
    última sincronización.
-   Usar el identificador de Entra ID como clave externa estable; no
    usar el correo como clave primaria.
-   Crear los usuarios nuevos y actualizar los existentes.
-   Marcar como inactivos a usuarios que estén deshabilitados o que no
    aparezcan en una sincronización completa y exitosa, conforme a las
    reglas aprobadas.
-   No borrar físicamente usuarios ni su historial de capacitación.
-   Excluir cuentas de servicio, invitados u otros tipos solo si la
    política aprobada lo especifica.
-   Registrar fecha de inicio y fin, resultado, cantidad leída, creados,
    actualizados, desactivados, omitidos y errores.
-   Gestionar expiración/rotación de credenciales, límites de
    solicitudes, reintentos y errores de Graph.
-   Permitir ejecución manual autorizada y ejecución programada.
-   Prevenir ejecuciones simultáneas o aplicar bloqueo de proceso.
-   La desactivación por ausencia debe ocurrir solo después de comprobar
    que se completaron todas las páginas y que el resultado fue válido.

**Aceptación** 1. Un usuario nuevo del tenant aparece una sola vez en la
plataforma tras una sincronización exitosa. 2. Los cambios de
nombre/correo actualizan el registro sin perder su historial. 3. Una
cuenta deshabilitada se marca inactiva según la política configurada. 4.
Un fallo de Graph no desactiva masivamente a los usuarios. 5. La
ejecución registra métricas, errores y marca de tiempo. 6. Repetir una
sincronización sin cambios no crea duplicados.

### RF-002 --- Autenticación y asociación de identidad

**Prioridad:** Must\
**Dependencias:** RT-004, RF-001, RF-003

-   Autenticar usuarios de forma segura, preferiblemente con Microsoft
    Entra ID si se aprueba.
-   Vincular la identidad autenticada al registro local mediante el ID
    de Entra ID.
-   No permitir acceso a usuarios inactivos, salvo una ruta
    administrativa de recuperación explícitamente autorizada.
-   Implementar cierre de sesión, expiración de sesión y protección
    contra CSRF cuando aplique.
-   No confiar en el correo enviado por el navegador como prueba de
    identidad.

### RF-003 --- Gestión de roles y autorización

**Prioridad:** Must\
**Dependencias:** RT-005, RF-002

-   Administrar roles y asignaciones de rol.
-   Aplicar permisos en servidor por acción, registro y ámbito.
-   Denegar por defecto las acciones no autorizadas.
-   Registrar cambios de roles y permisos en auditoría.
-   Impedir que un gestor de cursos se eleve a administrador.

### RF-004 --- Administración del catálogo de cursos

**Prioridad:** Must\
**Dependencias:** RT-006, RF-003

Cada curso tendrá como mínimo: - ID interno. - Código único opcional o
generado. - Título. - Descripción corta y descripción detallada. -
Categoría o etiquetas. - Tipo: obligatorio u opcional. - Estado:
borrador, publicado, archivado o retirado. - Fecha/hora de
disponibilidad y, opcionalmente, fecha de cierre. - Audiencia o reglas
de visibilidad. - Miniatura, imagen principal y banner. - Duración
estimada en minutos. - Criterio de finalización y aprobación. - Puntaje
mínimo de aprobación si contiene quiz. - Versión del curso y fecha de
última modificación. - Creador, editor y fechas de auditoría.

Funciones: - Crear, editar, previsualizar, publicar, archivar y
retirar. - Validar campos requeridos y límites de archivos. - Evitar
publicar cursos sin contenido mínimo válido. - Conservar historial de
cursos completados aunque el curso se archive. - Definir si una
modificación de contenido exige recursado; registrar versión de
contenido al momento de asignación. - No eliminar permanentemente cursos
que ya tengan asignaciones, intentos o certificados; usar archivo/retiro
lógico.

### RF-005 --- Módulos y estructura del curso

**Prioridad:** Must\
**Dependencias:** RF-004

-   Crear uno o varios módulos por curso.
-   Definir título, descripción, orden y duración estimada.
-   Permitir reordenar módulos.
-   Definir si los módulos deben completarse secuencialmente o si el
    usuario puede navegar libremente.
-   Permitir incluir varios videos y recursos en cada módulo.
-   Configurar reglas de finalización por módulo.
-   Mostrar claramente los módulos completados, pendientes y bloqueados.

### RF-006 --- Videos del curso

**Prioridad:** Must\
**Dependencias:** RF-005, RT-007

-   Permitir cargar uno o varios videos por módulo o asociar un video
    alojado en una plataforma aprobada.
-   Admitir formatos y tamaños configurables, documentados según la
    infraestructura.
-   Validar extensión, MIME real y tamaño; no confiar únicamente en el
    nombre del archivo.
-   Guardar los archivos fuera del directorio público o en
    almacenamiento privado con autorización de acceso.
-   Mostrar título, duración, orden y estado del video.
-   Registrar el avance de reproducción cuando la tecnología lo permita,
    evitando afirmar que el usuario vio el video completo si solo se
    conoce el tiempo del reproductor.
-   Definir si completar un video exige reproducir un porcentaje
    configurable y si el usuario puede continuar después.
-   Proteger URLs y descargas con permisos y enlaces temporales cuando
    corresponda.
-   No servir contenido activo subido por usuarios como HTML ejecutable.

### RF-007 --- Recursos descargables

**Prioridad:** Must\
**Dependencias:** RF-005, RT-007

-   Adjuntar PDF, Word y Excel a un curso o módulo.
-   Permitir nombre visible, descripción, orden, versión y fecha de
    carga.
-   Validar extensión, MIME, tamaño y, si está disponible, análisis
    antimalware.
-   Almacenar archivos de forma privada y verificar autorización antes
    de descargarlos.
-   Registrar descargas solo si la organización considera útil esa
    métrica; una descarga no implica finalización.
-   Permitir sustituir un recurso conservando referencia a versiones
    anteriores si el contenido ya fue utilizado.

### RF-008 --- Quiz y evaluación

**Prioridad:** Must\
**Dependencias:** RF-004, RF-005, RT-008

-   Crear quizzes asociados a un curso o módulo.
-   Configurar título, instrucciones, puntaje mínimo, número máximo de
    intentos, límite de tiempo opcional, aleatorización opcional y
    retroalimentación.
-   Soportar inicialmente preguntas de opción múltiple con una respuesta
    correcta, selección múltiple, verdadero/falso y respuesta corta
    evaluada manualmente si se aprueba.
-   Definir puntaje por pregunta y respuestas correctas.
-   Registrar intento, fecha, respuestas, puntaje, resultado y duración
    cuando aplique.
-   Calcular automáticamente las preguntas objetivas.
-   No mostrar respuestas correctas antes de que la política del quiz lo
    permita.
-   Aplicar reglas de reintento y registrar cada intento sin
    sobrescribir el historial.
-   Aprobar cuando se cumpla el puntaje mínimo y demás condiciones
    configuradas.
-   Mantener trazabilidad de cambios de preguntas que afecten
    evaluaciones previas.

**Aceptación** - Un usuario que alcanza el puntaje mínimo queda
aprobado. - Un usuario que no alcanza el puntaje queda no aprobado y
puede reintentar solo si la configuración lo permite. - Los resultados
previos permanecen consultables para usuarios autorizados. - Las
respuestas se validan en servidor y no se confía en el puntaje enviado
por el navegador.

### RF-009 --- Asignación de cursos

**Prioridad:** Must\
**Dependencias:** RF-001, RF-003, RF-004

-   Asignar un curso a uno o varios empleados mediante búsqueda, filtros
    y selección múltiple.
-   Permitir asignación por departamento, país/sede, grupo de usuarios u
    otra audiencia definida y disponible.
-   Mostrar resumen antes de confirmar la asignación.
-   Permitir definir fecha de vencimiento, obligatoriedad, notificación
    y audiencia.
-   Evitar duplicar asignaciones activas del mismo curso/versión a la
    misma persona.
-   Mantener un registro de quién asignó, cuándo y por qué medio.
-   Permitir retirar/cancelar una asignación con motivo y auditoría; no
    borrar el historial.
-   Definir cómo se tratan nuevas versiones del curso: mantener la
    asignación, requerir recursado o generar nueva asignación.

### RF-010 --- Catálogo e inscripción voluntaria

**Prioridad:** Must\
**Dependencias:** RF-002, RF-004, RF-009

-   Mostrar cursos publicados disponibles para el colaborador.
-   Ofrecer búsqueda, filtros por categoría, modalidad/contenido,
    duración y tipo.
-   Mostrar miniatura, título, descripción, duración estimada, fecha de
    disponibilidad y estado personal.
-   Permitir inscripción a cursos opcionales cuando el curso esté
    habilitado para autoinscripción.
-   Evitar que el usuario se inscriba en cursos fuera de su audiencia o
    no disponibles.
-   Mostrar de forma distinguible los cursos obligatorios asignados y
    los opcionales.
-   Ofrecer vista de detalle con módulos, recursos y criterios de
    finalización.

### RF-011 --- Seguimiento del avance

**Prioridad:** Must\
**Dependencias:** RF-005, RF-006, RF-007, RF-008, RF-009

-   Mostrar avance individual por curso y por módulo.
-   Definir y documentar una fórmula de progreso estable, configurable y
    entendible.
-   Recomendación inicial: calcular el avance por unidades obligatorias
    del curso (módulos, videos, actividades y/o quiz) completadas
    respecto del total requerido. Evitar calcularlo solo por tiempo de
    reproducción.
-   Guardar estado: no iniciado, en progreso, completado, aprobado,
    vencido o cancelado, según reglas de negocio.
-   Registrar fecha de primer inicio, última actividad, fecha de
    finalización y fecha de aprobación.
-   Distinguir finalización de aprobación: un curso puede estar
    completado sin estar aprobado si requiere una evaluación.
-   No permitir que el cliente web modifique directamente su porcentaje
    de avance.
-   Definir cómo se tratan cursos sin quiz y cursos con varios quizzes.
-   Mantener progreso aunque el usuario cierre sesión y vuelva
    posteriormente.

### RF-012 --- Certificados PDF

**Prioridad:** Must\
**Dependencias:** RF-008, RF-011, RT-009

-   Generar un certificado PDF al cumplirse los criterios configurados.
-   Incluir al menos: nombre del colaborador, título del curso, fecha de
    finalización/aprobación, duración reconocida, identificador único
    del certificado y marca Río Grande Foods.
-   Incluir firma o nombre del responsable solo si la organización lo
    define.
-   Generar un identificador verificable que no exponga datos personales
    innecesarios.
-   Guardar registro de emisión, versión de plantilla, archivo generado
    y estado de entrega.
-   Evitar emitir certificados duplicados para la misma finalización,
    salvo reemisión auditada.
-   Permitir descarga desde el perfil del colaborador y desde vistas
    autorizadas.
-   Definir si una reemisión invalida el certificado anterior.
-   El certificado debe utilizar el logotipo original aprobado,
    respetando sus proporciones y área de seguridad.

### RF-013 --- Entrega de certificados y notificaciones por correo

**Prioridad:** Must\
**Dependencias:** RF-012, RT-010

-   Enviar el certificado al correo corporativo vigente del colaborador
    tras su emisión, si la política está habilitada.
-   Enviar notificaciones configurables para asignación de curso,
    recordatorio, vencimiento y finalización.
-   Usar una cola o mecanismo de reintentos para fallos transitorios.
-   Registrar destinatario, tipo, fecha, resultado y error técnico sin
    almacenar contenido sensible innecesario.
-   Evitar envíos duplicados mediante una clave idempotente.
-   No considerar entregado un correo solo porque la solicitud al
    proveedor fue aceptada; distinguir solicitado, aceptado, fallido y
    confirmado cuando el proveedor lo permita.
-   No exponer listas de destinatarios a otros empleados.
-   Respetar las políticas corporativas de correo y límites de envío.

### RF-014 --- Inicio del colaborador y horas de capacitación

**Prioridad:** Must\
**Dependencias:** RF-002, RF-009, RF-011, RF-012

La página inicial debe mostrar: - Cursos obligatorios pendientes. -
Cursos en progreso. - Cursos completados/aprobados. - Próximos
vencimientos. - Certificados disponibles. - Total de horas de
capacitación del año calendario actual. - Acceso al catálogo de cursos.

Reglas de horas: - Definir si las horas se calculan desde duración
estimada aprobada, duración efectiva registrada o duración reconocida
por curso. - Recomendación inicial para métricas consistentes: usar la
duración reconocida configurada para cada curso una sola vez cuando el
colaborador complete/apruebe el curso; mostrar por separado tiempo
efectivo si se recopila. - Contabilizar por año calendario según la
fecha de finalización/aprobación y la zona horaria definida. - No sumar
dos veces reintentos, duplicados o reemisiones de certificados. -
Definir si cursos sin certificado también aportan horas. - Permitir que
el colaborador vea el detalle de cursos que componen el total.

### RF-015 --- Consola administrativa

**Prioridad:** Must\
**Dependencias:** RF-003 y módulos administrativos

Debe ofrecer accesos según permisos a: - Cursos, categorías, módulos,
videos y recursos. - Quizzes, preguntas e intentos. - Usuarios
sincronizados, estado y última sincronización. - Asignaciones,
inscripciones y progreso. - Certificados y cola de correo. - Reportes. -
Configuración de reglas de avance, aprobación, duración y
notificaciones. - Auditoría y diagnóstico de tareas.

Las operaciones destructivas deben requerir confirmación, explicar el
impacto y preferir archivado/cancelación lógica sobre borrado físico.

### RF-016 --- Reportes de seguimiento

**Prioridad:** Must\
**Dependencias:** RF-001, RF-009, RF-011

Permitir filtrar por curso, estado, empleado, departamento, país/sede,
gestor, fecha de asignación, fecha de vencimiento y periodo.

Mostrar como mínimo: - Personas asignadas. - Personas que no han
iniciado. - Personas en progreso y porcentaje actual. - Personas que
completaron. - Personas que aprobaron o no aprobaron. - Personas
vencidas. - Fecha de primer inicio, última actividad y finalización. -
Horas reconocidas por empleado en el año calendario. - Tasa de inicio,
finalización y aprobación por curso.

Los reportes deben distinguir "no iniciado" de "sin actividad reciente".
Permitir exportar CSV/XLSX si la política de datos lo autoriza. Aplicar
permisos y registrar exportaciones de reportes sensibles.

### RF-017 --- Auditoría

**Prioridad:** Must\
**Dependencias:** RF-003

Registrar de forma consultable: - Inicio/cierre de sesión relevante y
eventos de seguridad disponibles. - Creación, edición, publicación,
archivo y retiro de cursos. - Cambios de preguntas y reglas de
aprobación. - Asignaciones, cancelaciones y cambios de vencimiento. -
Cambios de roles. - Emisión y reemisión de certificados. -
Sincronizaciones con Microsoft 365. - Exportaciones administrativas
relevantes. - Cambios de configuración.

Cada evento debe incluir actor, fecha/hora, acción, entidad,
identificador, resultado y contexto mínimo necesario. No guardar
contraseñas, tokens ni secretos en bitácoras.

### RF-018 --- Búsqueda, filtros y usabilidad

**Prioridad:** Should

-   Incluir paginación y filtros en tablas grandes.
-   Mantener filtros al navegar entre páginas cuando sea razonable.
-   Proveer estados vacíos, mensajes de error accionables y
    confirmaciones.
-   Evitar formularios extensos sin agrupación.
-   Permitir navegación por teclado y etiquetas accesibles.
-   Mostrar fechas, porcentajes y duraciones de forma consistente.

### RF-019 --- Gestión de errores y tareas en segundo plano

**Prioridad:** Must

-   Implementar registro centralizado de errores sin datos sensibles.
-   Diferenciar errores recuperables y no recuperables.
-   Proveer estado de ejecución para sincronización, generación de
    certificados y correos.
-   Usar reintentos limitados con espera incremental cuando proceda.
-   Evitar duplicar certificados, asignaciones o correos al reintentar.
-   Proporcionar una forma segura de consultar tareas fallidas y
    reejecutarlas.

### RF-020 --- Retención y ciclo de vida de datos

**Prioridad:** Must

-   Conservar historial de capacitación de usuarios inactivos.
-   Definir política de retención para videos, recursos, intentos, logs
    y certificados.
-   Evitar borrado físico accidental de datos referenciados.
-   Permitir anonimización o eliminación conforme a la política
    legal/corporativa, con autorización y auditoría.
-   Documentar respaldos, recuperación y pruebas de restauración.

## 7. Requisitos no funcionales

### RNF-001 --- Seguridad

La seguridad debe aplicarse en el diseño, desarrollo, configuración,
pruebas, despliegue y operación. Usar como referencia un enfoque basado
 en OWASP ASVS/Top 10 y controles equivalentes de seguridad corporativa,
verificando su aplicabilidad al stack real. No afirmar conformidad
formal sin una evaluación documentada.

#### RNF-001.1 --- Secretos, tokens y credenciales

- Prohibido codificar secretos en Python, plantillas, SQL,
  JavaScript, HTML, archivos de configuración versionados, scripts de
  despliegue, imágenes de contenedor, repositorios o documentación.
- No guardar secretos en tablas de configuración accesibles desde la
  aplicación ni permitir que se consulten o editen desde la consola web.
- Usar preferentemente un gestor de secretos aprobado por TI. Si no
  existe, usar variables de entorno protegidas o un archivo de
  configuración fuera del directorio web, con permisos mínimos del
  sistema operativo y acceso limitado a la cuenta de servicio. No
  considerar una variable de entorno por sí sola como almacén seguro si
  administradores o procesos no autorizados pueden leerla.
- Entregar solo nombres de variables y archivos de ejemplo sin valores
  reales (por ejemplo, `.env.example`). Asegurar que `.env`, claves,
  certificados privados, respaldos de configuración y archivos locales
  con credenciales estén excluidos del repositorio.
- Microsoft Graph: preferir identidad administrada cuando la
  infraestructura lo soporte; de lo contrario, usar una aplicación de
  Entra ID con certificado o credencial de federación cuando sea viable.
  Si la organización requiere client secret, guardarlo fuera del código,
  limitar su vigencia y rotarlo según política corporativa. No registrar
  el token de acceso ni el refresh token en la base de datos ni en logs.
- Solicitar permisos de Graph mínimos, preferir permisos de aplicación
  específicos, justificar cada permiso y documentar el consentimiento
  administrativo. No usar permisos amplios como `Directory.ReadWrite.All`
  si la función solo requiere lectura.
- Rotar y revocar credenciales expuestas inmediatamente. Incluir un
  procedimiento para rotación, expiración y revocación, sin interrumpir
  indebidamente la operación.
- Mantener secretos distintos por desarrollo, pruebas y producción; no
  copiar credenciales de producción a ambientes inferiores.
- La cadena de conexión SQL Server debe residir en configuración
  protegida. Usar una cuenta de base de datos dedicada, permisos mínimos
  por esquema/operación y, cuando sea viable, separar cuenta de
  migración de cuenta de ejecución. No usar `sa` ni cuentas
  administradoras desde la aplicación.
- Revisar el repositorio y los artefactos antes de cada entrega con un
  escáner de secretos. No basta con borrar un secreto del último commit:
  si fue expuesto, tratarlo como comprometido y rotarlo.

#### RNF-001.2 --- Identidad, autenticación y sesión

- Preferir Microsoft Entra ID / OpenID Connect para inicio de sesión
  interactivo si el tenant lo permite. Usar bibliotecas y
  flujos mantenidos y aprobados; no implementar criptografía ni flujos
  de autenticación propios.
- Validar firma, emisor, audiencia, expiración, `state`, `nonce` y
  redirect URI de acuerdo con el protocolo y biblioteca adoptados.
  No confiar en correo o nombre de usuario como identificador único:
  asociar la cuenta al identificador inmutable del tenant y del usuario.
- Aplicar MFA y políticas de acceso condicional mediante Entra ID cuando
  la política corporativa lo requiera y la licencia/configuración lo
  permita.
- Regenerar el ID de sesión después de autenticar o elevar privilegios;
  invalidar sesiones al cerrar sesión, desactivar al usuario o detectar
  cambios de seguridad pertinentes. Configurar expiración por
  inactividad y duración máxima.
- Cookies de sesión `Secure`, `HttpOnly` y `SameSite` apropiado; usar
  HTTPS en todo el sitio y HSTS cuando el dominio y despliegue estén
  preparados. No colocar tokens de acceso en URLs ni en `localStorage`.
- Proteger formularios y acciones de cambio contra CSRF; aplicar
  validación de origen cuando corresponda y no depender solo de ella.
- Prevenir fuerza bruta y abuso de autenticación con limitación de
  intentos, demoras o bloqueo proporcional y monitoreo, evitando revelar
  si una cuenta existe.

#### RNF-001.3 --- Autorización y aislamiento de datos

- Denegar por defecto y autorizar en el servidor cada acción, recurso,
  archivo, exportación, API y registro. Ocultar botones no es control de
  acceso.
- Aplicar RBAC con permisos explícitos y comprobar pertenencia y ámbito
  de cada recurso en todas las solicitudes. Prevenir IDOR/BOLA cuando se
  cambian IDs de cursos, usuarios, intentos, certificados o archivos.
- Los estudiantes solo pueden acceder a su propio progreso, resultados
  y certificados; los gestores solo a los cursos y audiencias que les
  corresponden. Restringir exportaciones y datos de otros empleados.
- Separar tareas administrativas de las funciones normales; requerir
  autorización reforzada para cambios de roles, permisos, configuración
  de integración y acciones masivas.
- No confiar en roles, puntajes, progreso, duración de video, usuario o
  estado de aprobación enviados por el navegador. Recalcular y validar
  todo dato crítico en servidor.

#### RNF-001.4 --- Aplicación web y datos

- Usar consultas parametrizadas/preparadas; escapar salida según el
  contexto HTML/JavaScript/URL y validar entradas con listas permitidas
  cuando proceda. Evitar construir SQL con concatenación de datos del
  usuario.
- Implementar protección CSRF, XSS, SQL injection, path traversal,
  SSRF cuando haya solicitudes salientes configurables, open redirect,
  clickjacking y asignación masiva insegura. Configurar CSP y cabeceras
  HTTP de seguridad compatibles con la aplicación.
- Validar en servidor tipos, formatos, longitudes, rangos, límites,
  estados y transiciones de negocio. Normalizar nombres de archivo y
  no construir rutas de almacenamiento con rutas enviadas por usuarios.
- Cifrar en tránsito todas las conexiones, incluidos navegador-servidor,
  aplicación-SQL Server, Graph y servicios de correo. Verificar
  certificados TLS; no deshabilitar la validación de certificados.
- Evaluar cifrado en reposo para base de datos, volúmenes, respaldos y
  archivos, conforme a capacidades y política corporativa. Proteger y
  separar las claves de cifrado.
- Minimizar datos personales. Definir retención, eliminación segura,
  acceso a exportaciones y tratamiento de solicitudes de privacidad de
  acuerdo con políticas aplicables de la empresa.
- No incluir datos sensibles, tokens, contraseñas, contenido de
  documentos o información personal innecesaria en logs, URLs o
  mensajes de error.

#### RNF-001.5 --- Archivos, videos y cargas

- Guardar videos y recursos en almacenamiento no público, fuera del
  directorio web cuando sea posible. Servirlos mediante un controlador
  que valide sesión, autorización, estado del curso y acceso al recurso.
- Aplicar allowlist de extensiones y MIME, comprobar firma real del
  archivo, limitar tamaño/cantidad, renombrar con identificadores
  internos y evitar ejecución de contenido cargado. No confiar solo en
  extensión o `Content-Type` del cliente.
- Analizar archivos con antimalware cuando la infraestructura lo
  permita. Poner archivos en cuarentena hasta finalizar validación.
- Desactivar ejecución de scripts en directorios de carga; aplicar
  permisos mínimos del sistema operativo, cuotas y límites de disco.
  Proteger contra path traversal y sobrescritura de archivos.
- Para descargas, definir `Content-Disposition`, `X-Content-Type-Options`
  y políticas de caché apropiadas. No exponer rutas físicas ni nombres
  internos. Evitar que certificados o documentos se puedan enumerar por
  URL.
- Definir límites de tamaño y tiempos para uploads y descargas, política
  de retención, respaldo y restauración; monitorizar uso de disco.

#### RNF-001.6 --- Infraestructura, configuración y despliegue

- Separar desarrollo, pruebas/staging y producción, con credenciales,
  datos y permisos independientes. No probar cambios directamente en
  producción; usar datos sintéticos o anonimizados.
- Mantener Python, Django, Node.js, dependencias, sistema operativo, servidor web,
  drivers y dependencias en versiones soportadas y parcheadas. Eliminar
  extensiones, módulos, cuentas de ejemplo, endpoints de diagnóstico y
  archivos de instalación que no se necesiten.
- Deshabilitar DEBUG de Django, errores detallados y display de excepciones en
  producción; mantener logs de servidor protegidos, con rotación y
  retención definida. Nunca mostrar stack traces, rutas internas,
  consultas SQL, secretos o detalles de infraestructura al usuario.
- Configurar servidor web con TLS, métodos HTTP mínimos, límites de
  petición, timeouts, permisos de archivos y directorios correctos,
  protección de archivos ocultos y directorios de respaldo. Restringir
  paneles administrativos por autorización y, si procede, red/VPN.
- Restringir conectividad de red al mínimo necesario; no exponer SQL
  Server a Internet. Aplicar firewall, segmentación y reglas de entrada
  y salida aprobadas.
- Versionar cambios y migraciones sin secretos; revisar código por pares
  o revisión independiente antes de producción. Usar análisis estático,
  análisis de dependencias y escaneo de secretos cuando sea posible.
- Preparar despliegue repetible, aprobación, copia de seguridad previa,
  plan de reversión y comprobaciones posteriores al despliegue.

#### RNF-001.7 --- Registro, monitoreo e incidentes

- Registrar accesos administrativos, cambios de rol, publicación de
  cursos, exportaciones, acciones masivas, sincronizaciones, cambios de
  configuración y eventos de seguridad con fecha UTC/local definida,
  actor, acción, resultado y correlación.
- Los logs deben estar protegidos contra acceso/modificación no
  autorizados y no deben contener contraseñas, tokens, cookies,
  secretos, datos de autenticación ni contenido innecesario.
- Alertar sobre errores repetidos de autenticación, cambios inesperados
  de privilegios, fallos de sincronización, agotamiento de disco,
  credenciales próximas a expirar y anomalías relevantes.
- Documentar responsables y pasos de respuesta ante exposición de
  secretos, cuenta comprometida, malware, pérdida de datos o indisponibilidad.
  Incluir revocación de credenciales, preservación de evidencias y
  comunicación conforme a los procesos corporativos.

#### RNF-001.8 --- Calidad y criterios mínimos de seguridad

- Mantener un modelo de amenazas simple y actualizado para autenticación,
  roles, Microsoft Graph, archivos, quizzes, certificados, reportes y
  administración.
- Ejecutar análisis estático, revisión de dependencias, escaneo de
  secretos y pruebas de seguridad antes de producción, en la medida que
  las herramientas aprobadas lo permitan.
- Corregir vulnerabilidades críticas y altas antes de la salida. Toda
  excepción debe documentar justificación, controles compensatorios,
  responsable y aceptación explícita del riesgo con fecha de expiración.
- No prometer “riesgo cero” ni certificar seguridad sin pruebas. La meta
  es reducir el riesgo con controles verificables, evidencias y operación
  continua.

### RNF-002 --- Privacidad y minimización

-   Recopilar solo datos de usuarios necesarios para capacitación.
-   Limitar reportes de avance a personas autorizadas.
-   Documentar finalidad, acceso y retención de datos.
-   No recopilar actividad innecesaria del dispositivo ni datos
    personales ajenos al objetivo.

### RNF-003 --- Rendimiento y escalabilidad

-   Paginación en listados.
-   Índices en claves externas, estados, fechas y relaciones de reporte.
-   Procesar sincronización, PDFs y envíos masivos fuera de solicitudes
    web largas cuando sea posible.
-   Definir metas de rendimiento después de conocer el volumen esperado
    de usuarios, cursos y archivos.
-   Evitar cargar todos los videos o usuarios en memoria
    simultáneamente.

### RNF-004 --- Disponibilidad y recuperación

-   Definir RPO/RTO con TI.
-   Incluir respaldo de base de datos, archivos y configuración.
-   Probar restauración y recuperación de tareas.
-   Las fallas de correo o Graph no deben bloquear la navegación normal
    de la plataforma.

### RNF-005 --- Compatibilidad y mantenibilidad

-   Compatible con versiones soportadas de Django, Python, Node.js, base de
    datos y navegadores corporativos aprobados.
-   Código y configuración documentados.
-   Migraciones reproducibles y controladas.
-   Separar configuración por ambiente (desarrollo, pruebas y
    producción).
-   No usar datos reales en pruebas salvo autorización.

### RNF-006 --- Accesibilidad y experiencia de usuario

-   Contraste suficiente, navegación por teclado y etiquetas claras.
-   Diseño adaptable a escritorio, tableta y móvil.
-   Indicadores de estado no dependientes exclusivamente del color.
-   Mensajes en español claro, cálidos y profesionales, coherentes con
    la marca.

### RNF-007 --- Observabilidad

-   Logs estructurados con identificador de correlación para tareas.
-   Métricas de sincronización, fallos de correo, generación PDF y
    duración de procesos.
-   Alertas para fallos repetidos, credenciales próximas a expirar y
    tareas detenidas, si la infraestructura lo permite.

## 8. Identidad visual basada en el Brandbook de Río Grande Foods

La siguiente guía deriva del brandbook adjunto, especialmente las
secciones de personalidad, arquitectura de marca, tipografías y paleta
cromática.

### 8.1 Personalidad y tono

La marca se define como cálida, acogedora, auténtica, artesanal y
generadora de comunidad. El lenguaje de la interfaz debe ser claro,
sencillo, cercano y profesional. Puede inspirar sensación de conexión y
pertenencia sin convertir una herramienta corporativa en un sitio de
comercio electrónico.

### 8.2 Paleta de color

Usar los siguientes valores del brandbook como tokens de diseño:

  -----------------------------------------------------------------------
  Token                   HEX                     Uso sugerido en la
                                                  plataforma
  ----------------------- ----------------------- -----------------------
  Azul institucional      `#003D7C`               Navegación,
                                                  encabezados, enlaces y
                                                  acciones principales

  Amarillo marca          `#F1CF00`               Acentos, progreso,
                                                  selección y llamadas de
                                                  atención; comprobar
                                                  contraste

  Beige complementario    `#C7B99A`               Fondos secundarios,
                                                  separadores y
                                                  superficies suaves

  Rojo complementario     `#BF0811`               Errores, alertas
                                                  críticas y acciones
                                                  destructivas con
                                                  moderación

  Blanco                  `#FFFFFF`               Fondos y texto según
                                                  contraste

  Gris neutro             Elegir accesible y      Texto secundario,
                          documentar              bordes y fondos neutros
  -----------------------------------------------------------------------

No usar el amarillo como color de texto pequeño sobre blanco si no
alcanza contraste accesible. Validar todos los estados con contraste
suficiente.

### 8.3 Logotipo

-   Utilizar únicamente el archivo original aprobado.
-   Mantener proporciones, composición, colores y placa del logo.
-   Respetar zona de seguridad.
-   No agregar contornos, inclinar, estirar, recrear ni alterar
    tipografía o colores.
-   Sobre fondos azules, utilizar solo una versión autorizada con
    contraste apropiado.
-   No colocar contenido cerca del logotipo que compita con su área de
    resguardo.

### 8.4 Tipografía

El brandbook especifica familias como DIN Next LT Pro, Cocogoose y
Lancaste Script Demo para usos de marca concretos. Para una interfaz
web, comprobar primero licencias y disponibilidad de archivos web. No
imitar fuentes propietarias si no están licenciadas. Si no se dispone de
las fuentes autorizadas, seleccionar una alternativa sans-serif legible
y documentarla. Priorizar legibilidad de tablas, formularios y textos
extensos sobre usos decorativos.

### 8.5 Composición y recursos gráficos

-   Favorecer composiciones equilibradas, limpias y centradas donde
    corresponda.
-   Utilizar tarjetas de cursos con miniaturas y jerarquía clara de
    título, descripción y estado.
-   Las imágenes de cursos deben ser realistas, cálidas y pertinentes al
    contenido, sin interferir con la legibilidad.
-   Usar patrones o ilustraciones inspiradas en la marca solo si se
    dispone de recursos autorizados; no improvisar ni copiar recursos
    gráficos protegidos del brandbook.
-   No aplicar tramas densas detrás de texto operativo.
-   Mantener consistencia entre catálogo, dashboard, administración,
    reportes y certificados.

### 8.6 Componentes recomendados

-   Barra superior con marca y perfil.
-   Navegación lateral para administración.
-   Tarjetas de cursos.
-   Indicadores de progreso con porcentaje y etiqueta textual.
-   Tablas con filtros y paginación.
-   Alertas claras y accesibles.
-   Formularios agrupados por secciones.
-   Certificado PDF con jerarquía sobria, logo original, azul
    institucional y acento amarillo.

## 9. Modelo de datos lógico propuesto

El LLM debe adaptar nombres y tipos al motor existente. Este modelo es
conceptual, no un script SQL definitivo.

### Entidades principales

1.  **users**
    -   `id`
    -   `entra_object_id` (único, no nulo para usuarios sincronizados)
    -   `display_name`, `given_name`, `surname`
    -   `email`, `user_principal_name`
    -   `department`, `job_title`, `office_location` u otros atributos
        aprobados
    -   `is_active`
    -   `last_synced_at`, `created_at`, `updated_at`
2.  **roles**
    -   `id`, `code`, `name`, `description`
3.  **user_roles**
    -   `user_id`, `role_id`, `assigned_by`, `assigned_at`
4.  **courses**
    -   `id`, `code`, `title`, `short_description`, `description`,
        `category_id`
    -   `course_type` (obligatorio/opcional)
    -   `status` (borrador/publicado/archivado/retirado)
    -   `available_from`, `available_until`
    -   `thumbnail_file_id`, `image_file_id`, `banner_file_id`
    -   `estimated_duration_minutes`, `recognized_duration_minutes`
    -   `pass_score`, `completion_policy`, `audience_policy`
    -   `version`, `created_by`, `updated_by`, `created_at`,
        `updated_at`
5.  **course_categories**
    -   `id`, `name`, `description`, `sort_order`, `is_active`
6.  **course_modules**
    -   `id`, `course_id`, `title`, `description`, `sort_order`,
        `estimated_duration_minutes`, `completion_rule`
7.  **videos**
    -   `id`, `module_id`, `title`, `description`, `storage_key` o
        referencia aprobada
    -   `duration_seconds`, `sort_order`, `is_required`, `created_at`
8.  **course_resources**
    -   `id`, `module_id` o `course_id`, `title`, `description`,
        `storage_key`, `mime_type`, `size_bytes`, `version`, `is_active`
9.  **quizzes**
    -   `id`, `course_id` o `module_id`, `title`, `instructions`,
        `pass_score`, `max_attempts`, `time_limit_seconds`, `is_active`,
        `version`
10. **quiz_questions**
    -   `id`, `quiz_id`, `question_type`, `question_text`, `points`,
        `sort_order`, `is_required`
11. **quiz_options**
    -   `id`, `question_id`, `option_text`, `is_correct`, `sort_order`
12. **quiz_attempts**
    -   `id`, `quiz_id`, `user_id`, `started_at`, `submitted_at`,
        `score`, `passed`, `attempt_number`, `duration_seconds`,
        `course_version`
13. **quiz_answers**
    -   `id`, `attempt_id`, `question_id`, `selected_option_id` o
        respuesta normalizada, `points_awarded`
14. **course_assignments**
    -   `id`, `course_id`, `course_version`, `user_id`, `assigned_by`,
        `assigned_at`
    -   `due_at`, `is_mandatory`, `status`, `cancelled_at`,
        `cancellation_reason`
15. **course_enrollments**
    -   `id`, `course_id`, `course_version`, `user_id`, `enrolled_at`,
        `enrollment_source`, `status`
16. **course_progress**
    -   `id`, `course_id`, `course_version`, `user_id`, `status`,
        `progress_percent`
    -   `first_started_at`, `last_activity_at`, `completed_at`,
        `passed_at`
    -   Índice único apropiado por usuario, curso, versión y contexto de
        asignación/inscripción.
17. **module_progress**
    -   `id`, `module_id`, `user_id`, `status`, `progress_percent`,
        `started_at`, `completed_at`
18. **video_progress**
    -   `id`, `video_id`, `user_id`, `last_position_seconds`,
        `max_position_seconds`, `completed_at`, `updated_at`
19. **certificates**
    -   `id`, `certificate_uuid`, `user_id`, `course_id`,
        `course_version`
    -   `issued_at`, `completion_date`, `recognized_duration_minutes`,
        `file_key`, `status`, `template_version`
20. **notification_queue**
    -   `id`, `user_id`, `notification_type`, `idempotency_key`,
        `payload_reference`
    -   `status`, `attempt_count`, `next_attempt_at`, `sent_at`,
        `last_error`
21. **sync_runs**
    -   `id`, `started_at`, `finished_at`, `status`, `users_read`,
        `users_created`, `users_updated`, `users_deactivated`,
        `errors_summary`
22. **audit_logs**
    -   `id`, `actor_user_id`, `action`, `entity_type`, `entity_id`,
        `occurred_at`, `result`, `correlation_id`, `details_redacted`
23. **file_assets**
    -   `id`, `storage_key`, `original_name`, `mime_type`, `size_bytes`,
        `sha256`, `uploaded_by`, `created_at`, `status`
24. **app_settings**
    -   Parámetros no secretos, validados y auditables. No guardar
        secretos de Graph/correo aquí salvo que el mecanismo de
        almacenamiento esté diseñado y aprobado específicamente para
        secretos.

### Reglas de integridad

-   Usar claves foráneas donde el motor lo permita.
-   Agregar restricciones únicas para IDs externos, asignaciones
    activas, certificados e idempotencia.
-   Definir índices para búsquedas por curso, usuario, estado y fechas.
-   Usar borrado lógico para cursos, usuarios sincronizados y registros
    históricos.
-   Documentar cómo se calcula el avance y las horas reconocidas.

## 10. Integraciones y dependencias

### RT-001 --- Microsoft Entra ID / Microsoft Graph

-   Tenant ID.
-   Registro de aplicación y credenciales de aplicación o identidad
    administrada, según entorno.
-   Permisos de Graph mínimos aprobados y consentimiento administrativo.
-   Para listar usuarios, evaluar `User.Read.All` de tipo aplicación u
    otro permiso que Microsoft documente como suficiente en el momento
    de implementación.
-   Definir si se necesitan grupos de Entra ID; los permisos para grupos
    pueden ser distintos.
-   Gestionar paginación, throttling, reintentos, expiración y rotación
    de credenciales.
-   Validar los permisos exactos en documentación vigente de Microsoft
    antes de producción.

### RT-002 --- Planificador de tareas

-   Cron, tarea programada del servidor o mecanismo corporativo
    compatible.
-   Ejecución CLI/segura recomendada para sincronizaciones largas.
-   Cron o systemd timer en el Debian de la aplicación. Si no se puede,
    documentar una alternativa fiable sin depender de que un usuario abra
    la aplicación.

### RT-003 --- Base de datos

-   Dos cuentas de servicio por base de datos: migración y ejecución, con privilegios mínimos.
-   Backups y recuperación aprobados.
-   Migraciones de esquema versionadas.

### RT-004 --- Autenticación

-   Configuración de Microsoft Entra ID/OIDC si se aprueba.
-   URLs de redirección por ambiente.
-   Validación de issuer, audience, nonce/state y expiración según
    biblioteca utilizada.
-   Mapeo seguro a usuario local.

### RT-005 --- Seguridad y roles

-   Tablas de permisos/roles.
-   Política para alta inicial de administradores, sin rol administrador
    asignado automáticamente a todos.

### RT-006 --- Stack Django + Vue y ambientes

-   Servidores Debian 13 de pruebas y producción, con responsables
    identificados. Desarrollo corre en Mac con Docker Compose.
-   Docker Compose para desarrollo y pruebas; no se usa Kubernetes en
    este alcance.
-   Versiones de Python, Django, Node.js, Vue, driver ODBC y dependencias
    aprobadas por TI y registradas en el repositorio.
-   Convenciones de despliegue, migraciones y control de versiones en
    Azure DevOps.
-   Política de actualizaciones de seguridad para dependencias.

### RT-007 --- Almacenamiento de archivos y video

-   Espacio privado de almacenamiento.
-   Cuotas, límites de tamaño, respaldo, antivirus y política de
    retención.
-   Almacenamiento confirmado: directorio privado en el servidor de la
    aplicación (sección 4.1).
-   Evitar acceso público anónimo. Usar autorización, proxy de descarga
    o URLs temporales según solución.

### RT-008 --- Evaluación

-   Reglas aprobadas de preguntas, intentos, calificación, retención y
    revisión manual.
-   Política de accesibilidad y experiencia de evaluación.

### RT-009 --- Generación de PDF

-   Biblioteca PDF compatible con Python/Django y aprobada por TI.
-   Fuentes autorizadas y recurso del logotipo original.
-   Plantilla versionada y pruebas con caracteres acentuados, nombres
    largos y paginación.

### RT-010 --- Correo

**Estado:** pospuesto. La configuración de Microsoft Graph `sendMail` o SMTP se define en la fase de correo.

-   Servicio corporativo autorizado: SMTP autenticado o Microsoft Graph
    `sendMail`.
-   Remitente aprobado, límites, política antispam y seguimiento de
    errores.
-   Plantillas de correo revisadas por la empresa.

### RT-011 --- Seguridad de archivos

-   Validación MIME real, tamaño, nombres de archivo seguros y análisis
    antimalware si está disponible.
-   Política de descarga y retención.

### RT-012 --- Operación

-   Ambientes separados de desarrollo, pruebas y producción.
-   Certificados TLS.
-   Monitoreo, logs, respaldo y procedimiento de recuperación.
-   Responsable técnico y responsable funcional identificados.

## 11. Fases de implementación iterativa

Las fases deben completarse en orden, salvo que una dependencia se
apruebe explícitamente en otro orden.

### Fase 0 --- Descubrimiento y línea base

**Objetivo:** entender el entorno antes de modificarlo.

Entregables: - Inventario de versiones de Python, Django, Node.js, Vue,
SQL Server, driver ODBC y Debian 13. - Diagrama de arquitectura y flujo de autenticación. -
Confirmación de almacenamiento, correo, jobs y seguridad. - Decisiones
abiertas y riesgos. - Propuesta de estructura del proyecto y estrategia
de migraciones. - Matriz de trazabilidad RF/RNF/RT. - Confirmación de
los archivos oficiales de logo y fuentes.

Criterio de salida: las decisiones que bloquean la primera versión están
resueltas o registradas con responsable y fecha.

### Fase 1 --- Fundación, base de datos y seguridad

**Incluye:** RT-003, RT-005, RT-006, RNF-001, RF-003 parcial, RF-017
base.

Entregables: - Modelo de datos inicial y migraciones. - Configuración
por ambiente. - Manejo seguro de errores y auditoría. - Roles y permisos
mínimos. - Aplicación administrativa inicial protegida.

Criterio de salida: las migraciones se ejecutan y revierten de forma
documentada en ambiente de pruebas; pruebas de permisos pasan.

### Fase 2 --- Sincronización y acceso de usuarios

**Incluye:** RF-001, RF-002, RT-001, RT-002, RT-004.

Entregables: - Registro de aplicación y guía de permisos Graph. -
Sincronización completa, paginación y manejo de errores. - Job
programado y ejecución manual autorizada. - Panel de estado y auditoría
de sincronización. - Asociación segura entre identidad y usuario local.

Criterio de salida: pruebas con usuarios nuevos, modificados,
deshabilitados, errores de Graph y ejecución repetida sin duplicados.

### Fase 3 --- Cursos y administración de contenido

**Incluye:** RF-004, RF-005, RF-006, RF-007, RF-015 parcial, RT-007,
RT-011.

Entregables: - CRUD de cursos, categorías y módulos. - Carga y
protección de imágenes, videos y recursos. - Estados de
borrador/publicado/archivado. - Validaciones y controles de archivos. -
Diseño visual base de acuerdo con el brandbook.

Criterio de salida: un gestor autorizado puede crear, previsualizar y
publicar un curso con módulos, videos y recursos; un usuario no
autorizado no puede acceder a los archivos.

### Fase 4 --- Quiz y reglas de finalización

**Incluye:** RF-008, RF-011 parcial, RT-008.

Entregables: - Editor de quizzes y preguntas. - Motor de intentos,
calificación y aprobación. - Registro histórico. - Reglas configurables
de finalización. - Pruebas de seguridad para manipulación de puntaje.

Criterio de salida: pruebas de aprobación, reprobación, límite de
intentos, reintentos y persistencia de respuestas pasan.

### Fase 5 --- Asignación, catálogo y experiencia del estudiante

**Incluye:** RF-009, RF-010, RF-011, RF-014 parcial.

Entregables: - Asignación individual y múltiple. - Catálogo y detalle
del curso. - Autoinscripción de cursos opcionales. - Vista de
aprendizaje y seguimiento del avance. - Página inicial del colaborador.

Criterio de salida: la asignación genera una única relación válida; el
usuario solo ve cursos autorizados y su avance persiste al cerrar
sesión.

### Fase 6 --- Certificados y notificaciones

**Incluye:** RF-012, RF-013, RT-009, RT-010.

Entregables: - Plantilla de certificado alineada al brandbook. -
Generación de PDF e identificador único. - Descarga de certificado. -
Cola de correo y reintentos idempotentes. - Historial de entregas.

Criterio de salida: un curso aprobado produce un certificado correcto
una sola vez y el fallo de correo puede reintentarse sin duplicar
emisión.

### Fase 7 --- Reportes y métricas

**Incluye:** RF-014, RF-016.

Entregables: - Reporte de no iniciados, en progreso, completados,
aprobados, reprobados y vencidos. - Reporte de horas por empleado y año
calendario. - Filtros y exportación autorizada. - Validación de cifras
contra datos de prueba.

Criterio de salida: los conteos y horas coinciden con los casos de
prueba aprobados por el responsable funcional.

### Fase 8 --- Endurecimiento y salida a producción

**Incluye:** RF-018, RF-019, RF-020 y RNF completos.

Entregables: - Pruebas funcionales, integración, permisos, seguridad y
rendimiento. - Revisión de accesibilidad. - Backups y prueba de
restauración. - Manual de usuario y manual técnico. - Plan de despliegue
y reversión. - Monitoreo, alertas y responsables operativos. -
Aprobación de negocio y TI.

Criterio de salida: no quedan defectos críticos o altos sin aceptación
explícita de riesgo; los responsables aprueban la puesta en producción.

## 12. Dependencias y orden lógico

``` text
Fase 0 Descubrimiento
   └── Fase 1 Fundación / datos / seguridad
       ├── Fase 2 Identidad + sincronización M365
       └── Fase 3 Cursos + módulos + archivos
            └── Fase 4 Quiz + reglas de finalización
                 └── Fase 5 Asignación + catálogo + progreso
                      ├── Fase 6 Certificados + correo
                      └── Fase 7 Reportes + horas
                           └── Fase 8 Producción y operación
```

La implementación de cursos puede comenzar en paralelo con la
sincronización solo si la estructura de usuarios, autenticación y
permisos está definida y los ambientes de desarrollo lo permiten.

## 13. Matriz de trazabilidad resumida

  Requisito                    Fase principal    Dependencias clave
  ---------------------------- ----------------- ------------------------
  RF-001 Sincronización M365   2                 RT-001, RT-002, RT-003
  RF-002 Autenticación         2                 RT-004, RF-001
  RF-003 Roles                 1                 RT-005
  RF-004 Cursos                3                 RF-003, RT-006
  RF-005 Módulos               3                 RF-004
  RF-006 Videos                3                 RF-005, RT-007
  RF-007 Recursos              3                 RF-005, RT-007, RT-011
  RF-008 Quiz                  4                 RF-004, RF-005, RT-008
  RF-009 Asignación            5                 RF-001, RF-003, RF-004
  RF-010 Catálogo              5                 RF-002, RF-004
  RF-011 Progreso              4--5              RF-005 a RF-009
  RF-012 Certificados          6                 RF-008, RF-011, RT-009
  RF-013 Correo                6                 RF-012, RT-010
  RF-014 Inicio/horas          5--7              RF-009, RF-011, RF-012
  RF-015 Consola admin         1, 3, 5--7        RF-003
  RF-016 Reportes              7                 RF-001, RF-009, RF-011
  RF-017 Auditoría             1 y transversal   RF-003
  RF-018 Usabilidad            transversal       Diseño y componentes
  RF-019 Errores/tareas        transversal       RT-002, RT-010
  RF-020 Retención             1 y 8             RT-003, RT-007

## 14. Reglas de negocio que deben cerrarse antes de producción

1.  ¿Qué usuarios de Entra ID se incluyen y cuáles se excluyen?
2.  ¿Qué significa "usuario eliminado": deshabilitado, eliminado
    definitivamente o ausente de una sincronización completa?
3.  Entra ID para iniciar sesión: confirmado (sección 4.1).
4.  ¿Qué grupos, departamentos o atributos estarán disponibles para
    asignación?
5.  ¿Qué cursos requieren quiz para aprobar?
6.  ¿El progreso se basa en módulos, videos, actividades o combinación?
    ¿Qué porcentaje exige cada componente?
7.  ¿Se exige reproducir cierto porcentaje de un video o solo marcar una
    actividad como completada?
8.  ¿Cuántos intentos de quiz se permiten y se pueden reiniciar
    manualmente?
9.  ¿La aprobación exige completar todos los módulos y aprobar todos los
    quizzes?
10. ¿Las horas anuales serán estimadas, efectivas o reconocidas? ¿Se
    reconocen solo al aprobar?
11. ¿Los cursos opcionales requieren aprobación para inscribirse?
12. ¿Qué pasa con un empleado que cambia de correo, departamento o sede?
13. ¿Qué pasa con un usuario inactivo que tiene cursos pendientes?
14. ¿Las modificaciones a un curso publicado obligan a repetirlo?
15. ¿Quién puede reemitir o invalidar certificados?
16. ¿Qué tamaño máximo tendrán videos y documentos y dónde se
    almacenarán?
17. ¿Qué canal de correo está autorizado y cuál será el remitente?
18. ¿Qué zona horaria se usará para fechas y para el año calendario?
19. ¿Qué datos pueden exportarse y quién puede hacerlo?
20. ¿Qué política de retención y privacidad aplica a intentos,
    certificados y logs?

Si una respuesta aún no existe, documentarla como decisión pendiente con
responsable, fecha objetivo e impacto.

## 15. Estrategia de pruebas

### Pruebas unitarias y de lógica

-   Cálculo de progreso para cursos con distintos módulos.
-   Puntaje y resultado de quiz.
-   Cálculo de horas por año calendario.
-   Idempotencia de asignaciones, certificados y notificaciones.
-   Reglas de transición de estado.

### Pruebas de integración

-   Microsoft Graph: paginación, throttling, credenciales inválidas,
    error de red y respuestas incompletas.
-   Base de datos: integridad, índices, restricciones y migraciones.
-   Almacenamiento: carga, lectura autorizada, descarga denegada y
    archivos inválidos.
-   PDF: acentos, caracteres especiales, nombres largos y paginación.
-   Correo: éxito, rechazo, timeout y reintento.

### Pruebas de seguridad

- Acceso a recursos ajenos modificando IDs y comprobación de aislamiento
  entre estudiantes, gestores y administradores.
- Elevación de privilegios, autorización denegada por defecto y revisión
  de cada operación administrativa/exportación.
- SQL injection, XSS, CSRF, path traversal, open redirect, clickjacking
  y validación de cabeceras/cookies.
- Manipulación de porcentaje, puntaje, resultado, rol, usuario, duración
  de video o estado de aprobación desde el navegador.
- Acceso a videos/documentos/certificados sin sesión o sin autorización;
  pruebas de MIME falso, archivos excesivos, archivos maliciosos y rutas
  manipuladas.
- Escaneo del repositorio y artefactos para detectar secretos; confirmar
  que los tokens/API keys no aparecen en código, configuración pública,
  logs, mensajes de error, URLs o repositorio.
- Confirmar que los secretos se obtienen desde el mecanismo seguro
  elegido, que los permisos de archivos/configuración son mínimos y que
  el proceso de rotación/revocación está documentado.
- Revisar permisos de Graph, cadena de conexión SQL, cuenta de ejecución,
  TLS/certificados y exposición de puertos.
- Revisar dependencias y versiones vulnerables; documentar resultados,
  hallazgos, severidad, remediación y riesgos aceptados.
- Confirmar que producción no muestra errores detallados, stack traces,
  rutas físicas ni información interna.

### Lista de verificación de salida a producción

No autorizar el despliegue hasta verificar y registrar evidencia de:

1. Secretos fuera del código y del repositorio; escaneo de secretos sin
   hallazgos pendientes y rotación de cualquier credencial previamente
   expuesta.
2. Identidades y permisos mínimos para Microsoft Graph, SQL Server,
   correo y sistema operativo; credenciales distintas por ambiente.
3. Autenticación, MFA/políticas corporativas aplicables, sesiones,
   cookies y autorización por recurso probadas.
4. HTTPS/TLS válido en todos los enlaces relevantes; SQL Server no
   expuesto públicamente y reglas de firewall aprobadas.
5. Validación de entradas, consultas parametrizadas, salida escapada,
   protección CSRF y configuración de cabeceras revisadas.
6. Archivos y videos almacenados en ubicación privada, cargas validadas,
   ejecución deshabilitada y descargas autorizadas.
7. Logs sin secretos ni datos innecesarios, con permisos y retención
   definidos; monitoreo y alertas operativos.
8. Parches y dependencias revisados; hallazgos críticos/altos corregidos
   o excepción formal de riesgo aprobada.
9. Respaldos cifrados cuando corresponda, restauración probada y RPO/RTO
   definidos con TI.
10. Pruebas funcionales, integración, regresión, seguridad y rendimiento
    ejecutadas; resultados y limitaciones documentados.
11. Plan de despliegue, reversión, responsables operativos, gestión de
    incidentes y manual técnico disponibles.
12. Aprobación explícita de TI/seguridad y del responsable de negocio.

### Pruebas funcionales de extremo a extremo

1.  Sincronizar un usuario nuevo.
2.  Autenticarlo.
3.  Crear y publicar un curso.
4.  Asignarlo a un grupo de empleados.
5.  Verificar que un colaborador lo encuentra en su inicio.
6.  Completar módulos y presentar quiz.
7.  Confirmar progreso, aprobación, certificado y correo.
8.  Verificar reportes de asignados, no iniciados y completados.
9.  Verificar horas del año calendario.
10. Archivar el curso y confirmar que se conserva el historial.

## 16. Entregables requeridos por cada fase

Para cada fase el LLM debe entregar:

1.  Resumen de alcance implementado.
2.  Requisitos completados y pendientes, identificados por ID.
3.  Diagrama o explicación de los cambios de arquitectura.
4.  Cambios de esquema y migraciones.
5.  Código, migraciones y pruebas en el repositorio de Azure DevOps.
6.  Configuración requerida por ambiente, sin incluir secretos.
7.  Pruebas realizadas y resultados reales.
8.  Riesgos, supuestos y decisiones pendientes.
9.  Instrucciones para desplegar, validar y revertir.
10. Actualización de la documentación técnica y de la matriz de
    trazabilidad.

No avanzar automáticamente a la siguiente fase hasta que el responsable
confirme la aceptación de la fase actual.

## 17. Prompt inicial recomendado para utilizar este documento

> Actúa como arquitecto de software senior y desarrollador experto en
> Django, Python, Vue.js, SQL Server, Microsoft Entra ID y
> Microsoft Graph. Usa el archivo de especificación como fuente de
> verdad para construir la plataforma de capacitación de Río Grande
> Foods.
>
> Trabaja exclusivamente en la **Fase 0 --- Descubrimiento y línea
> base**. No implementes todavía módulos funcionales ni modifiques datos
> de producción.
>
> Primero inspecciona el entorno disponible y documenta las versiones de
> Python, Django, Node.js, motor de base de datos, estructura actual,
> autenticación, almacenamiento, correo y capacidad de ejecutar tareas
> programadas. No inventes valores que no puedas verificar.
>
> Después produce un informe de descubrimiento, un diagrama de
> arquitectura inicial, un registro de decisiones pendientes y una
> matriz que relacione los requisitos RF, RNF y RT con sus dependencias.
> Señala riesgos técnicos y preguntas bloqueantes. Respeta la identidad
> visual del brandbook adjunto, en particular el azul `#003D7C`,
> amarillo `#F1CF00`, beige `#C7B99A`, rojo `#BF0811`, la personalidad
> cálida y acogedora y las reglas de uso del logotipo.
>
>
> **Controles de seguridad obligatorios en todas las fases:** nunca
> incluyas tokens, API keys, contraseñas, client secrets, certificados
> privados o cadenas de conexión con credenciales en código, SQL,
> repositorio, logs, URLs ni documentación. Diseña y documenta cómo se
> obtendrán los secretos desde un gestor aprobado o configuración externa
> protegida, con permisos mínimos y separación por ambiente. No inventes
> credenciales ni solicites que se peguen en el chat. Revisa mínimo
> privilegio para Microsoft Graph y SQL Server; identifica amenazas,
> valida autorización en el servidor, protege archivos y sesiones, y
> define pruebas de seguridad para cada requisito. Si detectas un secreto
> expuesto, detén el proceso, no lo repitas y recomienda su revocación y
> rotación. Antes de producción exige una lista de verificación con
> evidencias y aprobación explícita; no declares que el sistema es seguro
> sin pruebas verificables.
>
> Cuando termines, detente y espera aprobación. No avances a la Fase 1
> sin autorización explícita.

## 18. Glosario

-   **Microsoft Entra ID:** servicio de identidad de Microsoft que
    administra usuarios y aplicaciones del tenant.
-   **Microsoft Graph:** API para acceder de forma autorizada a datos y
    servicios de Microsoft 365/Entra ID.
-   **Tenant:** instancia organizacional de Microsoft Entra ID/Microsoft
    365.
-   **Idempotencia:** propiedad por la que repetir una operación no crea
    efectos duplicados.
-   **Borrado lógico:** marcar un registro como inactivo/archivado sin
    eliminar su historial.
-   **RPO/RTO:** objetivos de pérdida de datos y tiempo de recuperación.
-   **Progreso:** medida de avance de un colaborador en los elementos
    requeridos del curso.
-   **Duración reconocida:** tiempo que la organización decide
    contabilizar como capacitación completada.
-   **Django:** framework web de Python con ORM, autenticación, CSRF y
    migraciones.
-   **Vue.js:** framework de interfaz de usuario en JavaScript.
-   **LTS:** versión con soporte de seguridad extendido por el proveedor.
-   **ORM:** capa de Django que traduce objetos Python a consultas SQL
    parametrizadas.
