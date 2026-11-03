"""Correos transaccionales con el branding de la plataforma (SiteSettings).
Si no hay servidor SMTP configurado (EMAIL_HOST vacío), Django usa la consola:
el correo queda en el log del contenedor y nada se rompe."""
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

log = logging.getLogger(__name__)

def _site():
    from apps.platform.models import SiteSettings
    s = SiteSettings.objects.filter(pk=1).first()
    return s

def _logo_url(s):
    if s and s.logo_url:
        return s.logo_url
    if s and s.logo_file:
        return settings.SITE_BASE_URL.rstrip("/") + "/api/branding/logo/"
    return ""

def send_branded_email(user, subject, headline, paragraphs, cta_text=None, cta_path="/"):
    if not getattr(user, "email", ""):
        return 0
    s = _site()
    platform = s.platform_name if s else "Academia"
    company = s.company_name if s else ""
    primary = s.primary_color if s else "#4F46E5"
    accent = s.accent_color if s else "#F59E0B"
    logo = _logo_url(s)
    name = (user.display_name or user.username or "").split(" ")[0]
    base = settings.SITE_BASE_URL.rstrip("/")
    body_paras = "".join(f'<p style="margin:0 0 12px;font-size:15px;line-height:1.55;color:#333">{p}</p>' for p in paragraphs)
    logo_html = f'<img src="{logo}" alt="{company}" style="max-height:44px"/>' if logo else ""
    cta = (f'<p style="margin:22px 0 4px"><a href="{base}{cta_path}" style="background:{accent};color:#191904;'
           f'text-decoration:none;font-weight:700;padding:12px 22px;border-radius:9px;display:inline-block">{cta_text}</a></p>') if cta_text else ""
    html = f"""<!doctype html><html><body style="margin:0;background:#FAF5EC;font-family:Segoe UI,Arial,sans-serif">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#FAF5EC;padding:28px 0"><tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #E9E1D2">
<tr><td style="background:{primary};padding:20px 28px">{logo_html}<span style="color:#ffffff;font-size:19px;font-weight:800">{platform}</span> <span style="color:#DCE7F2;font-size:13px">· {company}</span></td></tr>
<tr><td style="padding:26px 28px"><h1 style="margin:0 0 14px;font-size:21px;color:#1C2B39">{headline}</h1>
<p style="margin:0 0 12px;font-size:15px;color:#333">Hola, {name}.</p>{body_paras}{cta}
<p style="margin:20px 0 0;font-size:12.5px;color:#68737E">Este es un mensaje automático de {platform} ({company}). Si tienes dudas, responde a este correo o contacta a tu área de capacitación.</p></td></tr>
</table></td></tr></table></body></html>"""
    msg = EmailMultiAlternatives(subject=subject, body=strip_tags(html), from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email])
    msg.attach_alternative(html, "text/html")
    try:
        sent = msg.send(fail_silently=False)
        log.info("Correo enviado a %s: %s (n=%s)", user.email, subject, sent)
        return sent
    except Exception as e:
        log.warning("No se pudo enviar correo a %s (%s): %s", user.email, subject, e)
        return 0

def send_assignment_email(user, course, due_at=None):
    due_txt = ""
    if due_at:
        due_txt = f" La fecha límite para completarlo es el <strong>{due_at.strftime('%d/%m/%Y')}</strong>."
    return send_branded_email(
        user,
        subject=f"Nuevo curso asignado: {course.title}",
        headline="Tienes un curso nuevo 🎓",
        paragraphs=[f"Se te asignó el curso <strong>{course.title}</strong> en la plataforma de capacitación.{due_txt}",
                    "Ingresa cuando quieras y avanza a tu ritmo: el progreso se guarda automáticamente según veas los videos, consultes los recursos y apruebes el quiz."],
        cta_text="Ir al curso", cta_path=f"/curso/{course.id}")

def send_due_reminder_email(user, course, days_left, due_at):
    when = "hoy" if days_left == 0 else (f"en {days_left} día" + ("s" if days_left != 1 else ""))
    return send_branded_email(
        user,
        subject=f"Recordatorio: «{course.title}» vence {when}",
        headline="Tu curso está por vencer ⏰",
        paragraphs=[f"El curso <strong>{course.title}</strong> vence <strong>{when}</strong> ({due_at.strftime('%d/%m/%Y')}) y aún no lo has completado.",
                    "Dedícale unos minutos hoy para terminarlo a tiempo y obtener tu certificado."],
        cta_text="Continuar el curso", cta_path=f"/curso/{course.id}")
