from django.apps import AppConfig
class CoreConfig(AppConfig):
    default_auto_field="django.db.models.BigAutoField"
    name="apps.core"
    def ready(self):
        from django.db import connection
        def _wal(sender, connection, **kwargs):
            if connection.vendor == "sqlite":
                with connection.cursor() as c:
                    c.execute("PRAGMA journal_mode=WAL;")
                    c.execute("PRAGMA foreign_keys=ON;")
                    c.execute("PRAGMA busy_timeout=20000;")
        from django.db.backends.signals import connection_created
        connection_created.connect(_wal)
