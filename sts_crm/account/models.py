from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.admin import display
from django.utils import timezone
from django.db import models
from datetime import date
from .manager import CustomUserManager

# Create your models here.
class GouseUser(models.Model):
    token_uuid = models.CharField(max_length=200, blank=True, verbose_name=_("user uuid"))
    islogginIn = models.BooleanField(default=False, blank=True)
    divase = models.JSONField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    ip = models.CharField(blank=True, null=True)
    model = models.CharField(blank=True, null=True)
    hostName = models.CharField(blank=True, default='Desktop')
    create_at = models.DateField(blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    update_datetime = models.DateTimeField(auto_now=True, blank=True)
    userId = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.create_at is not None:
            self.create_at = date.today()
        return super().save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number.")
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], unique=True, verbose_name=_("phone")
    )
    shop_password = models.CharField(max_length=200, blank=True, null=True)
    vendor_user = models.BooleanField(default=False, blank=True, verbose_name=_("vendor user") )
    first_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("first name")
    )
    last_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("last name")
    )
    author = models.BooleanField(default=False, blank=True, verbose_name=_("author"))
    special_user = models.DateTimeField(
        default=timezone.now, verbose_name=_("Special User")
    )

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_("date joined")
    )
    two_step_password = models.BooleanField(
        default=False, verbose_name=_("two step password"),
        help_text=_("is active two step password?"),
    )
    # userActive = models.BooleanField(default=False, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    @property
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    # @property
    # def divase(self):
    #     goust_bool :bool = GouseUser.objects.filter(userId=self.pk).exists()
    #     if goust_bool:
    #         data_set = []
    #         gost_data = GouseUser.objects.filter(userId=self.pk)
    #         for i in gost_data:
    #             news = {
    #                 "token_uuid": i.token_uuid,
    #                 "islogginIn": i.islogginIn,
    #                 "create_datetime": i.create_datetime,
    #                 "devise": i.divase,
    #                 "name": i.name,
    #                 "host": i.hostName,
    #                 "model": i.model, 
    #             }
    #             data_set.append(news)
    #         return data_set
    #     return None

            



    @display(
        boolean=True,
        description=_("Special User"),
    )
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PhoneOtp(models.Model):
    phone_regex = RegexValidator(
        regex=r"^998\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number."),
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], unique=True, verbose_name=_("phone"),
    )
    otp = models.CharField(max_length=6)

    count = models.PositiveSmallIntegerField(default=0, help_text=_("Number of otp sent"))
    verify = models.BooleanField(default=False, verbose_name=_("is verify"))


    def __str__(self):
        return self.phone

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_nuber = models.CharField(max_length=13)
    address_line_1 = models.TextField()
    town_city = models.TextField(help_text='Enter residing city or town')
    state = models.CharField(max_length=50)
   
  

    class Meta:
        verbose_name_plural = 'Addresses'


"""
toke_uuid : char (200),
user_uuid: []
islogginId: flase 
divase: [],
sessin: ""
create_at: date
crate_time: datetime
update_date: update_datetime
"""



