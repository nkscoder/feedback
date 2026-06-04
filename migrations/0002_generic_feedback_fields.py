# Generated manually for generic feedback model upgrade

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="feedback",
            options={
                "ordering": ["-submitted_at"],
                "verbose_name": "feedback",
                "verbose_name_plural": "feedback",
            },
        ),
        migrations.AlterField(
            model_name="feedback",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="feedback_entries",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="feedback",
            name="name",
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name="feedback",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="feedback",
            name="rating",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="feedback",
            name="category",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="feedback",
            name="source",
            field=models.CharField(
                blank=True,
                help_text="Page, feature, or route where feedback was submitted.",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="feedback",
            name="link_type",
            field=models.CharField(blank=True, db_index=True, default="generic", max_length=64),
        ),
        migrations.AddField(
            model_name="feedback",
            name="link_id",
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
        migrations.AddField(
            model_name="feedback",
            name="extra_data",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="feedback",
            name="session_key",
            field=models.CharField(blank=True, db_index=True, max_length=40),
        ),
    ]
