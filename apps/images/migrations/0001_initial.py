# Generated by Django 3.0.3 on 2020-02-28 13:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
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
                (
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="Title | Optional",
                        max_length=55,
                        null=True,
                        verbose_name="",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to="images/", verbose_name=""),
                ),
                (
                    "created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Created",
                    ),
                ),
            ],
        ),
    ]
