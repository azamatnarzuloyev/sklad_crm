from django.db import models
import uuid
from django.core.validators import RegexValidator
from account.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from cash.models import Hamyon
from cash.serializers import PostSerializer

class TashkilotYaratish(models.Model):
    tashkilot_nomi = models.CharField(max_length=100, blank=True)
    phone_regexx = RegexValidator(
        regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$", message=("Invalid phone number.")
    )
    telefon_raqam = models.CharField(
        max_length=12, validators=[phone_regexx], unique=True, verbose_name=("phone")
    )
    inn_raqam = models.BigIntegerField(blank=True, null=True)

    shartnoma_file = models.FileField(upload_to='shartnomalar', blank=True, null=True)

    dagavor = models.FileField(upload_to='dagavorlar', blank=True, null=True)

    Shartnoma_1 = 'Shartnoma qilindi'
    Shartnoma_2 = 'shartnoma yuborildi'
    Shartnoma_3 = "bugaltera file yuborildi"
    Shartnoma_4 = 'pul tushdi'    



    organization_select = [
        (Shartnoma_1, 'Shartnoma qilindi'),
        (Shartnoma_2, 'shartnoma yuborildi'),
        (Shartnoma_3,'bugaltera file yuborildi'),
        (Shartnoma_4,'pul tushdi'),

    ]
    organzation_status =  models.CharField(
        max_length=30,
        choices=organization_select,
        default=Shartnoma_1, blank=True, null=True,
    )


class CommentaryStatus(models.Model):
    comment_title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    comment_text = models.TextField(blank=True, null=True)




class Klient(models.Model):
    """ do'kon klient yaratish har bir klient uchun savdo """
    phone_regexx = RegexValidator(
        regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$", message=("Invalid phone number.")
    )
    client_name = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(
        max_length=12, validators=[phone_regexx], unique=True, verbose_name=("phone")
    )
    passport_image = models.ImageField(upload_to="password/images/", blank=True, null=True)
    passportLocation_image = models.ImageField(upload_to="password/images/", blank=True, null=True)
    location = models.CharField(max_length=300, blank=True, null=True)
    savdo_sum = models.BigIntegerField(blank=True, default=0)
    cashback_register = models.BooleanField(default=False, blank=True)
    foiz = models.PositiveIntegerField(blank=True, null=True)
    foydalanuvchi_turi = models.IntegerField(default=0, blank=True)  # agar qiymat 0 = do'kon 1 = site register  2 = mobile register o'tgan # 3 = diller client 
    customer_type = models.BooleanField(default=False, blank=True)
    hisobraqam_article = ArrayField(models.IntegerField(blank=True, null=True), blank=True, null=True)

    
    Simple = 'Simple'
    Medium = 'Medium'
    Advanced= "Advanced"
    Special = 'special'    



    client_select = [
        (Simple, 'Simple'),
        (Medium, 'Medium'),
        (Advanced,'Advanced'),
        (Special,'Special'),

    ]
    status_client = models.CharField(
        max_length=30,
        choices=client_select,
        default=Simple, blank=True, null=True,
    )
    client_user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
 

    def clientStatusupdate(self):
        if self.savdo_sum <= 1000:
            self.status_client  = self.Simple 
        if self.savdo_sum < 10000 and self.savdo_sum > 1000:
           self.status_client = self.Medium
        if self.savdo_sum < 20000 and self.savdo_sum > 10000:
            self.status_client = self.Advanced
        if self.savdo_sum > 20000:
            self.status_client = self.Special
        return self.status_client
    

    def clientFoizstatus(self):
        if self.savdo_sum <= 1000:
            self.foiz  = 0.05 
        if self.savdo_sum < 10000 and self.savdo_sum > 1000:
           self.foiz = 0.07
        if self.savdo_sum < 20000 and self.savdo_sum > 10000:
            self.foiz = 0.10
        if self.savdo_sum > 20000:
            self.foiz = 0.13
        return self.foiz
    

    def hamyon_client_data(self):
        hamyon_exists:bool = Hamyon.objects.filter(id=self.mobile).values('id').exists()
        if hamyon_exists:
            hamyon = Hamyon.objects.get(id=self.mobile)
            serialzier = PostSerializer(hamyon)
            return {
                "hamyon": serialzier.data 
            }
        
    def qarzdorlik_fn(self):
        qarzdorlik:bool = DaySellerShop.objects.filter(client_uuid__id=self.pk).exists()
        data = []
        summa = 0
        if qarzdorlik:

            qarzlar = DaySellerShop.objects.filter(client_uuid__id=self.pk)
            for i in qarzlar:
                if i.savdo_detail["tolov_usullar"]["qarz"]["active"]:
                    summa = summa + i.savdo_detail["tolov_usullar"]["qarz"]["summa"]
                    arr = {
                        "savdo_id": i.pk,
                        "savdo_nomer": i.daySavdo_nomer,
                        "hisobot": i.savdo_detail['hisobot'],
                        "qarz":i.savdo_detail['tolov_usullar']['qarz'],
                        # "products": i.product_arr,
                    }
                    data.append(arr)
            
        if len(data) > 0:
            return {
                "summa": summa,
                "savdo": data
            }

        else:
            return {
                "summa": None,
                "savdo": [ {
                    "savdo_id": None,
                    "savdo_nomer": None,
                    "products": None,
                    "summa": None  
                }]
            }



        
        

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



