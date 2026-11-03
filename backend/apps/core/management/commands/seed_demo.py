"""
Datos de prueba del LMS (idempotente): usuarios demo, 3 cursos Case File de Breach Brief
con sus videos (descargados de las URLs en variables SEED_VIDEO_0001/0002/0003 si existen),
módulos, un recurso PDF por curso, un quiz por curso, asignaciones, progreso variado,
certificados, horas repartidas en el año y calificaciones con estrellas.
Uso: python manage.py seed_demo
"""
import os, io
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

PASSWORD = "Demo2026Segura!"

COURSES = [
    {"code": "CF-0001", "title": "Case File #0001: The OpenCode Breach",
     "short": "Cómo una credencial expuesta convirtió una herramienta de IA en un gasto millonario.",
     "desc": "Análisis del caso OpenCode: qué falló, cuánto costó y qué controles lo habrían evitado. Curso de prueba con el video real del episodio.",
     "env": "SEED_VIDEO_0001", "file": "casefile-0001-opencode.mp4", "cover": "cover-cf0001.jpg", "duration": 949, "recognized": 60,
     "quiz": [("¿Cuál fue la puerta de entrada del incidente de OpenCode?", ["Una credencial/token expuesto", "Un ataque de fuerza bruta al VPN", "Un correo de phishing al CEO"], 0),
              ("¿Qué control habría reducido más el impacto?", ["Alertas de consumo y límites por clave", "Cambiar el logo de la app", "Bloquear todos los usuarios"], 0),
              ("Si detectas un gasto anómalo en una cuenta cloud, ¿qué haces primero?", ["Reportarlo por el canal de incidentes", "Ignorarlo hasta fin de mes", "Borrar la cuenta"], 0)]},
    {"code": "CF-0002", "title": "Case File #0002: The MGM Resort Hack",
     "short": "Una llamada de 10 minutos al helpdesk costó $100 millones.",
     "desc": "Ingeniería social contra el helpdesk de MGM: suplantación, restablecimiento de credenciales y lecciones para cualquier mesa de ayuda.",
     "env": "SEED_VIDEO_0002", "file": "casefile-0002-mgm.mp4", "cover": "cover-cf0002.jpg", "duration": 1241, "recognized": 90,
     "quiz": [("¿Cómo entraron los atacantes en MGM?", ["Suplantaron a un empleado ante el helpdesk", "Rompieron el cifrado del casino", "Compraron acceso a un administrador"], 0),
              ("¿Qué debe pedir el helpdesk antes de restablecer una contraseña?", ["Verificación de identidad robusta (MFA/callback)", "Solo el nombre completo", "El color favorito del empleado"], 0),
              ("¿Qué información pública usaron para suplantar?", ["LinkedIn y perfiles públicos", "La nómina interna", "Correos privados"], 0)]},
    {"code": "CF-0003", "title": "Case File #0003: Change Healthcare — One Password, $3 Billion",
     "short": "Un portal sin MFA y una sola contraseña: la brecha que paralizó la salud de EE. UU.",
     "desc": "El ataque a Change Healthcare: acceso remoto sin segundo factor, 9 días dentro de la red y el mayor impacto económico en salud.",
     "env": "SEED_VIDEO_0003", "file": "casefile-0003-change-healthcare.mp4", "cover": "cover-cf0003.jpg", "duration": 916, "recognized": 75,
     "quiz": [("¿Cuál fue el fallo inicial en Change Healthcare?", ["Un portal de acceso remoto sin MFA", "Un USB infectado", "Un empleado despedido"], 0),
              ("¿Cuánto tiempo estuvieron los atacantes dentro antes de detonar?", ["9 días", "9 minutos", "9 meses"], 0),
              ("¿Qué regla resume la lección del caso?", ["Todo acceso remoto exige MFA, sin excepciones", "Las contraseñas largas bastan", "El antivirus lo cubre todo"], 0)]},
]

EMPLOYEES = [
    ("maria.gomez", "María Gómez", "Producción"), ("carlos.ruiz", "Carlos Ruiz", "Producción"),
    ("ana.torres", "Ana Torres", "Calidad"), ("luis.mendez", "Luis Méndez", "Logística"),
    ("sofia.hernandez", "Sofía Hernández", "Calidad"), ("jorge.castillo", "Jorge Castillo", "Mantenimiento"),
    ("laura.diaz", "Laura Díaz", "Administración"), ("pedro.ramirez", "Pedro Ramírez", "Logística"),
]

