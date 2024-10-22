# Generated by Django 4.2.5 on 2024-04-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GouseUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "token_uuid",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="user uuid"
                    ),
                ),
                ("islogginIn", models.BooleanField(blank=True, default=False)),
                ("divase", models.JSONField(blank=True, null=True)),
                ("create_at", models.DateField(blank=True, null=True)),
                ("create_datetime", models.DateTimeField(auto_now_add=True)),
                ("update_datetime", models.DateTimeField(auto_now=True)),
                ("userId", models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
