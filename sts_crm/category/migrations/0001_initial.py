# Generated by Django 4.2.5 on 2024-02-26 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_name', models.CharField(max_length=200, unique=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='categories/main/imgs/', verbose_name=' Main Category Image')),
                ('slug', models.SlugField(blank=True, editable=False, null=True, unique=True)),
                ('main_meta', models.CharField(blank=True, max_length=200, null=True)),
                ('main_content', models.CharField(blank=True, max_length=300, null=True)),
                ('sts_site', models.BooleanField(default=False)),
                ('rts_site', models.BooleanField(default=False)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'MainCategory',
                'ordering': ['pk', 'main_name'],
            },
        ),
        migrations.CreateModel(
            name='SuperCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('super_name', models.CharField(max_length=200, unique=True)),
                ('category_image', models.ImageField(blank=True, help_text='Please use our recommended dimensions: 120px X 120px', null=True, upload_to='categories/super/imgs/', verbose_name='Category Image')),
                ('slug', models.SlugField(blank=True, editable=False, null=True, unique=True)),
                ('meta_name', models.CharField(blank=True, max_length=200, null=True)),
                ('meta_content', models.CharField(blank=True, max_length=300, null=True)),
                ('sts_site', models.BooleanField(default=False)),
                ('rts_site', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'SuperCategory',
                'ordering': ['pk', 'super_name'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=200, unique=True)),
                ('sub_image', models.ImageField(blank=True, null=True, upload_to='categories/main/imgs/', verbose_name='Sub Category Image')),
                ('slug', models.SlugField(blank=True, editable=False, null=True, unique=True)),
                ('sub_meta', models.CharField(blank=True, max_length=200, null=True)),
                ('sub_content', models.CharField(blank=True, max_length=300, null=True)),
                ('sts_site', models.BooleanField(default=False)),
                ('rts_site', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('mainCategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.maincategory')),
            ],
            options={
                'verbose_name_plural': 'SubCategory',
                'ordering': ['pk', 'sub_name'],
            },
        ),
        migrations.AddField(
            model_name='maincategory',
            name='superCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.supercategory'),
        ),
    ]
