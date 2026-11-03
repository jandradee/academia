"""Recordatorio diario: avisa a cada usuario cuando uno de sus cursos vence en 3 días o menos
y aún no lo ha aprobado. Pensado para correr una vez al día (tarea programada de Coolify).
Uso: python manage.py send_due_reminders [--days 3]"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Envía recordatorios por correo de cursos próximos a vencer"
    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=3)
    def handle(self, *args, **opts):
        from apps.courses.models import Assignment
        from apps.progress.models import CourseProgress
        from apps.core.mailer import send_due_reminder_email
        now = timezone.now(); today = now.date()
        limit = now + timedelta(days=opts["days"])
        qs = Assignment.objects.filter(status="activa", due_at__isnull=False, due_at__gte=now - timedelta(days=1), due_at__lte=limit).select_related("user", "course")
        sent = skipped = 0
        for a in qs:
            if a.last_reminder_at and a.last_reminder_at.date() >= today:
                skipped += 1; continue
            cp = CourseProgress.objects.filter(user=a.user, course=a.course).first()
            if cp and cp.status == "aprobado":
                skipped += 1; continue
            days_left = max(0, (a.due_at.date() - today).days)
            if send_due_reminder_email(a.user, a.course, days_left, a.due_at):
                a.last_reminder_at = now; a.save(update_fields=["last_reminder_at"]); sent += 1
            else:
                skipped += 1
        self.stdout.write(self.style.SUCCESS(f"Recordatorios: enviados={sent} omitidos={skipped} (ventana {opts['days']} días)"))
