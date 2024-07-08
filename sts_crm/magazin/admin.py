from django.contrib import admin

# Register your models here.
from .models import  AllShop , Klient , TashkilotYaratish , Savdo , NastroykaModel
admin.site.register(NastroykaModel)



@admin.register(AllShop)
class AllShopAdmin(admin.ModelAdmin):
    list_display = ("foydalanuvchi_ism", "dokon_name",)
    list_filter = ("vendor", "sklad",)
    search_fields = ("foydalanuvchi_ism",)

@admin.register(Savdo)
class SavdoAdmin(admin.ModelAdmin):
    list_display = ("savdo_status", "savdo_yopish","daySalesDate_create")
    list_filter = ("savdo_status", "savdo_yopish")
    search_fields =("daySalesDate_create",)


@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ("mobile",)
    list_filter = ("client_name","mobile",)
    search_fields = ("client_name", "mobile",)


@admin.register(TashkilotYaratish)
class TashkilotYaratishAdmin(admin.ModelAdmin):
    list_display = ("tashkilot_nomi", "inn_raqam", "telefon_raqam" )
    list_filter = ("tashkilot_nomi", "inn_raqam", "telefon_raqam",)
    search_fields = ("tashkilot_nomi","inn_raqam",)
    