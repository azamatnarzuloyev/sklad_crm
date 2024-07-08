# Generated by Django 4.2.5 on 2024-04-15 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savdo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavdoSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skidka_bool', models.BooleanField(blank=True, default=False)),
                ('skidka', models.IntegerField(blank=True, default=0)),
                ('min_cashback', models.IntegerField(blank=True, default=1)),
                ('cashback_tolov_foiz', models.IntegerField(blank=True, default=50)),
                ('cashback_min', models.IntegerField(blank=True, null=True)),
                ('client_chekout', models.BooleanField(blank=True, default=True)),
            ],
        ),
    ]
