from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.FileField(blank=True, null=True, upload_to="avatars/"),
        ),
        migrations.AddField(
            model_name="user",
            name="language",
            field=models.CharField(default="es", max_length=5),
        ),
        migrations.AddField(
            model_name="user",
            name="email_notifications",
            field=models.BooleanField(default=True),
        ),
    ]
