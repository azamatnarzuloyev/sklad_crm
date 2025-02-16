# Generated by Django 5.0.6 on 2024-06-19 06:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0010_remove_savdo_savdo_files_remove_savdo_savdoluid_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='allshop',
            name='nastroyka',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='magazin.nastroykamodel'),
        ),
        migrations.AlterField(
            model_name='allshop',
            name='userId',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='daysellershop',
            name='client_uuid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='magazin.klient'),
        ),
        migrations.AlterField(
            model_name='daysellershop',
            name='daySavdo_nomer',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='klient',
            name='client_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='savdo',
            name='camentary_choise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='magazin.commentarystatus'),
        ),
        migrations.AlterField(
            model_name='savdo',
            name='dokon_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='magazin.allshop'),
        ),
    ]
