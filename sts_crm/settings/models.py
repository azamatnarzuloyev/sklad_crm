from django.db import models
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
# Create your models here.

# class ProductSetting(models.Model):
#     pass 

# class PuttySetting(models.Model):
#     pass 



class SavdoSetting(models.Model):
    skidka_max = models.IntegerField(blank=True , default=0,  verbose_name=_('sklida foizda'), help_text=_("bunda foizlarda ko'rsatiladi")) 
    skidkaSetting = models.BooleanField(default=False , blank=True , help_text=_("yoqilsa settingdagi skidka foydalanish ishga tushadi "))
    skidkaYoqish = models.BooleanField(default=False , blank=True, help_text=_("bu skidka berishni yoqish "))
    tavar_skidka = models.BooleanField(default=False, blank=True , help_text=_("bunda tavarni skidkasi ishga tushirish"))
    dokonSettings_skidka = models.BooleanField(default=False , blank=True)
    cashback_min = models.IntegerField(blank=True , null=True , verbose_name=_("cashback min miqdor"),  help_text=_("cashback min miqdori kiritiladi"))
    cashback_max = models.IntegerField(blank=True , verbose_name=_("cashback max miqdor") , help_text=_("client yechib oladigan max miqdor"))
    diller_verfify = models.BooleanField(default=False , blank=True, verbose_name=_("diller register sms"), help_text=_("diller royhatga olish uchun sms yuborish true yuboriladi false yuborilmaydi"))
    savdo_stop = models.BooleanField(default=True , blank=True , help_text=_("Agar true savdo amalga oshiriladi false savdo to'xtatiladi"))
    update_json = models.JSONField(blank=True , null=True)
    create_at =  models.DateTimeField(auto_now_add=True , blank=True)
    update_at = models.DateTimeField(auto_now=True, blank=True)
    cashbackYoqish = models.BooleanField(default=False, blank=True) 
    # cashbackSumma_skidkaTrue = models.IntegerField(blank=True , null=True) 



# class SiteSetting(models.Model):
#     pass 

# class ClientSetting(models.Model):
#     pass 

# class AdminCrmSetting(models.Model):
#     pass 

# class MobileClientSetting(models.Model):
#     pass

# class MobileCostumer(models.Model):
#     pass 


# class AdminSetting(models.Model):
#     pass

# class DesktopSetting(models.Model):
#     pass 



# class AllSetting(models.Model):
#     setting_name = models.CharField(max_length=200, blank=True)
#     productSetting = models.OneToOneField(ProductSetting , on_delete=models.SET_NULL , blank=True , null=True)
#     savdo_setting =  models.OneToOneField(SavdoSetting , on_delete=models.SET_NULL , blank=True , null=True)
#     putty_setting = models.OneToOneField(PuttySetting , on_delete=models.SET_NULL , blank=True , null=True)
#     sitesetting = models.OneToOneField(SiteSetting , on_delete=models.SET_NULL , blank=True , null=True)
#     client_setting = models.OneToOneField(ClientSetting , on_delete=models.SET_NULL , blank=True , null=True)
#     crmadminsetting = models.OneToOneField(AdminCrmSetting ,on_delete=models.SET_NULL , blank=True , null=True)
#     mobileclient = models.OneToOneField(MobileClientSetting , on_delete=models.SET_NULL , blank=True , null=True)
#     mobilecostumer = models.OneToOneField(MobileCostumer , on_delete=models.SET_NULL , blank=True , null=True)
#     adminsetting = models.OneToOneField(AdminSetting , on_delete=models.SET_NULL , blank=True , null=True)
#     desktopsetting = models.OneToOneField(DesktopSetting , on_delete=models.SET_NULL , blank=True , null=True)
#     setting_json = models.JSONField(blank=True, null=True)
#     settingupdate_json = models.JSONField(blank=True, null=True)
#     create_at = models.DateTimeField(auto_now_add=True, blank=True)




