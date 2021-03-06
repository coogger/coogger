# Generated by Django 3.0.3 on 2020-02-28 13:21

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.cooggerapp.models.common


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ThreadedComments",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reply_count", models.PositiveIntegerField(default=0)),
                (
                    "created",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="Created"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last update"
                    ),
                ),
                (
                    "permlink",
                    models.PositiveIntegerField(default=99999999999999),
                ),
                ("body", models.TextField()),
                ("image_address", models.URLField(blank=True, null=True)),
                ("object_id", models.PositiveIntegerField()),
                ("depth", models.PositiveIntegerField(default=0)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "reply",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="threaded_comment.ThreadedComments",
                    ),
                ),
                (
                    "to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
                "unique_together": {("user", "permlink")},
            },
            bases=(models.Model, apps.cooggerapp.models.common.View),
        ),
    ]
