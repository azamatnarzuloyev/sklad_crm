from django.contrib import admin
from .models import Kard, Hamyon , DepozitCarddata
# Register your models here.
# admin.site.register(Kard)
# admin.site.register(Hamyon)
# admin.site.register(DepozitCarddata)


@admin.register(Kard)
class KardAdmin(admin.ModelAdmin):
    list_display = ("kard_cod", "karta_sum", "activae_kard",)
    list_filter = ("kard_cod","activae_kard",)
    search_fields =("kard_cod",)


@admin.register(Hamyon)
class HamyonAdmin(admin.ModelAdmin):
    list_display = ("id", "karta_date","activete",)
    list_filter = ("id", "karta_date", "activete",)



@admin.register(DepozitCarddata)
class DepozitCarddataAdmin(admin.ModelAdmin):
    list_display = ("depozit_kard", "depozit_sum","activate_depozit",)
    list_filter = ("depozit_kard", "depozit_sum","activate_depozit",)
    search_fields = ("depozit_kard",)