# Generated by Django 4.2.5 on 2024-04-27 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_gouseuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="gouseuser",
            name="hostName",
            field=models.CharField(blank=True, default="Desktop"),
        ),
        migrations.AddField(
            model_name="gouseuser",
            name="ip",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="gouseuser",
            name="model",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="gouseuser",
            name="name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]