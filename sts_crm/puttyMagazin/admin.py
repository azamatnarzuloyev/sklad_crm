from django.contrib import admin

# Register your models here.
from .models import TavarPutty , DokonPutty





@admin.register(TavarPutty)
class TavarPuttyAdmin(admin.ModelAdmin):
    list_display = (
       "putty_status",

    )
    list_filter = ("putty_status",)
    search_fields = ("putty_status",)
