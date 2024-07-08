from django.db import models
from magazin.models import Savdo
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField


class KassaDokon(models.Model):

    day = models.DateField(blank=True, null=True)

    arr_dokon = models.ManyToManyField(Savdo, blank=True)

    kassa_status = models.BooleanField(default=False, blank=True)
    
    yaratish = models.BooleanField(default=False, blank=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


# technical staff

class TechnicalStaff(models.Model):
    """ yangi ustanofka ishlaydigan xodimni qo'shish """
    ism = models.CharField(max_length=50, blank=True)

    familya = models.CharField(max_length=50, blank=True, null=True)
    
    phone_regex = RegexValidator(
        regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number.")
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], unique=True, verbose_name=_("phone")
    )
    ish_staj = models.CharField(max_length=20, blank=True, null=True)
    
    xodim_band = models.BooleanField(default=False, null=True)

    ishga_kelmagan = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class InstallationService(models.Model):
    """ yangi servis ochish """
    organization_name = models.CharField(max_length=100, blank=True)

    davlatTashkilotYokiXususiy = models.BooleanField(blank=True, null=True)

    inn_nomer = models.BigIntegerField(blank=True, null=True)

    client_name = models.CharField(max_length=50, blank=True, null=True)

    telefon_nomer = models.CharField(max_length=12, blank=True, null=True)

    kun_ochish = models.DateField(blank=True, null=True)

    create_date = models.DateTimeField(blank=True)

    close_date = models.DateTimeField(blank=True, null=True)

    update_date = models.DateTimeField(blank=True, null=True)

    xodim_qoshish = models.ManyToManyField(TechnicalStaff, blank=True)

    baza_create = models.BooleanField(default=False, blank=True)

    dokon_create = models.BooleanField(default=False, blank=True)

    status_servis = models.BooleanField(default=False, blank=True)

    tavarlar_arrs = models.JSONField(blank=True, null=True)

    dokon_name = models.CharField(max_length=100, blank=True, null=True)

    dokon_id = models.UUIDField(blank=True, null=True)

    summa = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class SavdoSetting(models.Model):
    skidka_bool =  models.BooleanField(default=False, blank=True)
    skidka = models.IntegerField(default=0, blank=True)
    min_cashback = models.IntegerField(default=1, blank=True)
    cashback_tolov_foiz = models.IntegerField(default=50, blank=True)
    cashback_min = models.IntegerField(blank=True, null=True)
    client_chekout = models.BooleanField(default=True, blank=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)