from django.contrib import admin



from .models import User, PhoneOtp,Address , GouseUser

# Register your models here.


@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
    list_display = ( 
        'user','state',
    )
    search_fields = ('user',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone", "first_name",
        "last_name", "is_staff",
        "author", "is_special_user",
    )
    list_filter = ("is_staff", "is_superuser", "groups", 'vendor_user')
    search_fields = ("first_name", "last_name", "phone")
    ordering = ("is_superuser", "is_staff", "pk")


@admin.register(PhoneOtp)
class PhoneOtpAdmin(admin.ModelAdmin):
    list_display = (
        "phone", "otp", "count", "verify",
    )
    search_fields = ("phone", "otp",)

admin.site.register(GouseUser)