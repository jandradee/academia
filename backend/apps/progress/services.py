from django.utils import timezone
from .models import CourseProgress, VideoProgress, ResourceProgress

def _frac(num, den):
    return (num / den) if den else None

def recompute_course_progress(user, course):
    """Progreso real del curso = avance de video (minutos vistos) + recursos vistos + quizzes aprobados.
    Pesos: video 60%, recursos 15%, quiz 25% (se renormalizan si un componente no existe).
    Aprobado: contenido >=95% y 100% de quizzes aprobados -> emite certificado."""
    from apps.courses.models import Video, Resource
    from apps.quizzes.models import Quiz, Attempt
    videos = list(Video.objects.filter(module__course=course))
    vps = {vp.video_id: vp for vp in VideoProgress.objects.filter(user=user, video__in=videos)}
    watched_secs = 0.0; total_secs = 0.0
    for v in videos:
        vp = vps.get(v.id)
        if vp and v.duration_seconds:
            watched_secs += min(vp.max_position_seconds, v.duration_seconds)
        total_secs += v.duration_seconds or 0
    if total_secs > 0:
        video_frac = watched_secs / total_secs
    elif videos:
        done = sum(1 for v in videos if vps.get(v.id) and vps[v.id].completed_at)
        video_frac = done / len(videos)
    else:
        video_frac = None
    resources = list(Resource.objects.filter(module__course=course)) + list(Resource.objects.filter(course=course))
    if resources:
        viewed = ResourceProgress.objects.filter(user=user, resource__in=resources).count()
        res_frac = viewed / len(resources)
    else:
        res_frac = None
    quizzes = list(Quiz.objects.filter(course=course, is_active=True))
    if quizzes:
        passed_q = Attempt.objects.filter(user=user, quiz__in=quizzes, submitted_at__isnull=False, passed=True).values("quiz").distinct().count()
        quiz_frac = passed_q / len(quizzes)
    else:
        quiz_frac = None
    parts = [(0.60, video_frac), (0.15, res_frac), (0.25, quiz_frac)]
    present = [(w, f) for w, f in parts if f is not None]
    progress = round(100 * sum(w * f for w, f in present) / sum(w for w, _ in present), 2) if present else 0
    content_parts = [(0.8, video_frac), (0.2, res_frac)]
    c_present = [(w, f) for w, f in content_parts if f is not None]
    content_frac = (sum(w * f for w, f in c_present) / sum(w for w, _ in c_present)) if c_present else 1.0
    approved = content_frac >= 0.95 and (quiz_frac is None or quiz_frac >= 1.0) and progress > 0
    cp, _ = CourseProgress.objects.get_or_create(course=course, user=user, course_version=course.version)
    now = timezone.now()
    cp.progress_percent = progress
    if progress > 0 and not cp.first_started_at:
        cp.first_started_at = now
    if progress > 0:
        cp.last_activity_at = now
    if approved:
        if cp.status != "aprobado":
            cp.status = "aprobado"; cp.passed_at = now; cp.completed_at = now
            from apps.certificates.models import Certificate
            Certificate.objects.get_or_create(user=user, course=course, course_version=course.version,
                defaults={"completion_date": now.date(), "recognized_duration_minutes": course.recognized_duration_minutes})
    elif progress > 0:
        if cp.status in ("no_iniciado", "vencido"):
            cp.status = "en_progreso"
    cp.save()
    return cp