def get_savdo_status():
    return {
        "hisobot": { 
            "tavar_summasi": 0, 
            "jami_skidka": 0,
            "olingan_summa": 0, 
            "mahsulotUchun_tolov":0, 
            "tushgan_cashback_summa": None, 
            "yechilgan_cashback_summa": None, 
            "depozitga_tushgan_summa": None,},

        "tolov_usullar": {
            "naxt": {
                "active": False,
                "summa": 0, 
                "check": False
            },
            "plastik": { 
                "active": False, 
                "summa": 0, 
                "check": False,
            },
            "joyidaTolov": { 
                "active": False, 
                "summa": 0, 
                "check": False,  
                "id_raqam": None
            },
            "qarz": {
                "active": False,  
                "summa": 0, 
                "update_at": None, 
                "eslatma": {"date": None, "status": False}, },

            "depozit": { 
                "active": False,
                "summa": 0, 
                "check": False,},
            "shartnoma": {
                "active": False,
                "summa": 0,
                "check": False,
                "id_raqam": None },
            }
        }



class DaySellerShop(models.Model):
    """ Tavarlarni savdosi clientga  urish """
    daySavdo_nomer  =models.IntegerField(blank=True, null=True, unique=True)
    year_filter = models.IntegerField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    savdo_uuid = models.UUIDField(blank=True, null=True)
    savdo_yopish = models.BooleanField(default=False, blank=True)
    sellerdate_create = models.DateField(blank=True, null=True)
    client_uuid = models.ForeignKey(Klient, on_delete=models.SET_NULL, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    product_arr = ArrayField(models.JSONField(blank=True), blank=True, null=True)
    savdo_detail = models.JSONField(blank=True , default=get_savdo_status)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

      
class ShartNoma(models.Model):
    """ Savdo inn orqali to'lash uchun """
    created = models.BooleanField(default=False, blank=True)
    sharnoma_nomer = models.IntegerField(blank=True, null=True)
    arganization_name = models.CharField(max_length=300, blank=True)
    inn_code = models.BigIntegerField(blank=True, null=True)
    files = models.FileField(upload_to="shartnoma",blank=True, null=True)
    status = models.BooleanField(default=False, blank=True)
    savdo_id = models.UUIDField(blank=True, null=True)
    tolangan_summa = models.BigIntegerField(blank=True, null=True)
    qarzdorlik_sum = models.BigIntegerField(blank=True, null=True)
    birja_request = models.BooleanField(default=False, blank=True)
    request_money = models.BooleanField(default=False)
    closes = models.BooleanField(default=False, blank=True)
    data_create = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    product_array = ArrayField(models.JSONField(blank=True), blank=True, null=True)








class NastroykaModel(models.Model):
    savdo_all = models.BooleanField(default=False, blank=True, null=True)
    skidka = models.IntegerField(blank=True, null=True)


class AllShop(models.Model):
    """ do'kon model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foydalanuvchi_ism = models.CharField(max_length=100, blank=True, null=True)
    foydalanuvchi_familya = models.CharField(max_length=100, blank=True, null=True)
    dokon_name = models.CharField(max_length=200, blank=True, null=True, unique=True)
    dokon_url = models.URLField(blank=True, null=True)
    dokon_image = models.ImageField(upload_to='dokonImage', blank=True, null=True)
    shop_status = models.BooleanField(default=False, blank=True)
    zakas_site = models.BooleanField(default=False, blank=True)
    tavar_putty = models.BooleanField(default=False, blank=True)
    passwords =  models.CharField(max_length=100, blank=True, null=True)
    sklad = models.BooleanField(default=False, blank=True, null=True)
    tavarPuttyID = models.UUIDField(default=uuid.uuid4, editable=False, auto_created=True)
    vendor = models.BooleanField(default=False, blank=True)
    userId = models.OneToOneField(User , on_delete=models.SET_NULL, blank=True, null=True)
    nastroyka = models.OneToOneField(NastroykaModel, on_delete=models.SET_NULL, blank=True, null=True)
    dokon_long = models.FloatField(blank=True, null=True)
    dokon_lat = models.FloatField(blank=True, null=True)
    dokon_client = models.ManyToManyField(Klient, blank=True)
    
    class Meta:
        verbose_name_plural = "Barcha dokonlar"
        ordering = ["pk", "foydalanuvchi_ism"]

    def __str__(self):
        return f"{self.dokon_name}"




class Savdo(models.Model):
    """ Do'konda savdolari """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    daySalesDate_create = models.DateField(blank=True, unique=True)
    daySalesCloseDate = models.DateTimeField(blank=True, null=True)
    savdo_status = models.BooleanField(default=False, blank=True)
    kunlik_chiqim = models.PositiveIntegerField(blank=True, null=True)
    camentary_choise = models.ForeignKey(CommentaryStatus, on_delete=models.SET_NULL, blank=True, null=True)
    comentary = models.TextField(blank=True, null=True)
    total_price = models.PositiveIntegerField(blank=True, default=0)
    createdateseller = models.ManyToManyField(DaySellerShop, blank=True)
    savdo_yopish = models.BooleanField(default=False, blank=True)
    kassa_qabul = models.BooleanField(default=False, blank=True)
    shartnoma_create = models.ManyToManyField(ShartNoma, blank=True)
    dokon_id = models.ForeignKey(AllShop, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    

