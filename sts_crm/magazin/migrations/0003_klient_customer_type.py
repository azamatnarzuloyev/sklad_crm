# Generated by Django 4.2.5 on 2024-03-15 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("magazin", "0002_alter_savdo_total_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="klient",
            name="customer_type",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
