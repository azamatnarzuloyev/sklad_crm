# Generated by Django 5.0.6 on 2024-06-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0006_productserenapathend_productserenapathfour_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productserenapathend",
            name="productSerena_path",
        ),
        migrations.RemoveField(
            model_name="productserenapathend",
            name="product_serena",
        ),
        migrations.RemoveField(
            model_name="productserenapathfour",
            name="productSerena_path",
        ),
        migrations.RemoveField(
            model_name="productserenapathfour",
            name="product_serena",
        ),
        migrations.RemoveField(
            model_name="productserenapathone",
            name="productSerena_path",
        ),
        migrations.RemoveField(
            model_name="productserenapathone",
            name="product_serena",
        ),
        migrations.RemoveField(
            model_name="productserenapathtwo",
            name="productSerena_path",
        ),
        migrations.RemoveField(
            model_name="productserenapathtwo",
            name="product_serena",
        ),
        migrations.AddField(
            model_name="productserenapathend",
            name="serena_path",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="productserenapathfour",
            name="serena_path",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="productserenapathone",
            name="serena_path",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="productserenapathtwo",
            name="serena_path",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
