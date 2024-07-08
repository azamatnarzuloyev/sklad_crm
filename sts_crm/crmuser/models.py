from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from account.models import User

# Super user foydalanuvchi yaratish (Bu foydalanuvchi barcha ruxsatlarga ega bo’ladi Butun tizimni boshqarish uchun to’liq permissionga ega bo’ladi

    


class CrmUserModels(models.Model):
    """ Crm foydalanuvchilarni yaratish """
    telefon_regex = RegexValidator(regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$" , message=_("invalid phone number"))
    telefon = models.CharField(max_length=12 , validators=[telefon_regex] , unique=True , verbose_name=_("pone"))
    ism = models.CharField(max_length=50, help_text=_("ismingizni kiriting: "), verbose_name="ism")
    familya = models.CharField(max_length=50, blank=True , verbose_name=_("familya") )
    user_id = models.OneToOneField(User, on_delete=models.CASCADE , blank=True)
    status_user = models.BooleanField(default=False , blank=True)
    GostUser = "GostUser"
    SuperUser = "SuperUser"
    AdminUser = "AdminUser"
    AnalizUser = "AnalizUser"
    NazoratUser = "NazoratUser"
    user_choise = [
        (SuperUser , 'SuperUser'),
        (AdminUser , 'AdminUser'),
        (AnalizUser , 'AnalizUser'),
        (NazoratUser , 'NazoratUser'),
        (GostUser , 'GostUser')
    ]
    rol = models.CharField(max_length=25 , choices=user_choise , default=GostUser , blank=True , verbose_name=_("user role permission"))

    
    class Meta:
        verbose_name_plural = 'Crm foydanaluvchilar'
        ordering = ["pk"]

    def __str__(self):
        return f"{self.ism}"

    



class KunYopish(models.Model):
    """ Bu admin , analiz nazorat foydalanuvchilar uchun yangi kun ochish va superuser ga malumotlarni jo'natisah uchun xizmat qiladi  """
    kun_ochish = models.BooleanField(default=False , blank=True , verbose_name=_("yangi kun ochish "))
    yopish = models.BooleanField(default=False , blank=True , verbose_name=_("Hisobotlarni yopish")) 
    qabul_qilish = models.BooleanField(default=False , blank=True,  verbose_name=_("qabul qilish status"))
    create_date = models.DateField(blank=True , unique=True, verbose_name=_("yangi kunni yaratish "))
    create_at = models.DateTimeField(auto_now_add=True , blank=True)
    update_at = models.DateTimeField(auto_now=True , blank=True)
    crmuser_id = models.ForeignKey(CrmUserModels , on_delete=models.CASCADE , blank=True, null=True)

    class Meta:
        verbose_name_plural = "Kun Yopish"
        ordering = ["pk", "create_at" , "update_at"]

    def __str__(self):
        return f"{self.create_at}"
    




class XabarlarHujjatlar(models.Model):
    """ Bu Xodimlarni Xujjatlar va xabarl va file  yuborish uchun """
    title = models.CharField(max_length=100, blank=True)
    yuboruvchi_id = models.IntegerField(blank=True , verbose_name=_("yuboruvchi id"))
    qabulqiluvchi_id = models.IntegerField(blank=True, verbose_name=_("qabul qiluvchi id raqami"))
    read_status = models.BooleanField(default=False , blank=True, verbose_name=_("oqiganlik haqida status"))
    content = models.TextField(blank=True, null=True , verbose_name=_("xabar bady qism"))
    json_file = models.JSONField(blank=True, null=True , verbose_name=_("json file qism"))
    file = models.FileField(upload_to="files", blank=True, null=True , verbose_name=_("file data"), help_text=_("doc , pdf , excell read file"))
    file_status = models.BooleanField(default=False, blank=True, verbose_name=_("file status"))
    fileurl = models.URLField(blank=True, null=True , verbose_name=_("file url"))
    fileupdate = models.FileField(upload_to="files", blank=True, verbose_name=_("update files"))
    fileupdate_url = models.URLField(blank=True, null=True, verbose_name=_("file update url"))
    fileupdate_status = models.BooleanField(default=False, blank=True, verbose_name=_("file update status"))
    qabulqilindi = models.BooleanField(default=False, blank=True, verbose_name=_("qabul qilindi status"))
    create_date = models.DateField(auto_now_add=True, blank=True )
    update_at = models.DateTimeField(auto_now=True, blank=True )


    class Meta:
        verbose_name_plural = "Xabar Hujjatlar"
        ordering = ["pk", "create_date" , "update_at"]

    def __str__(self):
        return f"{self.title}"
    


class GoustUsers(models.Model):
    token = models.UUIDField(blank=True)
    create_data = models.DateTimeField(auto_now=True)
    online = models.BooleanField(default=False, blank=True)
    userId = models.IntegerField(blank=True, null=True)
    device = models.CharField(blank=True, null=True)
    ipAdress = models.CharField(blank=True, null=True)



    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