class Command(BaseCommand):
    help = "Crea los datos de prueba del LMS (idempotente)"
    def handle(self, *args, **opts):
        from apps.users.models import Role
        from apps.courses.models import Category, Course, Module, Video, Resource, Assignment
        from apps.quizzes.models import Quiz, Question, Option
        from apps.progress.models import CourseProgress, VideoProgress
        from apps.certificates.models import Certificate
        from apps.platform.models import CourseRating
        U = get_user_model()
        now = timezone.now()

        for code, name in [("ADMIN", "Administrador de plataforma"), ("GESTOR", "Gestor de cursos"), ("COLABORADOR", "Colaborador / estudiante")]:
            Role.objects.get_or_create(code=code, defaults={"name": name})
        gestor_role = Role.objects.get(code="GESTOR"); colab_role = Role.objects.get(code="COLABORADOR")

        gestor, _ = U.objects.get_or_create(username="gestor.cursos", defaults={"email": "gestor@example.local", "display_name": "Gestora de Cursos (demo)", "department": "Recursos Humanos"})
        gestor.set_password(PASSWORD); gestor.save(); gestor.roles.add(gestor_role)

        employees = []
        for uname, dname, dept in EMPLOYEES:
            u, _ = U.objects.get_or_create(username=uname, defaults={"email": f"{uname}@example.local", "display_name": dname, "department": dept})
            u.set_password(PASSWORD); u.save(); u.roles.add(colab_role); employees.append(u)
        juan = U.objects.filter(username="juan").first()

        cat, _ = Category.objects.get_or_create(name="Ciberseguridad", defaults={"description": "Casos reales de brechas y lecciones aplicables"})

        # Matriz de progreso demo: (empleado_idx, curso_idx) -> estado
        plan = {}
        for ei in range(len(employees)):
            for ci in range(3):
                v = (ei + ci) % 4
                plan[(ei, ci)] = ["aprobado", "en_progreso", "no_iniciado", "aprobado"][v]
        if juan:
            plan[("juan", 0)] = "aprobado"; plan[("juan", 1)] = "en_progreso"; plan[("juan", 2)] = "no_iniciado"

        stars_plan = [5, 4, 5, 4, 3, 5, 4, 5]
        for ci, spec in enumerate(COURSES):
            course, _ = Course.objects.get_or_create(code=spec["code"], defaults={
                "title": spec["title"], "short_description": spec["short"], "description": spec["desc"],
                "category": cat, "course_type": "obligatorio", "status": "publicado",
                "estimated_duration_minutes": round(spec["duration"] / 60), "recognized_duration_minutes": spec["recognized"]})
            course.status = "publicado"; course.save()
            # Imagen miniatura del curso (asset incluido en el repo)
            if spec.get("cover") and not course.cover_key:
                import shutil
                from django.conf import settings as _s
                src = os.path.join(os.path.dirname(__file__), "..", "..", "seed_assets", spec["cover"])
                src = os.path.normpath(src)
                if os.path.exists(src):
                    dest_cover = os.path.join(str(_s.MEDIA_ROOT), "covers", spec["cover"])
                    os.makedirs(os.path.dirname(dest_cover), exist_ok=True)
                    shutil.copyfile(src, dest_cover)
                    course.cover_key = f"covers/{spec['cover']}"; course.save(update_fields=["cover_key"])
            module, _ = Module.objects.get_or_create(course=course, title="Episodio completo", defaults={"description": "Video del caso y materiales de apoyo", "sort_order": 1})

            # Video real: descargar a media si hay URL en el entorno y aún no existe
            storage_key = f"videos/{spec['file']}"
            dest = os.path.join("media_placeholder", storage_key)  # solo referencia; la ruta real usa MEDIA_ROOT abajo
            from django.conf import settings
            dest = os.path.join(str(settings.MEDIA_ROOT), storage_key)
            url = os.environ.get(spec["env"])
            if url and not os.path.exists(dest):
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                import urllib.request
                self.stdout.write(f"Descargando video {spec['code']} desde URL de despliegue...")
                urllib.request.urlretrieve(url, dest)
                self.stdout.write(f"  -> {os.path.getsize(dest)/1e6:.1f} MB guardados")
            video, _ = Video.objects.get_or_create(module=module, title=spec["title"], defaults={"storage_key": storage_key if os.path.exists(dest) else "", "duration_seconds": spec["duration"], "sort_order": 1})

            # Recurso PDF sencillo generado al vuelo
            res_key = f"resources/resumen-{spec['code'].lower()}.pdf"
            res_dest = os.path.join(str(settings.MEDIA_ROOT), res_key)
            if not os.path.exists(res_dest):
                os.makedirs(os.path.dirname(res_dest), exist_ok=True)
                try:
                    from reportlab.lib.pagesizes import letter
                    from reportlab.pdfgen import canvas
                    c = canvas.Canvas(res_dest, pagesize=letter)
                    c.setFont("Helvetica-Bold", 14); c.drawString(72, 720, spec["title"])
                    c.setFont("Helvetica", 11); c.drawString(72, 690, "Resumen del caso (material de prueba del LMS)")
                    c.drawString(72, 665, spec["short"][:95])
                    c.drawString(72, 640, "Lección clave: reporta, verifica y protege tus accesos.")
                    c.save()
                except Exception as e:
                    self.stdout.write(f"PDF no generado ({e}); se omite el recurso")
            if os.path.exists(res_dest):
                Resource.objects.get_or_create(module=module, title=f"Resumen del caso {spec['code']} (PDF)", defaults={"storage_key": res_key, "mime_type": "application/pdf", "size_bytes": os.path.getsize(res_dest)})

            quiz, _ = Quiz.objects.get_or_create(course=course, title=f"Evaluación — {spec['code']}", defaults={"pass_score": 70, "instructions": "Responde las 3 preguntas. Apruebas con 70% o más."})
            if not quiz.questions.exists():
                for qi, (text, opts, correct) in enumerate(spec["quiz"]):
                    q = Question.objects.create(quiz=quiz, question_text=text, points=1, sort_order=qi)
                    for oi, otxt in enumerate(opts):
                        Option.objects.create(question=q, option_text=otxt, is_correct=(oi == correct), sort_order=oi)

            targets = [(f"e{ei}", u) for ei, u in enumerate(employees)] + ([("juan", juan)] if juan else [])
            for key, user in targets:
                state = plan.get((key if key == "juan" else int(key[1:]), ci)) if key == "juan" else plan[(int(key[1:]), ci)]
                Assignment.objects.get_or_create(course=course, user=user, course_version=1, status="activa", defaults={"is_mandatory": True, "assigned_by": gestor})
                months_ago = (ci * 2 + (sum(ord(ch) for ch in user.username) % 3)) % 8
                passed_at = now - timedelta(days=30 * months_ago + 5) if state == "aprobado" else None
                cp, _ = CourseProgress.objects.get_or_create(course=course, user=user, course_version=1)
                cp.status = state
                cp.progress_percent = 100 if state == "aprobado" else (45 if state == "en_progreso" else 0)
                cp.first_started_at = now - timedelta(days=20) if state != "no_iniciado" else None
                cp.last_activity_at = now - timedelta(days=2) if state != "no_iniciado" else None
                cp.completed_at = passed_at; cp.passed_at = passed_at
                cp.save()
                if state in ("aprobado", "en_progreso"):
                    vp, _ = VideoProgress.objects.get_or_create(video=video, user=user)
                    vp.max_position_seconds = spec["duration"] if state == "aprobado" else int(spec["duration"] * 0.45)
                    vp.last_position_seconds = vp.max_position_seconds
                    if state == "aprobado": vp.completed_at = passed_at
                    vp.save()
                if state == "aprobado":
                    Certificate.objects.get_or_create(user=user, course=course, course_version=1, defaults={"completion_date": passed_at.date() if passed_at else now.date(), "recognized_duration_minutes": spec["recognized"]})
                    CourseRating.objects.update_or_create(course=course, user=user, defaults={"stars": stars_plan[sum(ord(ch) for ch in user.username) % len(stars_plan)], "comment": "Curso claro y útil (opinión de prueba)."})
        self.stdout.write(self.style.SUCCESS("Datos de prueba listos: 1 gestor, 8 empleados, 3 cursos Case File con video, quizzes, progreso, certificados y calificaciones."))
        self.stdout.write(f"Contraseña de las cuentas demo: {PASSWORD} (solo ambiente de prueba)")
