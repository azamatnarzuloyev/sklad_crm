# Generated by Django 4.2.5 on 2024-04-13 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puttyMagazin', '0003_zakasproduct_nomer_zakas'),
    ]

    operations = [
        migrations.AddField(
            model_name='zakasproduct',
            name='date_filter',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zakasproduct',
            name='shop_name',
            field=models.CharField(blank=True, null=True),
        ),
    ]
