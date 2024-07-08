
from django.contrib import admin

from .models import KassaDokon, InstallationService , TechnicalStaff

@admin.register(KassaDokon)
class KassaDOkon(admin.ModelAdmin):
    list_display=("day","kassa_status","yaratish", )
    list_filter= ("day",)
    search_fields = ("day",)


@admin.register(TechnicalStaff)
class TechnicalStafAdmin(admin.ModelAdmin):
    list_display =("ism", "familya", "phone",)
    list_filter = ("ish_staj","xodim_band",)
    search_fields = ("ism",)

@admin.register(InstallationService)
class InstallationServiceAdmin(admin.ModelAdmin):
    list_display = ("organization_name","inn_nomer",)
    list_filter = ("create_date","status_servis",)
    search_fields = ("organization_name", "inn_nomer",)
    # popup_response_template=os.path.join(BASE_DIR, 'templates/data.html')




