from django.contrib import admin
from .models import SubCategory, MainCategory , SuperCategory
# Register your models here.

@admin.register(SuperCategory)
class DokonPuttyAdmin(admin.ModelAdmin):
    list_display = (
       "super_name",

    )
    list_filter = ("super_name",)
    search_fields = ("super_name",)


@admin.register(MainCategory)
class DokonPuttyAdmin(admin.ModelAdmin):
    list_display = (
       "main_name",

    )
    list_filter = ("main_name",)
    search_fields = ("main_name",)

@admin.register(SubCategory)
class DokonPuttyAdmin(admin.ModelAdmin):
    list_display = (
       "sub_name",

    )
    list_filter = ("sub_name",)
    search_fields = ("sub_name",)