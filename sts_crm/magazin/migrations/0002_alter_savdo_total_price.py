# Generated by Django 4.2.5 on 2024-03-02 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savdo',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
